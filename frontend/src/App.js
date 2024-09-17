import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from './components/Login';
import Register from './components/Register';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import LoginResetPassword from './components/LoginResetPassword';
import ClientForm from './components/ClientForm';
import Clients from './components/Clients'
import ProtectedRoute from './components/ProtectedRoute';
// import Navbar from './components/Navbar'
function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/login-reset-password" element={<ProtectedRoute element={LoginResetPassword} />} />
          <Route path="/add-client" element={<ProtectedRoute element={ClientForm} />} />
          <Route path="/clients" element={<ProtectedRoute element={Clients} />} />
        </Routes>
      </Router>

    </div>
  );
}
export default App;