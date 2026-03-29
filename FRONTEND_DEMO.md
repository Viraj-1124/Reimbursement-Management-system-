# SmartReimburse AI - Frontend Demo Guide

This document contains the final polish output for the hackathon judges, offering a copy-pasteable README section and a bulletproof 3-minute demo script.

---

## Add This to your README.md

### Frontend Architecture

The SmartReimburse UI is built natively using **Vite + React**, optimized for performance and a highly polished "Enterprise Light" aesthetic. 

- **State Management:** Lightweight React Context (`AppContext.jsx`) ensures fast, dependency-free mock role switching and session handling.
- **Styling Strategy:** Custom CSS utilizing native CSS Variables (e.g., `var(--color-primary)`) to ensure pixel-perfect fidelity without wrestling framework defaults. 
- **Icons:** Powered by `lucide-react` for beautifully crisp, scalable graphics.
- **Failsafe Mocks:** Employs a robust `api.js` abstraction layer that permits running the full AI orchestration flow 100% offline via a simple `MOCK_MODE` toggle. This protects against any unexpected backend API failures during the live pitch.

#### Quick Start

1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Open `http://localhost:5173`

---

## 3-Minute Golden Path Demo Script

**Goal:** Wow the judges with speed, explainable AI, and flawless UX.

### 1. Act I: The Employee (1 min)
*Action: Open `http://localhost:5173` and click `[Login as Employee]`.*

"Reimbursements are typically slow and error-prone. Look at how easy we make it for the employee. I simply drag my Delta receipt into this dropzone."

*Action: Drop any receipt image into the box. Let the 2-second AI scan animation run.*

"Our OCR automatically kicks in. It correctly parses the vendor and amount, confidently autofilling the data. But notice here: the AI flagged a policy warning right on the submission form, immediately reminding the employee that this receipt is out of our standard policy window."

*Action: Pick `Travel` from the category dropdown, and click `Submit`. The success Toast appears.*

"The employee corrects it or adds a note, hits submit, and they are done."

### 2. Act II: The Manager (1.5 min)
*Action: Click `Logout` in the navbar, then click `[Login as Manager]`.*

"Now, let's look at the manager's perspective. I have 3 pending claims, but my dashboard instantly alerts me that 1 of them is HIGH RISK."

*Action: Point at the High Risk summary count. Then click the top row in the queue.*

"When I open this high-risk claim, our app isolates the uploaded receipt right next to a dedicated Explainable AI risk panel. I don't have to guess why this was flagged. The AI explicitly calculates the risk score and lists exactly what tripped the model: the date is 6 months old and the amount is unusually high for this category."

*Action: Type 'Out of policy window, please review guidelines' into the textarea. Click `Reject`.*

"I drop a quick remark and reject it. Our system securely processes the decision instantly. No back-and-forth email chains required."

### 3. Act III: The Admin Rules (30s)
*Action: Click `Logout`, then click `[Login as Admin]`.*

"Underpinning all of this are dynamic organizational rules set by Finance. The Admin configuration enforces the baseline thresholds and multipliers we just saw the AI evaluate against. It ensures the whole company stays compliant automatically. Thank you!"
