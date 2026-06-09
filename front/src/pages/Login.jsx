import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({ 
    login: '', 
    password: '', 
    full_name: '', 
    email: '', 
    group_name: '',
    role: 'STUDENT'
  });
  const [error, setError] = useState('');
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (isRegister) {
        await register(formData);
        await login(formData.login, formData.password);
      } else {
        await login(formData.login, formData.password);
      }
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Произошла ошибка');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', padding: '20px' }}>
      <div className="glass-card" style={{ padding: '40px', width: '100%', maxWidth: '420px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '24px', fontSize: '24px' }}>
          {isRegister ? 'Создать аккаунт' : 'Вход в систему'}
        </h2>
        
        {error && <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', padding: '12px', borderRadius: '8px', marginBottom: '20px', textAlign: 'center', fontSize: '14px' }}>{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <label className="label">Логин</label>
          <input name="login" className="input-field" value={formData.login} onChange={handleChange} required />
          
          <label className="label">Пароль</label>
          <input name="password" type="password" className="input-field" value={formData.password} onChange={handleChange} required />
          
          {isRegister && (
            <>
              <label className="label">ФИО</label>
              <input name="full_name" className="input-field" value={formData.full_name} onChange={handleChange} required />
              
              <label className="label">Email</label>
              <input name="email" type="email" className="input-field" value={formData.email} onChange={handleChange} required />
              
              <label className="label">Учебная группа</label>
              <input name="group_name" className="input-field" value={formData.group_name} onChange={handleChange} required />
              
              <label className="label">Роль</label>
              <select name="role" className="input-field" value={formData.role} onChange={handleChange} required>
                <option value="STUDENT">Студент</option>
                <option value="STAROSTA">Староста</option>
                <option value="ADMIN">Администратор</option>
              </select>
            </>
          )}
          
          <button type="submit" className="btn-primary" style={{ marginTop: '24px' }}>
            {isRegister ? 'Зарегистрироваться' : 'Войти'}
          </button>
        </form>
        
        <button onClick={() => setIsRegister(!isRegister)} className="btn-secondary" style={{ width: '100%', marginTop: '16px' }}>
          {isRegister ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрироваться'}
        </button>
      </div>
    </div>
  );
};
export default Login;