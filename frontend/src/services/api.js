export const MOCK_MODE = true;

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

export const extractReceipt = async (base64Image) => {
  if (MOCK_MODE) {
    await delay(1500); // simulate OCR scanning delay
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

export const getMyExpenses = async () => {
  if (MOCK_MODE) {
    await delay(500);
    return [
      { id: 1, vendor: "Starbucks", amount: 5.40, status: "APPROVED", date: "2023-10-25" }
    ];
  }
};
