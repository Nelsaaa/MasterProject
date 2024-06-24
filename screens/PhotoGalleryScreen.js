import React, { useState, useEffect, useCallback } from 'react';
import { StyleSheet, View, Image, FlatList, TouchableOpacity, Text, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from '@react-navigation/native'; // Importez useFocusEffect

export default function PhotoGalleryScreen({ route }) {
  const { photos: initialPhotos = [] } = route.params || {};
  const [photos, setPhotos] = useState(initialPhotos);

  // Utilisez useFocusEffect pour charger les photos à chaque fois que l'écran devient visible
  useFocusEffect(
    useCallback(() => {
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

      loadPhotos(); // Chargez les photos lorsque l'écran devient visible
    }, [])
  );

  const deletePhoto = async (uri) => {
    const newPhotos = photos.filter(photo => photo !== uri);
    setPhotos(newPhotos);
    try {
      await AsyncStorage.setItem('photos', JSON.stringify(newPhotos));
    } catch (error) {
      console.error('Failed to delete photo: ', error);
    }
  };

  const confirmDeletePhoto = (uri) => {
    Alert.alert(
      'Delete Photo',
      'Are you sure you want to delete this photo?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: () => deletePhoto(uri),
        },
      ],
      { cancelable: false }
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={photos}
        keyExtractor={(item) => item}
        renderItem={({ item }) => (
          <View style={styles.photoContainer}>
            <Image source={{ uri: item }} style={styles.photo} />
            <TouchableOpacity style={styles.deleteButton} onPress={() => confirmDeletePhoto(item)}>
              <Text style={styles.deleteButtonText}>Delete</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  photoContainer: {
    margin: 5,
    alignItems: 'center',
  },
  photo: {
    width: 300,
    height: 300,
    borderRadius: 5,
  },
  deleteButton: {
    marginTop: 10,
    padding: 10,
    backgroundColor: 'red',
    borderRadius: 5,
  },
  deleteButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
});
