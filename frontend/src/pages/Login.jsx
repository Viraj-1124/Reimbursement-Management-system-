import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { LogIn } from 'lucide-react';

export default function Login() {
  const { login } = useAppContext();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    const role = await login(email, password);
    setLoading(false);

    if (role) {
      if (role === 'EMPLOYEE') navigate('/employee');
      if (role === 'MANAGER') navigate('/manager');
      if (role === 'ADMIN') navigate('/admin'); 
    } else {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-lg">
      <div className="text-center">
        <h1>SmartReimburse AI</h1>
        <p className="text-muted">Sign in to your account</p>
      </div>

      <div className="card flex flex-col gap-md" style={{ minWidth: '320px' }}>
        <form onSubmit={handleLogin} className="flex flex-col gap-md">
          {error && <div style={{ color: 'red', textAlign: 'center', fontSize: '0.9rem' }}>{error}</div>}
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label style={{ fontSize: '0.9rem', fontWeight: 500 }}>Email Address</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="employee@test.com"
              required 
              style={{
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                fontSize: '1rem',
                outline: 'none'
              }}
            />
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label style={{ fontSize: '0.9rem', fontWeight: 500 }}>Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required 
              style={{
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                fontSize: '1rem',
                outline: 'none'
              }}
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary flex items-center justify-center gap-sm mt-sm"
            disabled={loading}
          >
            <LogIn size={18} /> {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <div style={{ textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '1rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
          <p style={{ fontWeight: 600, marginBottom: '0.25rem' }}>Demo Accounts Available:</p>
          <p>admin@test.com | manager@test.com | employee@test.com</p>
          <p style={{ marginTop: '0.25rem' }}>Password: <b>password</b></p>
        </div>
      </div>
    </div>
  );
}
