import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const Library = () => {
  const [projects, setProjects] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const { user, logout } = useAuth();

  useEffect(() => { fetchProjects(); }, []);

  const fetchProjects = () => {
    api.get('/api/projects').then((res) => setProjects(res.data));
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await api.post('/api/projects', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setFile(null);
      fetchProjects();
    } finally {
      setUploading(false);
    }
  };

  const getStatusClass = (status) => {
    if (status === 'DONE') return 'status-done';
    if (status === 'PROCESSING') return 'status-processing';
    return 'status-pending';
  };

  return (
    <div>
      <nav className="navbar">
        <Link to="/" className="nav-logo">Библиотека моделей</Link>
        <div className="nav-links">
          <Link to="/" className="nav-link">Главная</Link>
          <Link to="/library" className="nav-link active">Библиотека</Link>
          <Link to="/profile" className="nav-link">Профиль</Link>
          <span style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
            {user?.full_name} <span style={{ color: 'var(--primary)', fontWeight: '600' }}>({user?.role})</span>
          </span>
          <button onClick={logout} className="btn-secondary" style={{ padding: '8px 16px' }}>Выйти</button>
        </div>
      </nav>

      <div className="container">
        {user?.role !== 'STUDENT' && (
          <div className="glass-card" style={{ padding: '16px 24px', marginBottom: '24px', background: 'rgba(99, 102, 241, 0.05)', border: '1px solid var(--primary)' }}>
            <p style={{ color: 'var(--primary)', fontSize: '14px', fontWeight: '500', margin: 0 }}>
              👁️ Вы просматриваете все проекты группы (роль: {user?.role})
            </p>
          </div>
        )}

        <div className="glass-card" style={{ padding: '32px', marginBottom: '40px' }}>
          <h2 style={{ marginBottom: '20px' }}>Загрузить новый архив для реконструкции</h2>
          <form onSubmit={handleUpload} className="upload-form">
            <label className="file-upload-zone">
              <input type="file" accept=".zip" onChange={(e) => setFile(e.target.files[0])} />
              <div style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>
                {file ? file.name : 'Нажмите или перетащите .zip файл сюда'}
              </div>
              <div style={{ color: 'var(--text-muted)', fontSize: '14px' }}>Поддерживаются только ZIP-архивы с исходными данными</div>
            </label>
            <div className="upload-button-container">
              <button type="submit" className="btn-primary" disabled={!file || uploading}>
                {uploading ? 'Загрузка...' : 'Начать реконструкцию'}
              </button>
            </div>
          </form>
        </div>

        <h2 style={{ marginBottom: '24px' }}>Ваши проекты</h2>
        <div className="grid-3">
          {projects.length === 0 ? (
            <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)', gridColumn: '1 / -1' }}>
              У вас пока нет загруженных проектов
            </div>
          ) : (
            projects.map((project) => (
              <div key={project.id} className="glass-card" style={{ padding: '24px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                  <h3 style={{ fontSize: '18px', wordBreak: 'break-all', flex: 1 }}>{project.title}</h3>
                  <span className={`status-badge ${getStatusClass(project.status)}`} style={{ marginLeft: '12px', flexShrink: 0 }}>
                    {project.status}
                  </span>
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '20px' }}>
                  {new Date(project.created_at).toLocaleString('ru-RU')}
                </p>
                {project.status === 'DONE' && (
                  <Link to={`/viewer/${project.id}`} className="btn-primary" style={{ textAlign: 'center', display: 'block', textDecoration: 'none' }}>
                    Открыть 3D-вьювер
                  </Link>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Library;