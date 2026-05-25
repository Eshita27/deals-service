# 🏷️ Polyglot Commerce — Deals API

## 📌 Overview
The **Deals API** is a high-performance service responsible for calculating dynamic marketing campaigns, customer targeted tiers, and real-time global promotional flash discount overrides.

* **Technology Stack:** Python 3.11+ | FastAPI | MongoDB
* **Architectural Pattern:** Flat Service-Repository Pattern
* **Downstream Integration:** Serves requests routed exclusively via the SHP API Orchestrator (BFF).

---

## 📂 Project Directory Architecture
```text
deals-api/
├── app/
│   ├── api/v1/          # HTTP Router endpoints & Request schemas
│   ├── core/            # App initialization, database drivers, & global configs
│   ├── models/          # MongoDB document object structures
│   ├── repositories/    # Direct database serialization logic
│   ├── services/        # Core discount calculations & Waterfall rules engine
│   └── main.py          # Application entry-point
├── .github/
│   └── PR_Template.md   # Quality assurance pull request schema
├── requirements.txt     # Python dependency configuration manifest
└── README.md

🚀 Local Development Setup
1. Initialize Virtual Environment
Bash
python -m venv .venv
source .venv/scripts/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
2. Required Environment Configurations (.env)
Code snippet
PORT=8082
MONGO_URI=mongodb://localhost:27017/deals_db
GLOBAL_OVERRIDE_SECRET=my-dev-secret-token
3. Spin Up Application locally
Bash
uvicorn app.main:app --reload --port 8082
Interactive API Docs: Navigate to http://localhost:8082/docs once running.