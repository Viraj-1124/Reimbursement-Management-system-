import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';
import { LogOut } from 'lucide-react';

export default function Navbar() {
  const { currentUser, logout } = useAppContext();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (!currentUser) return null;

  return (
    <nav style={{ background: 'var(--color-primary)', color: 'white', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h3 style={{ margin: 0, color: 'white' }}>SmartReimburse AI</h3>
      <div className="flex items-center gap-md">
        <span>{currentUser.name} ({currentUser.role})</span>
        <button className="btn btn-outline" style={{ borderColor: 'var(--color-border)', color: 'white' }} onClick={handleLogout}>
          <LogOut size={16} /> Logout
        </button>
      </div>
    </nav>
  );
}
