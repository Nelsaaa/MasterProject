import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { useAuth } from '../contexts/AuthContext';
import HomeScreen from '../screens/HomeScreen';
import CameraScreen from '../screens/CameraScreen';
import PhotoGalleryScreen from '../screens/PhotoGalleryScreen';
import AuthNavigator from './AuthNavigator';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

// Création du Bottom Tab Navigator
const BottomTabNavigator = () => (
  <Tab.Navigator>
    <Tab.Screen name="Home" component={HomeScreen} />
    <Tab.Screen name="Camera" component={CameraScreen} />
    <Tab.Screen name="PhotoGallery" component={PhotoGalleryScreen} />
  </Tab.Navigator>
);

const AppNavigator = () => {
  const { user } = useAuth();

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {user ? (
          <Stack.Screen 
            name="Main" 
            component={BottomTabNavigator} 
            options={{ headerShown: false }} 
          />
        ) : (
          <Stack.Screen 
            name="Auth" 
            component={AuthNavigator} 
            options={{ headerShown: false }} 
          />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;