import { useState, useEffect } from 'react';
import { fetchPendingApprovals, submitApprovalDecision } from '../services/api';
import PendingQueueTable from '../components/dashboard/PendingQueueTable';
import AIAnalysisPanel from '../components/dashboard/AIAnalysisPanel';
import Modal from '../components/common/Modal';
import Toast from '../components/common/Toast';
import { Loader2, FileText, Check, X } from 'lucide-react';

export default function ManagerHome() {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [remarks, setRemarks] = useState("");
  const [toastMsg, setToastMsg] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchPendingApprovals();
      setApprovals(data || []);
    } catch(e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const highRiskCount = approvals.filter(a => a.risk_level === 'HIGH').length;

  const handleDecision = async (decision) => {
    if (!selectedItem) return;
    setIsSubmitting(true);
    try {
      await submitApprovalDecision(selectedItem.id, decision, remarks);
      setToastMsg(`Expense ${decision.toLowerCase()} successfully.`);
      // Optimistically remove from list
      setApprovals(prev => prev.filter(a => a.id !== selectedItem.id));
      setSelectedItem(null);
      setRemarks("");
    } catch(err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header & Stats */}
      <div className="flex justify-between items-end mb-lg">
        <div>
          <h2>Manager Approvals Queue</h2>
          <p className="text-muted">Review pending reimbursements flagged by AI.</p>
        </div>
        <div className="flex gap-md">
          <div className="card text-center" style={{ padding: '0.75rem 1.5rem', minWidth: '120px' }}>
             <h3 style={{ margin: 0, fontSize: '1.5rem', color: 'var(--color-primary)' }}>{approvals.length}</h3>
             <span className="text-muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>PENDING</span>
          </div>
          <div className="card text-center" style={{ padding: '0.75rem 1.5rem', minWidth: '120px', borderBottom: highRiskCount > 0 ? '4px solid var(--color-danger-text)' : '1px solid var(--color-border)' }}>
             <h3 style={{ margin: 0, fontSize: '1.5rem', color: highRiskCount > 0 ? 'var(--color-danger-text)' : 'var(--color-primary)' }}>{highRiskCount}</h3>
             <span className="text-muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>HIGH RISK</span>
          </div>
        </div>
      </div>
      
      {/* Queue Table */}
      {loading ? (
        <div className="flex justify-center items-center py-lg"><Loader2 className="animate-spin text-accent" size={32} /></div>
      ) : (
        <PendingQueueTable items={approvals} onRowClick={(item) => { setSelectedItem(item); setRemarks(""); }} />
      )}

      {/* Detail Modal */}
      <Modal isOpen={!!selectedItem} onClose={() => { if(!isSubmitting) setSelectedItem(null); }} title={`Review Expense: ${selectedItem?.id}`} maxWidth="900px">
        {selectedItem && (
          <div className="flex gap-lg" style={{ marginTop: '0.5rem', flexWrap: 'wrap' }}>
            {/* Left: Receipt Preview */}
            <div style={{ flex: '1 1 350px' }}>
              <div style={{ background: 'var(--color-background)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)', height: '100%', minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
                 <div style={{ padding: '0.75rem', borderBottom: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 600 }}>
                   <FileText size={16} className="text-muted"/> Receipt Document
                 </div>
                 <div style={{ flex: 1, padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#e2e8f0', flexDirection: 'column', gap: '1rem' }}>
                   <div style={{ padding: '2rem', background: '#cbd5e1', borderRadius: 'var(--radius-md)', width: '80%', height: '70%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                     <span style={{ color: '#64748b', fontWeight: 600 }}>Secure Document Viewer</span>
                   </div>
                 </div>
              </div>
            </div>

            {/* Right: Details & Process */}
            <div style={{ flex: '1 1 400px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
               <div className="flex justify-between items-start">
                  <div>
                    <h2 style={{ margin: '0 0 0.25rem 0' }}>{selectedItem.currency || 'USD'} {selectedItem.amount.toFixed(2)}</h2>
                    {selectedItem.converted_amount && selectedItem.converted_amount !== selectedItem.amount && (
                       <p style={{ margin: 0, fontWeight: 600, color: 'var(--color-primary)' }}>
                         Converted: {selectedItem.converted_amount.toFixed(2)} (Company Match)
                       </p>
                    )}
                    <p style={{ margin: '0.25rem 0 0 0', color: 'var(--color-text-muted)' }}>{selectedItem.vendor} | {selectedItem.category}</p>
                    <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.9rem' }}>Submitted by <strong>{selectedItem.employee_name}</strong> on {selectedItem.date}</p>
                  </div>
               </div>

               <AIAnalysisPanel 
                 riskLevel={selectedItem.risk_level} 
                 score={selectedItem.risk_score} 
                 flags={selectedItem.flags} 
                 recommendation={selectedItem.ai_recommendation} 
               />

               <div style={{ marginTop: 'auto' }}>
                 <label style={{ display: 'block', fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.25rem' }}>Manager Remarks (Optional)</label>
                 <textarea 
                   rows="2" 
                   value={remarks}
                   onChange={(e) => setRemarks(e.target.value)}
                   disabled={isSubmitting}
                   style={{ width: '100%', padding: '0.75rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', fontFamily: 'inherit', resize: 'vertical' }}
                   placeholder="Add a note for the employee or accounting..."
                 />
                 
                 <div className="flex gap-md" style={{ marginTop: '1rem' }}>
                   <button 
                     onClick={() => handleDecision('REJECTED')} 
                     disabled={isSubmitting}
                     className="btn btn-outline flex items-center justify-center gap-sm" 
                     style={{ flex: 1, color: 'var(--color-danger-text)', borderColor: 'var(--color-border)', opacity: isSubmitting ? 0.7 : 1 }}
                   >
                     <X size={18} /> Reject
                   </button>
                   <button 
                     onClick={() => handleDecision('APPROVED')} 
                     disabled={isSubmitting}
                     className="btn btn-accent flex items-center justify-center gap-sm" 
                     style={{ flex: 2, opacity: isSubmitting ? 0.7 : 1 }}
                   >
                     {isSubmitting ? <Loader2 size={18} className="animate-spin" /> : <Check size={18} />} 
                     {isSubmitting ? 'Processing...' : 'Approve Expense'}
                   </button>
                 </div>
               </div>
            </div>
          </div>
        )}
      </Modal>

      {toastMsg && <Toast message={toastMsg} onClose={() => setToastMsg('')} />}
    </div>
  );
}
