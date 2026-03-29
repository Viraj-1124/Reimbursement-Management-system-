export const MOCK_MODE = true;

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

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
  // TODO: Add real axios post
};

export const submitExpense = async (data) => {
  if (MOCK_MODE) {
    await delay(1000);
    return { success: true, id: Math.random().toString(36).substr(2, 9) };
  }
  // TODO: Add real axios post
};

export const getMyExpenses = async () => {
  if (MOCK_MODE) {
    await delay(500);
    return [
      { id: 1, vendor: "Starbucks", amount: 5.40, status: "APPROVED", date: "2023-10-25" },
      { id: 2, vendor: "Delta Airlines", amount: 142.50, status: "PENDING", date: "2023-10-24" }
    ];
  }
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
      },
      {
        id: "EXP-1205",
        employee_name: "Sarah Sales",
        vendor: "Starbucks",
        amount: 14.20,
        date: "2024-03-25",
        category: "Meals",
        status: "PENDING",
        receipt_preview: null,
        risk_score: 12,
        risk_level: "LOW",
        flags: [],
        ai_recommendation: "Low risk. Routine expense pattern detected."
      },
      {
        id: "EXP-1206",
        employee_name: "Michael Tech",
        vendor: "AWS Services",
        amount: 450.00,
        date: "2024-03-20",
        category: "Software",
        status: "PENDING",
        receipt_preview: null,
        risk_score: 45,
        risk_level: "MEDIUM",
        flags: ["Amount slightly above expected threshold for Software"],
        ai_recommendation: "Medium risk. Verify specific AWS instance usage."
      }
    ];
  }
};

export const submitApprovalDecision = async (id, decision, remarks) => {
  if (MOCK_MODE) {
    await delay(800);
    return { success: true, id, decision };
  }
};
