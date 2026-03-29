export const MOCK_MODE = false;

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

const API_BASE = 'http://localhost:8000';

const getHeaders = () => {
  const token = localStorage.getItem('auth_token');
  return {
    'Authorization': `Bearer ${token}`
  };
};

export const extractReceipt = async (file) => {
  if (MOCK_MODE) {
    await delay(2000); // 2-second simulated OCR scanning
    return {
      amount: 142.50,
      date: "2023-10-24",
      vendor: "Delta Airlines",
      confidence: 0.94,
      flags: ["Date is 6 months old"],
      risk_score: 85,
      ai_recommendation: "High risk due to old date."
    };
  }
  
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/expenses/extract`, {
    method: 'POST',
    headers: getHeaders(), // Don't set Content-Type for FormData
    body: formData
  });
  if (!response.ok) throw new Error('Failed to extract receipt');
  return response.json();
};

export const submitExpense = async (data) => {
  if (MOCK_MODE) {
    await delay(1000);
    return { success: true, id: Math.random().toString(36).substr(2, 9) };
  }
  
  const payload = {
    amount: parseFloat(data.amount) || 0,
    currency: "USD",
    category: data.category || "General",
    description: data.notes || "Receipt submission",
    date: data.date || new Date().toISOString().split('T')[0]
  };

  const response = await fetch(`${API_BASE}/expenses/submit`, {
    method: 'POST',
    headers: { 
      ...getHeaders(),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  
  if (!response.ok) throw new Error('Failed to submit expense');
  return response.json();
};

export const getMyExpenses = async () => {
  if (MOCK_MODE) {
    await delay(500);
    return [
      { id: 1, vendor: "Starbucks", amount: 5.40, status: "APPROVED", date: "2023-10-25" },
      { id: 2, vendor: "Delta Airlines", amount: 142.50, status: "PENDING", date: "2023-10-24" }
    ];
  }
  
  const response = await fetch(`${API_BASE}/expenses/my`, {
    headers: getHeaders(),
  });
  if (!response.ok) throw new Error('Failed to fetch expenses');
  
  const data = await response.json();
  return data.map(exp => ({
    id: exp.id,
    vendor: exp.category || 'General',
    amount: exp.amount,
    status: exp.status,
    date: exp.date
  }));
};

export const fetchPendingApprovals = async () => {
  if (MOCK_MODE) {
    await delay(600);
    return [
      {
        id: "EXP-1204",
        employee_name: "Alex Employee",
        vendor: "Delta Airlines",
        amount: 142.50,
        date: "2023-10-24",
        category: "Travel",
        status: "PENDING",
        receipt_preview: null,
        risk_score: 85,
        risk_level: "HIGH",
        flags: ["Date is 6 months old", "Amount is 2.1x higher than average"],
        ai_recommendation: "High risk. Recommend manager review regarding policy on old receipts."
      }
    ];
  }
  
  const response = await fetch(`${API_BASE}/workflow/pending`, {
    headers: getHeaders()
  });
  if (!response.ok) throw new Error('Failed to fetch pending approvals');
  return response.json();
};

export const submitApprovalDecision = async (id, decision, remarks) => {
  if (MOCK_MODE) {
    await delay(800);
    return { success: true, id, decision };
  }
  
  const response = await fetch(`${API_BASE}/workflow/approve?approval_id=${id}`, {
    method: 'POST',
    headers: { 
      ...getHeaders(),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ decision, comments: remarks || "" })
  });
  
  if (!response.ok) throw new Error('Failed to submit decision');
  return response.json();
};
