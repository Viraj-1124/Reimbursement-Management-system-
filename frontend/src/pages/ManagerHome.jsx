export default function ManagerHome() {
  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div className="mb-lg">
        <h2>Manager Approvals Queue</h2>
        <p className="text-muted">Review pending reimbursements flagged by AI.</p>
      </div>
      
      <div className="card" style={{ padding: '1.5rem' }}>
        <div className="flex justify-between items-center">
          <div>
            <strong>Expense #1204 - Delta Airlines</strong>
            <p className="text-muted" style={{ margin: '0.25rem 0' }}>Submitted by Alex Employee</p>
          </div>
          <div>
            <span className="badge badge-warning">High Risk AI Flag</span>
          </div>
        </div>
      </div>
    </div>
  );
}
