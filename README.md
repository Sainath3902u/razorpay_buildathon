# RevenueOS — AI Revenue Intelligence

RevenueOS is a full-stack revenue intelligence app for the Razorpay Buildathon. It analyzes merchant payment/customer data and identifies **Recover, Prevent, and Grow** opportunities with recommended actions.

## Tech Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python
- **Data:** Pandas, NumPy
- **AI:** Opportunity detection engine + Agentic AI action workflow

## System Design

```text
Merchant Dataset
      ↓
Next.js Frontend
      ↓
FastAPI Backend
      ↓
Read → Map Columns → Normalize
      ↓
Opportunity Detection Engine
      ↓
┌──────────┬──────────┬──────────┐
│ RECOVER  │ PREVENT  │   GROW   │
└──────────┴──────────┴──────────┘
      ↓
Priority + Probability + Expected Value
      ↓
Agentic AI
      ↓
Dashboard / Analytics / Opportunities
```

## Agentic AI

RevenueOS is designed to move beyond a passive dashboard.

The agent follows:

```text
Observe → Analyze → Decide → Recommend → Act → Evaluate
```

Example:

```text
Repeated payment failures
        ↓
Detect revenue risk
        ↓
Estimate impact
        ↓
Prioritize opportunity
        ↓
Recommend alternate payment
        ↓
Execute approved recovery action
```

The agentic layer can later support autonomous payment retries, customer communication, payment-method switching, and outcome-based learning.

## Core Features

- Upload CSV / XLS / XLSX / JSON datasets
- Automatic schema detection and column mapping
- Revenue opportunity detection
- Recover / Prevent / Grow classification
- Priority and expected-value scoring
- Explainable opportunity details
- Dataset-driven Dashboard and Analytics
- Recommended next-best actions
- Agentic AI workflow foundation

## How to Run the App in VS Code

### 1. Open the project

Open the `razorpay_buildathon` folder in VS Code.

### 2. Install dependencies

Open **Terminal 1**:

```bash
cd backend
pip install -r requirements.txt
```

Open **Terminal 2**:

```bash
cd frontend
npm install
```

### 3. Start the backend

In Terminal 1:

```bash
cd ..
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Check:

```text
http://localhost:8000/health
```

Expected:

```json
{"status":"healthy"}
```

### 4. Start the frontend

In Terminal 2:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

Make sure `frontend/.env.local` contains:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Use the app

```text
Upload Dataset
→ Backend analyzes the data
→ View Overview
→ View Opportunities
→ Click an opportunity for details
→ View Analytics
```

### Quick Run

After dependencies are installed, use two VS Code terminals:

**Terminal 1**
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2**
```bash
cd frontend
npm run dev
```

## Main API

```text
POST /api/upload
GET  /api/opportunities/{dataset_id}
GET  /health
```

## Opportunity Data

Each opportunity can contain:

```text
Opportunity ID
Category
Opportunity Type
Customer ID
Amount at Risk
Probability
Expected Value
Priority
Reason
Recommended Action
Recovery Eligibility
Recovery Reason
Source Detector
```

## Demo Flow

```text
Upload Dataset
   ↓
Backend analyzes data
   ↓
Opportunities generated
   ↓
Dashboard shows revenue impact
   ↓
Analytics shows distribution
   ↓
Click opportunity
   ↓
View reason + recommended action
```

## Vision

**RevenueOS turns payment signals into revenue actions — and evolves from analytics into an agentic revenue system.**
