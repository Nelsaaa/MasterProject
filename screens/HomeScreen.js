import React from 'react';
import { View, Text, Button } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { useNavigation } from '@react-navigation/native'; // Importez useNavigation

const HomeScreen = () => {
  const { user, logout } = useAuth();
  const navigation = useNavigation(); // Utilisez useNavigation pour obtenir l'objet de navigation

  return (
    <View>
      <Text>Welcome, {user?.username}</Text>
      <Button title="Logout" onPress={logout} />
      <Button title="Open Camera" onPress={() => navigation.navigate('Camera')} /> 
        
    </View>
  );
};

export default HomeScreen;