import { Link } from 'react-router-dom';

const ShopSuccess = () => {
  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center',
      background: 'var(--bg-light)'
    }}>
      <div className="glass-card" style={{ padding: '48px', textAlign: 'center', maxWidth: '500px' }}>
        <div style={{ fontSize: '80px', marginBottom: '24px' }}>✅</div>
        <h1 style={{ marginBottom: '16px' }}>Оплата успешна!</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '32px' }}>
          Спасибо за покупку. Ваш товар будет доставлен магическим способом.
        </p>
        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
          <Link to="/shop" className="btn-primary">Вернуться в магазин</Link>
          <Link to="/" className="btn-secondary">На главную</Link>
        </div>
      </div>
    </div>
  );
};

export default ShopSuccess;