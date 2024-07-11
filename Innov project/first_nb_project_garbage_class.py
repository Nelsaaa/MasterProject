# first_nb_project_garbage_class.py

import os
import numpy as np
import torch
import torchvision
from torch.utils.data import random_split, DataLoader
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
from PIL import Image
from pathlib import Path

data_dir = '/Users/nelsayago/Downloads/Innov project 2/Garbage classification/Garbage classification'
classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def multilabel_transform(label):
    multi_label = [0] * len(classes)
    multi_label[label] = 1
    return torch.tensor(multi_label, dtype=torch.float)

train_transformations = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

test_transformations = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

dataset = ImageFolder(data_dir, transform=train_transformations, target_transform=multilabel_transform)
random_seed = 42
torch.manual_seed(random_seed)
train_ds, val_ds, test_ds = random_split(dataset, [1593, 176, 758])
batch_size = 32

train_dl = DataLoader(train_ds, batch_size, shuffle=True, num_workers=4, pin_memory=True)
val_dl = DataLoader(val_ds, batch_size*2, num_workers=4, pin_memory=True)

def accuracy(outputs, labels, threshold=0.5):
    preds = (outputs > threshold).float()
    correct = (preds == labels).float().sum()
    return correct / labels.numel()

class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch
        out = self(images)
        loss = F.binary_cross_entropy_with_logits(out, labels)
        return loss

    def validation_step(self, batch):
        images, labels = batch
        out = self(images)
        loss = F.binary_cross_entropy_with_logits(out, labels)
        acc = accuracy(out, labels)
        return {'val_loss': loss.detach(), 'val_acc': acc}

    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}

    def epoch_end(self, epoch, result):
        print("Epoch {}: train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch+1, result['train_loss'], result['val_loss'], result['val_acc']))

class ResNet(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        self.network = models.resnet50(pretrained=True)
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Sequential(
            nn.Linear(num_ftrs, len(classes)),
            nn.Sigmoid()
        )

    def forward(self, xb):
        return self.network(xb)

def get_default_device():
    return torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

def to_device(data, device):
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device

    def __iter__(self):
        for b in self.dl:
            yield to_device(b, self.device)

    def __len__(self):
        return len(self.dl)

device = get_default_device()

def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.Adam):
    history = []
    optimizer = opt_func(model.parameters(), lr)
    for epoch in range(epochs):
        model.train()
        train_losses = []
        for batch in train_loader:
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        model.epoch_end(epoch, result)
        history.append(result)
    return history

def predict_image(img, model):
    xb = img.unsqueeze(0).to(device)
    yb = model(xb)
    preds = yb.squeeze().cpu().detach().numpy()
    return {classes[i]: preds[i] for i in range(len(preds))}

def save_model(model, path='model.pth'):
    torch.save(model.state_dict(), path)

def load_model(path='model.pth'):
    model = ResNet()
    model.load_state_dict(torch.load(path))
    return model

loaded_model = ResNet()

recycling_scores = {
    'cardboard': 7.5,
    'glass': 8.6,
    'metal': 8.6,
    'paper': 7.3,
    'plastic': 2.4,
    'trash': 0
}

def calculate_recycling_score(predicted_labels):
    total_score = 0
    total_percentage = 0
    for material, percentage in predicted_labels.items():
        score = recycling_scores[material]
        total_score += score * percentage
        total_percentage += percentage
    if total_percentage == 0:
        return 0
    recycling_score = total_score / total_percentage
    return recycling_score

def predict_external_image(image_path, model):
    try:
        image = Image.open(Path(image_path))
        example_image = test_transformations(image)
        predicted_labels = predict_image(example_image, model)
        recycling_score = calculate_recycling_score(predicted_labels)
        print("The image resembles", predicted_labels)
        print(f'The recycling score for the product is: {recycling_score:.2f}/10')
    except FileNotFoundError:
        print(f"File not found: {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    train_dl = DeviceDataLoader(train_dl, device)
    val_dl = DeviceDataLoader(val_dl, device)
    to_device(loaded_model, device)
    evaluate(loaded_model, val_dl)
    num_epochs = 3
    opt_func = torch.optim.Adam
    lr = 5.5e-5
    history = fit(num_epochs, lr, loaded_model, train_dl, val_dl, opt_func)
    save_model(loaded_model, 'model.pth')
    predict_external_image('/Users/nelsayago/Downloads/Innov project 2/photo_test3.jpg', loaded_model)
