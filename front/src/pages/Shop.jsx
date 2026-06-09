import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const Shop = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const { user, logout } = useAuth();

  useEffect(() => {
    api.get('/api/shop/products').then(res => setProducts(res.data));
  }, []);

  const handleBuy = async (product) => {
    setLoading(true);
    try {
      const response = await api.post('/api/shop/create-payment', {
        product_id: product.id,
        return_url: `${window.location.origin}/shop/success`
      });
      
      // Перенаправь на страницу оплаты ЮKassa
      window.location.href = response.data.confirmation_url;
    } catch (error) {
      alert('Ошибка при создании платежа: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <nav className="navbar">
        <Link to="/" className="nav-logo">Магазин</Link>
        <div className="nav-links">
          <Link to="/" className="nav-link">Главная</Link>
          <Link to="/library" className="nav-link">Библиотека</Link>
          <Link to="/shop" className="nav-link active">Магазин</Link>
          <span style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
            {user?.full_name}
          </span>
          <button onClick={logout} className="btn-secondary" style={{ padding: '8px 16px' }}>Выйти</button>
        </div>
      </nav>

      <div className="container">
        <h1 style={{ marginBottom: '32px', textAlign: 'center' }}>Магический магазин</h1>
        
        <div className="grid-3">
          {products.map(product => (
            <div key={product.id} className="glass-card" style={{ padding: '32px', textAlign: 'center' }}>
              <div style={{ 
                width: '100px', 
                height: '100px', 
                margin: '0 auto 20px',
                background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '40px'
              }}>
                ✨
              </div>
              
              <h3 style={{ marginBottom: '12px', fontSize: '20px' }}>{product.name}</h3>
              <p style={{ color: 'var(--text-muted)', marginBottom: '20px', minHeight: '40px' }}>
                {product.description}
              </p>
              
              <div style={{ fontSize: '28px', fontWeight: '700', color: 'var(--primary)', marginBottom: '20px' }}>
                {product.price.toFixed(2)} ₽
              </div>
              
              <button 
                className="btn-primary" 
                onClick={() => handleBuy(product)}
                disabled={loading}
                style={{ width: '100%' }}
              >
                {loading ? 'Обработка...' : 'Купить'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Shop;