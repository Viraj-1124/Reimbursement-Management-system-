# SmartReimburse AI - Backend Demo Guide

This document outlines the architecture of the SmartReimburse AI backend and provides a step-by-step guide to get the API running locally.

---

## 🏗️ Backend Architecture Overview

The backend is built using **FastAPI**, **SQLAlchemy** (PostgreSQL), and **Pydantic**. It is designed to expose a high-performance REST API while seamlessly orchestrating fraud detection through its AI engine.

### Core Modules & Responsibilities

1. `backend/main.py`: The entry point. Initializes the FastAPI application, maps API routers, configures `CORSMiddleware`, and ensures the database tables are built.
2. `backend/core/database.py`: Establishes the PostgreSQL database connection and provides the injection dependency (`get_db`) to safely supply database sessions to all endpoints.
3. `backend/core/models.py`: Defines the SQLAlchemy ORM schema (Users, Expenses, Approvals, Companies).
4. `backend/core/schemas.py`: Pydantic models for strictly validating incoming HTTP requests and formatting outgoing JSON payload shapes.
5. `backend/core/auth.py`: Handles JWT (JSON Web Token) generation, bcrypt password hashing, and Role-Based Access Control (RBAC) via the `get_current_user` dependency logic.
6. `backend/core/users.py`: Business logic for managing users, handling employee creation, and assigning organizational structures (managers).
7. `backend/core/expenses.py`: Manages the lifecycle of an expense claim and manually invokes the `fraud_detection` models whenever a new receipt is submitted.
8. `backend/core/workflow.py`: Manages the dynamic multi-step approval chain. It ensures claims correctly route to the correct manager for sign-off.
9. `backend/core/routes.py`: The API controllers. Secures HTTP endpoints (`/auth/login`, `/expenses/submit`, etc.) and manages request/response translations via the above modules.
10. `backend/ai_engine/`: Dedicated AI logic module. Intercepts submitted expenses to run complex anomaly detection (e.g., duplicate receipts, out-of-policy date ranges, and standard deviation comparisons).
11. `backend/seed.py`: A vital bootstrap script to populate the database with a working Admin, Manager, and Employee for the frontend demo.

---

## 🚀 How to Run the Backend

Follow these exact steps to deploy and connect your local environment.

### 1. Database Configuration
You must have an active PostgreSQL database. 
1. Open `backend/core/database.py`.
2. Locate the `DATABASE_URL` variable at the top of the file.
3. Replace the placeholder connection string with your own PostgreSQL credentials. 

*Example:*
`DATABASE_URL = "postgresql://postgres:root%40123@localhost:5432/reimbursement_db"`

### 2. Environment Setup & Dependency Installation
It is highly recommended to use a virtual environment before installing the requirements to prevent dependency conflicts with your global python install.

**Open your terminal at the root of the project:**

```bash
# 1. Create a Virtual Environment
python -m venv venv

# 2. Activate the Virtual Environment
# For Windows (PowerShell):
.\venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

# 3. Install Core API Dependencies
pip install -r backend/requirements.txt

# 4. Install AI Engine Dependencies
pip install -r backend/ai_engine/requirements_ai.txt
```

### 3. Seed the Database
Before running the frontend application, run the seed script to automatically build your tables and inject standard demo users into the system. This allows you to immediately log in!

```bash
python backend/seed.py
```
*Depending on the script, you now have three demo accounts (password is `password` for all):*
- `admin@test.com` (Admin Role)
- `manager@test.com` (Manager Role)
- `employee@test.com` (Employee Role)

### 4. Start the Server
Once everything is configured and seeded, boot up the FastAPI Uvicorn server:

```bash
uvicorn backend.main:app --reload
```
You should see it successfully bind to `http://127.0.0.1:8000`. The frontend React application (running on Vite at port `5173`) will cleanly connect to this port automatically using the configured `CORSMiddleware`.

### 5. API Documentation
Once the server is running, you can view the natively auto-generated Swagger UI interactive documentation natively in your browser by visiting:
**[http://localhost:8000/docs](http://localhost:8000/docs)**
