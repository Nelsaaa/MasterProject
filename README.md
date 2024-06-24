# README pour l'application

## Introduction

Ce document fournit toutes les instructions nécessaires pour configurer et lancer l'application sur votre machine locale. L'application est composée d'un backend en Python utilisant Flask pour la gestion des utilisateurs et d'un frontend en React Native pour l'interface utilisateur mobile.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les logiciels suivants sur votre machine :

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Node.js (incluant npm)
- Expo CLI pour React Native
- Un émulateur Android/iOS ou un dispositif physique pour tester l'application

## Configuration du Backend

1. **Cloner le dépôt Git** : Clonez le dépôt de l'application sur votre machine locale.

2. **Installer les dépendances** : Naviguez dans le dossier du backend et installez les dépendances Python en utilisant pip :

   ```bash
   cd chemin/vers/le/backend
   pip install -r requirements.txt
   ```

3. **Initialiser la base de données** : Exécutez le script d'initialisation de la base de données pour créer les tables nécessaires :

   ```bash
   python init_db.py
   ```

4. **Lancer le serveur** : Démarrez le serveur backend en exécutant :

   ```bash
   python app.py
   ```

   Assurez-vous que le serveur fonctionne correctement et notez l'URL du serveur (par exemple, `http://localhost:5000`).

## Configuration du Frontend

1. **Installer les dépendances** : Naviguez dans le dossier du frontend et installez les dépendances nécessaires en utilisant npm :

   ```bash
   cd chemin/vers/le/frontend
   npm install
   ```

2. **Configurer l'URL du backend** : Ouvrez le fichier `API.js` (ou tout fichier contenant les configurations d'API) dans le dossier du frontend et remplacez l'URL de l'API par l'URL de votre serveur backend.

3. **Lancer l'application** : Utilisez Expo pour démarrer l'application :

   ```bash
   expo start
   ```

   Un QR code s'affichera dans votre terminal. Scannez ce QR code avec l'application Expo Go (disponible sur Android et iOS) ou lancez un émulateur via les options proposées dans le terminal.

## Tester l'application

- **Créer un compte** : Utilisez l'écran d'inscription pour créer un nouveau compte utilisateur.
- **Se connecter** : Utilisez l'écran de connexion pour accéder à l'application avec les identifiants du compte créé.
- **Utiliser l'application** : Explorez les différentes fonctionnalités de l'application, comme la prise de photos, la visualisation de la galerie, etc.

## Problèmes connus et solutions

- **Problèmes de connexion à la base de données** : Assurez-vous que les informations de connexion à la base de données dans le fichier de configuration du backend sont correctes.
- **Problèmes de dépendances** : Si vous rencontrez des problèmes avec les versions des dépendances, vérifiez leur compatibilité ou essayez de les mettre à jour.

## Contribution

Les contributions à ce projet sont les bienvenues. Veuillez suivre les bonnes pratiques de développement et soumettre des Pull Requests pour toute nouvelle fonctionnalité ou correction de bugs.

---

Ce README devrait vous aider à configurer et lancer l'application sur votre machine locale. Pour toute question ou problème, n'hésitez pas à ouvrir un ticket dans le système de suivi des problèmes du dépôt Git.
