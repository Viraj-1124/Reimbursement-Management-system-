import { ShieldCheck, Users, Settings } from 'lucide-react';

export default function AdminHome() {
  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div className="mb-lg">
        <h2>Admin Settings</h2>
        <p className="text-muted">Manage system rules and organizational structure.</p>
      </div>

      <div className="flex gap-lg" style={{ flexWrap: 'wrap' }}>
        {/* Rules Card */}
        <div className="card" style={{ flex: '1 1 300px' }}>
          <div className="flex items-center gap-sm mb-md pb-sm border-b">
            <ShieldCheck className="text-accent" size={20} />
            <h3 style={{ margin: 0, fontSize: '1.1rem' }}>Global Approval Rules</h3>
          </div>
          <div className="flex flex-col gap-md">
             <div>
               <label className="text-muted" style={{ fontSize: '0.85rem', fontWeight: 600 }}>AUTO-APPROVAL THRESHOLD</label>
               <input type="text" value="$50.00" disabled style={{ width: '100%', padding: '0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)', backgroundColor: 'var(--color-background)', color: 'var(--color-text-muted)', marginTop: '0.4rem', fontWeight: 500 }} />
             </div>
             <div>
               <label className="text-muted" style={{ fontSize: '0.85rem', fontWeight: 600 }}>WARNING MULTIPLIER (VS AVERAGE)</label>
               <input type="text" value="2.0x" disabled style={{ width: '100%', padding: '0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)', backgroundColor: 'var(--color-background)', color: 'var(--color-text-muted)', marginTop: '0.4rem', fontWeight: 500 }} />
             </div>
             <button className="btn btn-outline" disabled style={{ marginTop: '0.5rem', cursor: 'not-allowed', color: 'var(--color-text-muted)', display: 'flex', justifyContent: 'center' }}>
                <Settings size={16} /> Edit System Rules
             </button>
          </div>
        </div>

        {/* User Assignment Card */}
        <div className="card" style={{ flex: '2 1 400px' }}>
          <div className="flex items-center gap-sm mb-md pb-sm border-b">
            <Users className="text-accent" size={20} />
            <h3 style={{ margin: 0, fontSize: '1.1rem' }}>Organization Chart</h3>
          </div>
          <div className="flex flex-col gap-sm">
             <div className="flex justify-between items-center" style={{ padding: '0.75rem 1rem', backgroundColor: 'var(--color-background)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
               <div>
                  <strong style={{ display: 'block' }}>Alex Employee</strong>
                  <span className="text-muted" style={{ fontSize: '0.8rem' }}>Software Engineer</span>
               </div>
               <span className="badge badge-warning" style={{ backgroundColor: '#e2e8f0', color: 'var(--color-text-muted)', border: '1px solid #cbd5e1' }}>Reports to: Sam</span>
             </div>
             <div className="flex justify-between items-center" style={{ padding: '0.75rem 1rem', backgroundColor: 'var(--color-background)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
               <div>
                  <strong style={{ display: 'block' }}>Sarah Sales</strong>
                  <span className="text-muted" style={{ fontSize: '0.8rem' }}>Account Executive</span>
               </div>
               <span className="badge badge-warning" style={{ backgroundColor: '#e2e8f0', color: 'var(--color-text-muted)', border: '1px solid #cbd5e1' }}>Reports to: Sam</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
