import { ChevronRight } from 'lucide-react';

export default function PendingQueueTable({ items, onRowClick }) {
  
  const getRiskBadge = (level) => {
    switch(level) {
      case 'HIGH': return <span className="badge badge-danger">High Risk</span>;
      case 'MEDIUM': return <span className="badge badge-warning">Medium Risk</span>;
      default: return <span className="badge badge-success">Low Risk</span>;
    }
  };

  if (!items || items.length === 0) {
    return <div className="card text-center text-muted" style={{ padding: '3rem' }}>No pending approvals. Amazing!</div>;
  }

  return (
    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead style={{ background: 'var(--color-background)', borderBottom: '1px solid var(--color-border)' }}>
          <tr>
            <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--color-text-muted)' }}>ID</th>
            <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--color-text-muted)' }}>Employee</th>
            <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--color-text-muted)' }}>Vendor / Category</th>
            <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--color-text-muted)' }}>Amount</th>
            <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--color-text-muted)' }}>AI Assessment</th>
            <th style={{ padding: '1rem' }}></th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id} 
                onClick={() => onRowClick(item)}
                style={{ borderBottom: '1px solid var(--color-border)', cursor: 'pointer', transition: 'background 0.2s' }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'var(--color-background)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
            >
              <td style={{ padding: '1rem', fontWeight: 500 }}>{item.id}</td>
              <td style={{ padding: '1rem' }}>
                <div style={{ fontWeight: 500 }}>{item.employee_name}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>{item.date}</div>
              </td>
              <td style={{ padding: '1rem' }}>
                <div>{item.vendor}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>{item.category}</div>
              </td>
              <td style={{ padding: '1rem' }}>
                <div style={{ fontWeight: 600 }}>{item.currency || 'USD'} {item.amount.toFixed(2)}</div>
                {item.converted_amount && item.converted_amount !== item.amount && (
                  <div style={{ fontSize: '0.8rem', color: 'var(--color-primary)' }}>
                    {item.converted_amount.toFixed(2)} (Default)
                  </div>
                )}
              </td>
              <td style={{ padding: '1rem' }}>{getRiskBadge(item.risk_level)}</td>
              <td style={{ padding: '1rem', textAlign: 'right' }}>
                <ChevronRight size={18} className="text-muted" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
