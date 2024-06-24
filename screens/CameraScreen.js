import React, { useState, useEffect, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, Image } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import * as MediaLibrary from 'expo-media-library';
import * as Sharing from 'expo-sharing';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function CameraScreen({ navigation }) {
  const [facing, setFacing] = useState('back');
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef(null);
  const [photoUri, setPhotoUri] = useState(null);
  const [photos, setPhotos] = useState([]);

  useEffect(() => {
    loadPhotos();
  }, []);

  const loadPhotos = async () => {
    try {
      const storedPhotos = await AsyncStorage.getItem('photos');
      if (storedPhotos) {
        setPhotos(JSON.parse(storedPhotos));
      }
    } catch (error) {
      console.error('Failed to load photos: ', error);
    }
  };

  const savePhotos = async (newPhotos) => {
    try {
      await AsyncStorage.setItem('photos', JSON.stringify(newPhotos));
    } catch (error) {
      console.error('Failed to save photos: ', error);
    }
  };

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    );
  }

  function toggleCameraFacing() {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync();
        setPhotoUri(photo.uri);
        const newPhotos = [photo.uri, ...photos];
        setPhotos(newPhotos);
        savePhotos(newPhotos);
      } catch (error) {
        console.error('Failed to take picture: ', error);
      }
    }
  };

  const savePhoto = async () => {
    const { status } = await MediaLibrary.requestPermissionsAsync();
    if (status === 'granted' && photoUri) {
      await MediaLibrary.saveToLibraryAsync(photoUri);
      alert('Photo saved to media library!');
      setPhotoUri(null);
    }
  };

  const sharePhoto = async () => {
    if (await Sharing.isAvailableAsync() && photoUri) {
      await Sharing.shareAsync(photoUri);
      setPhotoUri(null);
    }
  };

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} type={facing} ref={cameraRef}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={toggleCameraFacing}>
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={takePicture}>
            <Text style={styles.text}>Take Picture</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('PhotoGallery', { photos })}>
            <Text style={styles.text}>View Gallery</Text>
          </TouchableOpacity>
        </View>
      </CameraView>
      {photoUri && (
        <View style={styles.previewContainer}>
          <Image source={{ uri: photoUri }} style={styles.preview} />
          <TouchableOpacity style={styles.button} onPress={savePhoto}>
            <Text style={styles.text}>Save Photo</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={sharePhoto}>
            <Text style={styles.text}>Share Photo</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
    padding: 10,
    borderRadius: 5,
    margin: 10,
  },
  text: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  previewContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  preview: {
    width: '100%',
    height: '80%',
    resizeMode: 'contain',
    borderWidth: 1,
    borderColor: '#ccc',
  },
});
