export default function EmployeeHome() {
  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div className="flex justify-between items-center mb-lg">
        <div>
          <h2>Employee Dashboard</h2>
          <p className="text-muted">Submit an expense and track history.</p>
        </div>
        <button className="btn btn-accent">Submit New Expense</button>
      </div>
      
      <div className="card">
         <p className="text-muted text-center" style={{ padding: '2rem 0' }}>No recent expenses found.</p>
      </div>
    </div>
  );
}
