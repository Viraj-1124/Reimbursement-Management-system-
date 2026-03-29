import { useState, useEffect } from 'react';
import DragDropArea from '../components/forms/DragDropArea';
import ExpenseForm from '../components/forms/ExpenseForm';
import Toast from '../components/common/Toast';
import { extractReceipt, submitExpense, getMyExpenses } from '../services/api';
import { FileText, Loader2, AlertTriangle, Clock, CheckCircle } from 'lucide-react';

export default function EmployeeHome() {
  const [file, setFile] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [ocrData, setOcrData] = useState(null);
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  
  const [expenses, setExpenses] = useState([]);
  
  useEffect(() => {
    // Load initial expenses list from Mock/Backend
    getMyExpenses().then(data => setExpenses(data || []));
  }, []);

  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile);
    setIsScanning(true);
    setOcrData(null);
    
    // Simulate OCR API Call (takes 2 seconds)
    try {
      const data = await extractReceipt(selectedFile);
      setOcrData(data);
    } catch (error) {
       console.error("OCR Failed", error);
    } finally {
      setIsScanning(false);
    }
  };

  const handleFormSubmit = async (formData) => {
    setIsSubmitting(true);
    try {
      await submitExpense(formData);
      setToastMessage("Expense submitted successfully!");
      // Reset form area for next submission
      setFile(null);
      setOcrData(null);
      
      // Refresh list to show new expense at the top
      const newData = await getMyExpenses();
      setExpenses([
        { id: Math.random(), vendor: formData.vendor, amount: parseFloat(formData.amount), status: "PENDING", date: formData.date },
        ...newData
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'APPROVED': return <span className="badge badge-success flex items-center gap-sm" style={{display:'inline-flex'}}><CheckCircle size={14}/> Approved</span>;
      case 'PENDING': return <span className="badge badge-warning flex items-center gap-sm" style={{display:'inline-flex'}}><Clock size={14}/> Pending</span>;
      case 'REJECTED': return <span className="badge badge-danger flex items-center gap-sm" style={{display:'inline-flex'}}><AlertTriangle size={14}/> Rejected</span>;
      default: return null;
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div className="mb-lg">
        <h2>Submit Reimbursement</h2>
        <p className="text-muted">Upload a receipt and let AI do the heavy lifting.</p>
      </div>
      
      <div className="flex gap-lg" style={{ flexWrap: 'wrap' }}>
        {/* LEFT COLUMN: Upload & Form */}
        <div style={{ flex: '2 1 500px' }} className="flex flex-col gap-lg">
          {!file ? (
            <div className="card">
              <DragDropArea onFileSelect={handleFileSelect} />
            </div>
          ) : (
            <div className="card">
              <div className="flex justify-between items-center mb-md" style={{ borderBottom: '1px solid var(--color-border)', paddingBottom: '1rem' }}>
                 <div className="flex items-center gap-sm" style={{ fontWeight: 600 }}>
                    <FileText size={18} className="text-muted"/> 
                    {file.name}
                 </div>
                 <button className="btn btn-outline" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }} onClick={() => { setFile(null); setOcrData(null); }}>
                   Remove & Start Over
                 </button>
              </div>

              {isScanning ? (
                <div className="flex flex-col items-center justify-center py-lg gap-md" style={{ minHeight: '300px' }}>
                  <Loader2 size={40} className="text-accent" style={{ animation: 'spin 1s linear infinite' }} />
                  <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
                  <p style={{ fontWeight: 600, color: 'var(--color-accent)' }}>AI is extracting receipt details...</p>
                </div>
              ) : (
                <ExpenseForm initialData={ocrData || {}} onSubmit={handleFormSubmit} isSubmitting={isSubmitting} />
              )}
            </div>
          )}
          
          {/* AI Hint Card (Shows up immediately after OCR returns a flag) */}
          {ocrData && ocrData.flags && ocrData.flags.length > 0 && (
            <div className="card" style={{ borderLeft: '4px solid var(--color-warning-text)', background: 'var(--color-warning-bg)' }}>
              <div className="flex gap-sm items-start">
                <AlertTriangle size={20} color="var(--color-warning-text)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div>
                  <h4 style={{ margin: '0 0 0.25rem 0', color: 'var(--color-warning-text)' }}>AI Policy Warning</h4>
                  <p style={{ margin: 0, fontSize: '0.9rem', color: '#854d0e', lineHeight: 1.4 }}>
                    <strong>{ocrData.flags[0]}.</strong> {ocrData.ai_recommendation} Please ensure your description clearly explains this expense to expedite approval.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: History */}
        <div style={{ flex: '1 1 300px' }}>
           <h3 className="mb-md">Recent Expenses</h3>
           <div className="flex flex-col gap-md">
             {expenses.length === 0 ? (
               <div className="card text-center text-muted">No recent expenses.</div>
             ) : (
               expenses.map(exp => (
                 <div key={exp.id} className="card flex justify-between items-center" style={{ padding: '1rem' }}>
                   <div>
                     <strong style={{ display: 'block', marginBottom: '4px' }}>{exp.vendor}</strong>
                     <span className="text-muted" style={{ fontSize: '0.85rem' }}>${exp.amount.toFixed(2)} | {exp.date}</span>
                   </div>
                   <div>{getStatusBadge(exp.status)}</div>
                 </div>
               ))
             )}
           </div>
        </div>
      </div>

      {toastMessage && <Toast message={toastMessage} onClose={() => setToastMessage('')} />}
    </div>
  );
}
