import { Canvas } from '@react-three/fiber';
import { OrbitControls, Box } from '@react-three/drei';
import { useParams, Link } from 'react-router-dom';

const RotatingCube = () => {
  return (
    <mesh>
      <Box args={[2.5, 2.5, 2.5]}>
        <meshStandardMaterial color="#6366f1" roughness={0.3} metalness={0.8} />
      </Box>
    </mesh>
  );
};

const Viewer = () => {
  const { id } = useParams();

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: '#f8fafc' }}>
      <nav className="navbar" style={{ position: 'absolute', width: '100%', zIndex: 10, background: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)' }}>
        <Link to="/" className="nav-logo">3D Viewer</Link>
        <Link to="/library" className="btn-secondary" style={{ textDecoration: 'none' }}>← Назад в библиотеку</Link>
      </nav>
      
      <div style={{ flex: 1, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
        <Canvas camera={{ position: [5, 5, 5], fov: 45 }}>
          <ambientLight intensity={0.6} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          <pointLight position={[-10, -10, -10]} intensity={0.5} color="#6366f1" />
          <RotatingCube />
          <OrbitControls enableZoom={true} autoRotate autoRotateSpeed={1.5} />
          <gridHelper args={[20, 20, '#e2e8f0', '#cbd5e1']} />
        </Canvas>
      </div>
      
      <div style={{ position: 'absolute', bottom: '24px', left: '50%', transform: 'translateX(-50%)', background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(8px)', padding: '12px 24px', borderRadius: '30px', border: '1px solid #e2e8f0', color: '#475569', fontSize: '14px', textAlign: 'center', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        Проект #{id} Левая кнопка: вращение Правая: перемещение Колёсико: зум
      </div>
    </div>
  );
};
export default Viewer;