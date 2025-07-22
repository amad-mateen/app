import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';


import Registration from './Registration';
import Login from './Login';
import FraudCheck from './FraudCheck';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Registration />} />
        <Route path="/login" element={<Login />} />
        <Route path="/fraud-check" element={<FraudCheck />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
