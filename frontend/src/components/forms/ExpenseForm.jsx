import { useState, useEffect } from 'react';
import { Sparkles } from 'lucide-react';
import { fetchCountries } from '../../services/api';

export default function ExpenseForm({ initialData = {}, onSubmit, isSubmitting }) {
  const [formData, setFormData] = useState({
    amount: '',
    currency: 'USD',
    date: '',
    vendor: '',
    category: '',
    description: ''
  });

  const [countries, setCountries] = useState([]);
  const uniqueCurrencies = Array.from(new Map(countries.map(c => [c.currency_code, c])).values());

  useEffect(() => {
    fetchCountries().then(data => setCountries(data));
  }, []);

  const [errors, setErrors] = useState({});

  useEffect(() => {
    // Populate form data once OCR results arrive
    if (Object.keys(initialData).length > 0) {
      setFormData(prev => ({
        ...prev,
        amount: initialData.amount || '',
        date: initialData.date || '',
        vendor: initialData.vendor || '',
      }));
    }
  }, [initialData]);

  const validate = () => {
    const newErrors = {};
    if (!formData.amount || formData.amount <= 0) newErrors.amount = "Valid amount is required";
    if (!formData.date) newErrors.date = "Date is required";
    if (!formData.vendor) newErrors.vendor = "Vendor is required";
    if (!formData.category) newErrors.category = "Please select a category";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  const inputStyle = {
    width: '100%',
    padding: '0.8rem',
    borderRadius: 'var(--radius-md)',
    border: '1px solid var(--color-border)',
    marginTop: '0.4rem',
    fontFamily: 'inherit',
    fontSize: '0.95rem'
  };

  const labelStyle = {
    fontWeight: 600,
    fontSize: '0.9rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    color: 'var(--color-text-main)'
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-md">
      <div className="flex gap-md w-full">
        <div style={{ width: '120px', flexShrink: 0 }}>
          <label style={labelStyle}>Currency</label>
          <select 
            style={inputStyle}
            value={formData.currency}
            onChange={(e) => setFormData({...formData, currency: e.target.value})}
          >
            <option value="USD">USD ($)</option>
            {uniqueCurrencies.filter(c => c.currency_code !== 'USD').map(c => (
              <option key={c.currency_code} value={c.currency_code}>{c.currency_code} ({c.currency_symbol || c.currency_code})</option>
            ))}
          </select>
        </div>
        <div style={{ flex: 1 }}>
          <label style={labelStyle}>
            Amount
            {initialData.confidence && (
              <span className="badge badge-success flex items-center gap-sm" style={{ fontSize: '0.75rem', fontWeight: 500 }}>
                <Sparkles size={12} /> AI Extracted ({(initialData.confidence * 100).toFixed(0)}%)
              </span>
            )}
          </label>
          <input 
            type="number" 
            step="0.01"
            style={{ ...inputStyle, borderColor: errors.amount ? 'var(--color-danger-text)' : 'var(--color-border)' }}
            value={formData.amount}
            onChange={(e) => setFormData({...formData, amount: e.target.value})}
            placeholder="0.00"
          />
          {errors.amount && <span style={{ color: 'var(--color-danger-text)', fontSize: '0.8rem', display: 'block', marginTop: '4px' }}>{errors.amount}</span>}
        </div>
      </div>

      <div className="flex gap-md w-full">
        <div style={{ flex: 1 }}>
          <label style={labelStyle}>Date</label>
          <input 
            type="date" 
            style={{ ...inputStyle, borderColor: errors.date ? 'var(--color-danger-text)' : 'var(--color-border)' }}
            value={formData.date}
            onChange={(e) => setFormData({...formData, date: e.target.value})}
          />
        </div>
        <div style={{ flex: 1 }}>
          <label style={labelStyle}>Vendor</label>
          <input 
            type="text" 
            style={{ ...inputStyle, borderColor: errors.vendor ? 'var(--color-danger-text)' : 'var(--color-border)' }}
            value={formData.vendor}
            onChange={(e) => setFormData({...formData, vendor: e.target.value})}
            placeholder="E.g. Starbucks"
          />
        </div>
      </div>

      <div>
        <label style={labelStyle}>Category</label>
        <select 
          style={{ ...inputStyle, borderColor: errors.category ? 'var(--color-danger-text)' : 'var(--color-border)' }}
          value={formData.category}
          onChange={(e) => setFormData({...formData, category: e.target.value})}
        >
          <option value="">Select a category</option>
          <option value="Travel">Travel</option>
          <option value="Meals">Meals & Entertainment</option>
          <option value="Office Supplies">Office Supplies</option>
          <option value="Software">Software & Subscriptions</option>
        </select>
        {errors.category && <span style={{ color: 'var(--color-danger-text)', fontSize: '0.8rem', display: 'block', marginTop: '4px' }}>{errors.category}</span>}
      </div>

      <div>
        <label style={labelStyle}>Description (Optional)</label>
        <textarea 
          rows="2"
          style={inputStyle}
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          placeholder="What was this expense for?"
        />
      </div>

      <button type="submit" disabled={isSubmitting} className="btn btn-primary" style={{ marginTop: '0.5rem', justifyContent: 'center', opacity: isSubmitting ? 0.7 : 1, cursor: isSubmitting ? 'not-allowed' : 'pointer' }}>
        {isSubmitting ? 'Submitting...' : 'Submit Reimbursement'}
      </button>
    </form>
  );
}
