import { CheckCircle2, X } from 'lucide-react';
import { useEffect } from 'react';

export default function Toast({ message, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div style={{
      position: 'fixed',
      bottom: '2rem',
      right: '2rem',
      background: 'var(--color-surface)',
      borderLeft: '4px solid var(--color-success-text)',
      boxShadow: 'var(--shadow-lg)',
      padding: '1rem',
      borderRadius: 'var(--radius-md)',
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem',
      zIndex: 1000,
      animation: 'slideIn 0.3s ease-out forwards'
    }}>
      <style>{`
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
      <CheckCircle2 color="var(--color-success-text)" />
      <span style={{ fontWeight: 500 }}>{message}</span>
      <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', marginLeft: '1rem' }}>
        <X size={16} className="text-muted" />
      </button>
    </div>
  );
}
