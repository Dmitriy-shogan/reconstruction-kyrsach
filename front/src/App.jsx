import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Home from './pages/Home';
import Library from './pages/Library';
import Viewer from './pages/Viewer';
import Profile from './pages/Profile';
import AdminNews from './pages/AdminNews';
import Shop from './pages/Shop';
import ShopSuccess from './pages/ShopSuccess';

const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  return user ? children : <Navigate to="/login" />;
};

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
      <Route path="/" element={<PrivateRoute><Home /></PrivateRoute>} />
      <Route path="/library" element={<PrivateRoute><Library /></PrivateRoute>} />
      <Route path="/viewer/:id" element={<PrivateRoute><Viewer /></PrivateRoute>} />
      <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
      <Route path="/admin/news" element={<PrivateRoute><AdminNews /></PrivateRoute>} />
      <Route path="/shop" element={<PrivateRoute><Shop /></PrivateRoute>} />
      <Route path="/shop/success" element={<PrivateRoute><ShopSuccess /></PrivateRoute>} />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;