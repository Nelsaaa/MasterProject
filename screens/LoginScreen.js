import React, { useState } from 'react';
import { View, Button, TextInput, Text, ActivityIndicator } from 'react-native';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import { useAuth } from '../contexts/AuthContext';

const API_URL = 'https://552b-92-89-40-98.ngrok-free.app/login';

const LoginScreen = () => {
  const { login } = useAuth();
  const navigation = useNavigation();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await axios.post(API_URL, { username, password });
      const { user, token } = response.data;
      setMessage('Login successful');
      login({ user, token });
    } catch (error) {
      setMessage(error.response ? error.response.data.msg : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Login" onPress={handleLogin} />
      <Button title="Register" onPress={() => navigation.navigate('Register')} />
      {loading && <ActivityIndicator />}
      {message ? <Text>{message}</Text> : null}
    </View>
  );
};

export default LoginScreen;
