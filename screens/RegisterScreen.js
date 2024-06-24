import React, { useState } from 'react';
import { View, Button, TextInput, Text, ActivityIndicator } from 'react-native';
import axios from 'axios';

const API_URL = 'https://552b-92-89-40-98.ngrok-free.app/register';

const RegisterScreen = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    setLoading(true);
    try {
      const response = await axios.post(API_URL, { username, email, password });
      setMessage(response.data.msg);
    } catch (error) {
      setMessage(error.response ? error.response.data.msg : 'Registration failed');
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
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Register" onPress={handleRegister} />
      {loading && <ActivityIndicator />}
      {message ? <Text>{message}</Text> : null}
    </View>
  );
};

export default RegisterScreen;
