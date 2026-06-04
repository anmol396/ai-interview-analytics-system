import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import AIAssistant from './pages/AIAssistant';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';

// Protected Route — checks localStorage flag
const ProtectedRoute = ({ children }) => {
  const isAuth = localStorage.getItem('isAuthenticated') === 'true';
  if (!isAuth) {
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  // Session persistence enabled (localStorage removals removed)

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard/ai-assistant" element={<AIAssistant />} />
        <Route path="/about" element={<About />} />
      </Route>
      {/* Catch all redirect to root */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
