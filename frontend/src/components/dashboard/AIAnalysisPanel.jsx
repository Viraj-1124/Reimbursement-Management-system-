import { ShieldAlert, ShieldCheck, Shield } from 'lucide-react';

export default function AIAnalysisPanel({ riskLevel, score, flags, recommendation }) {
  let indicatorColor = 'var(--color-success-text)';
  let bgColor = 'var(--color-success-bg)';
  let Icon = ShieldCheck;
  let title = "Low Risk";

  if (riskLevel === 'MEDIUM') {
    indicatorColor = 'var(--color-warning-text)';
    bgColor = 'var(--color-warning-bg)';
    Icon = Shield;
    title = "Medium Risk Analysis";
  } else if (riskLevel === 'HIGH') {
    indicatorColor = 'var(--color-danger-text)';
    bgColor = 'var(--color-danger-bg)';
    Icon = ShieldAlert;
    title = "High Risk Detected";
  }

  return (
    <div style={{ border: `1px solid ${indicatorColor}`, background: bgColor, borderRadius: 'var(--radius-md)', padding: '1rem' }}>
      <div className="flex justify-between items-start" style={{ marginBottom: '0.5rem' }}>
        <div className="flex items-center gap-sm">
          <Icon color={indicatorColor} size={20} />
          <strong style={{ color: indicatorColor }}>{title}</strong>
        </div>
        <span style={{ fontWeight: 600, color: indicatorColor }}>Score: {score}/100</span>
      </div>
      
      <p style={{ fontSize: '0.9rem', margin: '0.5rem 0', color: '#334155' }}>
        <strong>AI Recommendation:</strong> {recommendation}
      </p>

      {flags && flags.length > 0 && (
        <div style={{ marginTop: '0.75rem' }}>
          <strong style={{ fontSize: '0.85rem', color: indicatorColor }}>Flags:</strong>
          <ul style={{ margin: '0.25rem 0 0 0', paddingLeft: '1.25rem', fontSize: '0.85rem', color: '#475569' }}>
            {flags.map((flag, idx) => (
              <li key={idx} style={{ marginBottom: '0.25rem' }}>{flag}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
