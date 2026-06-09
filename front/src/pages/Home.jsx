import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const Home = () => {
  const [news, setNews] = useState([]);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/api/news').then((res) => setNews(res.data)).catch(() => {});
  }, []);

  return (
    <div>
      <nav className="navbar">
        <Link to="/" className="nav-logo">3D Reconstruction</Link>
        <div className="nav-links">
          <Link to="/" className="nav-link active">Главная</Link>
          <Link to="/library" className="nav-link">Библиотека</Link>
          <Link to="/profile" className="nav-link">Профиль</Link>
          {user?.role === 'ADMIN' && <Link to="/admin/news" className="nav-link">Админ-панель</Link>}
          <span style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
            {user?.full_name} <span style={{ color: 'var(--primary)', fontWeight: '600' }}>({user?.role})</span>
          </span>
          <button onClick={() => { logout(); navigate('/login'); }} className="btn-secondary" style={{ padding: '8px 16px' }}>Выйти</button>
        </div>
      </nav>
      
      <div className="container">
        <h2 style={{ marginBottom: '24px', fontSize: '28px' }}>Последние новости и обновления</h2>
        {news.length === 0 ? (
          <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Новостей пока нет. Ожидайте обновлений от администрации.
          </div>
        ) : (
          <div className="grid-3">
            {news.map((item) => (
              <div key={item.id} className="glass-card" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>{item.title}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '15px', lineHeight: '1.6', marginBottom: '16px' }}>{item.content}</p>
                <small style={{ color: 'var(--primary)', fontSize: '13px' }}>
                  {new Date(item.created_at).toLocaleDateString('ru-RU')}
                </small>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
export default Home;