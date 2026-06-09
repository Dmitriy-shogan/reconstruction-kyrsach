import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const Profile = () => {
  const { user, logout } = useAuth();
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    group_name: user?.group_name || '',
    password: '',
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updateData = {};
      if (formData.full_name !== user.full_name) updateData.full_name = formData.full_name;
      if (formData.email !== user.email) updateData.email = formData.email;
      if (formData.group_name !== user.group_name) updateData.group_name = formData.group_name;
      if (formData.password) updateData.password = formData.password;

      await api.patch('/api/users/me', updateData);
      setMessage('✅ Профиль успешно обновлён!');
      setFormData({ ...formData, password: '' });
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage('❌ Ошибка при обновлении');
    }
  };

  return (
    <div>
      <nav className="navbar">
        <Link to="/" className="nav-logo">Настройки профиля</Link>
        <div className="nav-links">
          <Link to="/" className="nav-link">Главная</Link>
          <Link to="/library" className="nav-link">Библиотека</Link>
          <button onClick={logout} className="btn-secondary" style={{ padding: '8px 16px' }}>Выйти</button>
        </div>
      </nav>

      <div className="container" style={{ maxWidth: '600px' }}>
        <div className="glass-card" style={{ padding: '40px' }}>
          <h2 style={{ marginBottom: '24px' }}>Редактирование данных</h2>
          {message && <div style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#6ee7b7', padding: '12px', borderRadius: '8px', marginBottom: '20px', textAlign: 'center' }}>{message}</div>}
          
          <form onSubmit={handleSubmit}>
            <label className="label">Логин (нельзя изменить)</label>
            <input value={user?.login || ''} disabled className="input-field" />
            
            <label className="label">ФИО</label>
            <input name="full_name" value={formData.full_name} onChange={handleChange} className="input-field" />
            
            <label className="label">Email</label>
            <input name="email" type="email" value={formData.email} onChange={handleChange} className="input-field" />
            
            <label className="label">Учебная группа</label>
            <input name="group_name" value={formData.group_name} onChange={handleChange} className="input-field" />
            
            <label className="label">Новый пароль (оставьте пустым, чтобы не менять)</label>
            <input name="password" type="password" value={formData.password} onChange={handleChange} className="input-field" placeholder="••••••••" />
            
            <button type="submit" className="btn-primary" style={{ marginTop: '32px' }}>Сохранить изменения</button>
          </form>
        </div>
      </div>
    </div>
  );
};
export default Profile;