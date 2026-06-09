import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const AdminNews = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ title: '', content: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setMessage('');
  setError('');

  try {
    await api.post('/api/news', {
      title: formData.title,
      content: formData.content
    });

    setMessage('Новость успешно создана');
    setFormData({ title: '', content: '' });
    
    setTimeout(() => {
      navigate('/');
    }, 1500);
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'Ошибка при создании новости';
    setError(typeof errorMessage === 'string' ? errorMessage : 'Ошибка валидации данных');
  }
  };

  if (user?.role !== 'ADMIN') {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', background: 'var(--bg-light)' }}>
        <div className="glass-card" style={{ padding: '40px', textAlign: 'center' }}>
          <h2 style={{ color: 'var(--danger)', marginBottom: '16px' }}>Доступ запрещён</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Только администраторы могут создавать новости</p>
          <Link to="/" className="btn-primary" style={{ marginTop: '24px', display: 'inline-block', textDecoration: 'none', width: 'auto' }}>
            На главную
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      <nav className="navbar">
        <Link to="/" className="nav-logo">Админ-панель</Link>
        <div className="nav-links">
          <Link to="/" className="nav-link">Главная</Link>
          <Link to="/library" className="nav-link">Библиотека</Link>
          <button onClick={logout} className="btn-secondary" style={{ padding: '8px 16px' }}>Выйти</button>
        </div>
      </nav>

      <div className="container" style={{ maxWidth: '700px' }}>
        <div className="glass-card" style={{ padding: '40px' }}>
          <h2 style={{ marginBottom: '8px' }}>📰 Создать новую новость</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>Заполните форму для публикации новости на главной странице</p>

          {message && (
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)', padding: '16px', borderRadius: '8px', marginBottom: '24px', textAlign: 'center', fontWeight: '500' }}>
              {message}
            </div>
          )}

          {error && (
            <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)', padding: '16px', borderRadius: '8px', marginBottom: '24px', textAlign: 'center', fontWeight: '500' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <label className="label">Заголовок новости</label>
            <input
              name="title"
              className="input-field"
              value={formData.title}
              onChange={handleChange}
              placeholder="Например: Обновление системы реконструкции"
              required
              style={{ fontSize: '16px', fontWeight: '500' }}
            />

            <label className="label">Содержание</label>
            <textarea
              name="content"
              className="input-field"
              value={formData.content}
              onChange={handleChange}
              placeholder="Опишите подробности новости..."
              required
              rows="6"
              style={{ fontSize: '15px', resize: 'vertical', lineHeight: '1.6' }}
            />

            <button type="submit" className="btn-primary" style={{ marginTop: '24px' }}>
              Опубликовать новость
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AdminNews;