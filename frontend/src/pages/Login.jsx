import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { LogIn, UserPlus } from 'lucide-react';
import { fetchCountries } from '../services/api';

export default function Login() {
  const { login, register } = useAppContext();
  const navigate = useNavigate();
  
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [country, setCountry] = useState('');
  
  const [countries, setCountries] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isRegister && countries.length === 0) {
      fetchCountries().then(data => setCountries(data));
    }
  }, [isRegister, countries.length]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    let role;
    if (isRegister) {
      role = await register(name, email, password, companyName, country);
      if (!role) setError('Registration failed. Email might be in use.');
    } else {
      role = await login(email, password);
      if (!role) setError('Invalid email or password');
    }
    
    setLoading(false);

    if (role) {
      if (role === 'EMPLOYEE') navigate('/employee');
      if (role === 'MANAGER') navigate('/manager');
      if (role === 'ADMIN') navigate('/admin'); 
    }
  };

  const inputStyle = {
    padding: '0.75rem',
    borderRadius: '8px',
    border: '1px solid var(--border-color)',
    fontSize: '1rem',
    outline: 'none',
    width: '100%',
    fontFamily: 'inherit'
  };

  const labelStyle = { fontSize: '0.9rem', fontWeight: 500, marginBottom: '0.25rem', display: 'block' };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-lg" style={{ padding: '2rem' }}>
      <div className="text-center">
        <h1>SmartReimburse AI</h1>
        <p className="text-muted">{isRegister ? 'Create a new account' : 'Sign in to your account'}</p>
      </div>

      <div className="card flex flex-col gap-md" style={{ width: '100%', maxWidth: '400px' }}>
        <form onSubmit={handleSubmit} className="flex flex-col gap-md">
          {error && <div style={{ color: 'red', textAlign: 'center', fontSize: '0.9rem' }}>{error}</div>}
          
          {isRegister && (
            <div>
              <label style={labelStyle}>Full Name</label>
              <input 
                type="text" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Alex Smith"
                required={isRegister}
                style={inputStyle}
              />
            </div>
          )}

          <div>
            <label style={labelStyle}>Email Address</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="employee@test.com"
              required 
              style={inputStyle}
            />
          </div>
          
          <div>
            <label style={labelStyle}>Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required 
              style={inputStyle}
            />
          </div>

          {isRegister && (
             <div style={{ borderTop: '1px dashed var(--border-color)', paddingTop: '1rem', marginTop: '0.5rem' }}>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                  <strong>Admin Setup (Optional):</strong> Fill these to create a new Company along with your Admin account. Leave empty to join as standard Employee.
                </p>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={labelStyle}>Company Name</label>
                  <input 
                    type="text" 
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="Acme Corp"
                    style={inputStyle}
                  />
                </div>
                <div>
                  <label style={labelStyle}>Company Country</label>
                  <select 
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    style={inputStyle}
                  >
                    <option value="">Select a country...</option>
                    {countries.map(c => (
                      <option key={c.country} value={c.country}>{c.country} ({c.currency_code})</option>
                    ))}
                  </select>
                </div>
             </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary flex items-center justify-center gap-sm mt-sm"
            disabled={loading}
          >
            {isRegister ? <UserPlus size={18} /> : <LogIn size={18} />} 
            {loading ? 'Processing...' : (isRegister ? 'Sign Up' : 'Sign In')}
          </button>
        </form>
        
        <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>
           <button 
              type="button" 
              onClick={() => { setIsRegister(!isRegister); setError(''); }}
              style={{ background: 'none', border: 'none', color: 'var(--color-primary)', cursor: 'pointer', fontSize: '0.9rem', textDecoration: 'underline' }}
           >
             {isRegister ? 'Already have an account? Sign In' : 'Need an account? Sign Up'}
           </button>
        </div>

        {!isRegister && (
          <div style={{ textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '1rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
            <p style={{ fontWeight: 600, marginBottom: '0.25rem' }}>Demo Accounts Available:</p>
            <p>admin@test.com | manager@test.com | employee@test.com</p>
            <p style={{ marginTop: '0.25rem' }}>Password: <b>password</b></p>
          </div>
        )}
      </div>
    </div>
  );
}
