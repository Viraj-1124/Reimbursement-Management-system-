import { ShieldCheck, Users, Settings, Save, Edit3 } from 'lucide-react';
import { useState } from 'react';

export default function AdminHome() {
  const [isEditing, setIsEditing] = useState(false);
  const [autoApproval, setAutoApproval] = useState("$50.00");
  const [multiplier, setMultiplier] = useState("2.0x");

  const toggleEdit = () => {
    if (isEditing) {
      // simulate save
      alert("System rules saved successfully!");
    }
    setIsEditing(!isEditing);
  };

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
               <input 
                 type="text" 
                 value={autoApproval}
                 onChange={(e) => setAutoApproval(e.target.value)}
                 disabled={!isEditing} 
                 style={{ width: '100%', padding: '0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)', backgroundColor: isEditing ? '#fff' : 'var(--color-background)', color: isEditing ? '#000' : 'var(--color-text-muted)', marginTop: '0.4rem', fontWeight: 500 }} 
               />
             </div>
             <div>
               <label className="text-muted" style={{ fontSize: '0.85rem', fontWeight: 600 }}>WARNING MULTIPLIER (VS AVERAGE)</label>
               <input 
                 type="text" 
                 value={multiplier}
                 onChange={(e) => setMultiplier(e.target.value)}
                 disabled={!isEditing} 
                 style={{ width: '100%', padding: '0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)', backgroundColor: isEditing ? '#fff' : 'var(--color-background)', color: isEditing ? '#000' : 'var(--color-text-muted)', marginTop: '0.4rem', fontWeight: 500 }} 
               />
             </div>
             <button 
               className={isEditing ? "btn btn-primary" : "btn btn-outline"} 
               onClick={toggleEdit} 
               style={{ marginTop: '0.5rem', display: 'flex', justifyContent: 'center' }}
             >
                {isEditing ? <><Save size={16}/> Save Settings</> : <><Edit3 size={16}/> Edit System Rules</>}
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
               <span style={{ cursor: 'pointer', padding: '0.2rem 0.5rem', borderRadius: '12px', fontSize: '0.75rem', backgroundColor: '#e2e8f0', color: 'var(--color-text-muted)', border: '1px solid #cbd5e1' }}>Reports to: Sam ▼</span>
             </div>
             <div className="flex justify-between items-center" style={{ padding: '0.75rem 1rem', backgroundColor: 'var(--color-background)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
               <div>
                  <strong style={{ display: 'block' }}>Sarah Sales</strong>
                  <span className="text-muted" style={{ fontSize: '0.8rem' }}>Account Executive</span>
               </div>
               <span style={{ cursor: 'pointer', padding: '0.2rem 0.5rem', borderRadius: '12px', fontSize: '0.75rem', backgroundColor: '#e2e8f0', color: 'var(--color-text-muted)', border: '1px solid #cbd5e1' }}>Reports to: Sam ▼</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
