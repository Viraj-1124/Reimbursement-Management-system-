import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { Shield, User, Building } from 'lucide-react';

export default function Login() {
  const { login } = useAppContext();
  const navigate = useNavigate();

  const handleLogin = (role) => {
    login(role);
    if (role === 'EMPLOYEE') navigate('/employee');
    if (role === 'MANAGER') navigate('/manager');
    if (role === 'ADMIN') navigate('/admin'); 
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-lg">
      <div className="text-center">
        <h1>SmartReimburse AI</h1>
        <p className="text-muted">Hackathon Demo Login</p>
      </div>

      <div className="card flex flex-col gap-md" style={{ minWidth: '320px' }}>
        <h2>Select Demo Role</h2>
        <button className="btn btn-outline flex items-center justify-center gap-sm" onClick={() => handleLogin('EMPLOYEE')}>
          <User size={18} /> Login as Employee
        </button>
        <button className="btn btn-outline flex items-center justify-center gap-sm" onClick={() => handleLogin('MANAGER')}>
          <Building size={18} /> Login as Manager
        </button>
        <button className="btn btn-primary flex items-center justify-center gap-sm" onClick={() => handleLogin('ADMIN')}>
          <Shield size={18} /> Login as Admin
        </button>
      </div>
    </div>
  );
}
