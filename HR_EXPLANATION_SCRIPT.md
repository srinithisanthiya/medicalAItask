# MIRA Health Prediction — HR Explanation Script

**Use this when explaining your project to HR or in your demo video.**  
Speak naturally — you don't need to read word-for-word.

**Before recording:** Start both servers, open http://127.0.0.1:8000

---

## PART 1 — TASK REQUIREMENTS (30–45 sec)

**SAY:**

> "The task asked me to build a **health prediction application** using Python as the backend.
>
> It must collect patient details — **Full Name, Date of Birth, Email, Glucose, Haemoglobin, Cholesterol** — and generate **Remarks using an external AI/ML API**.
>
> It must support full **CRUD** — Create, Read, Update, Delete.
>
> It needs a **user-friendly UI**, **input validation**, **persistent storage**, and **integration with an AI/ML or Health API** for prediction.
>
> I designed my solution to meet **every requirement** — nothing was skipped."

---

## PART 2 — WHY I CHOSE THESE TOOLS (1–2 min)

**SAY:**

> "I chose tools that are **simple, practical, and suitable for a real backend + AI project**.
>
> **Frontend — HTML, Bootstrap, JavaScript**
> - The task allows any frontend — HTML/CSS/Bootstrap is simple and fast to build
> - Bootstrap gives a clean, professional UI without heavy setup
> - JavaScript `fetch()` is enough for CRUD — no need for React for this scope
>
> **Backend — Python + FastAPI**
> - The task requires **Python**
> - FastAPI is modern, fast, and perfect for **REST APIs**
> - Built-in validation with Pydantic — email, date, numbers checked automatically
> - Auto API docs at `/docs` — easy to test and show in demo
>
> **Database — SQLite**
> - Task asks for persistent storage
> - SQLite is file-based — no extra database server to install
> - Perfect for demo and submission — data persists after refresh
>
> **AI/ML — Separate FastAPI service + scikit-learn**
> - Task requires calling an **external AI/ML API**
> - I built a **separate ML service** on port 8001 — backend calls it like a real external API
> - Used **RandomForest** from scikit-learn — trained on a public health dataset
> - This shows I understand **API integration**, not just putting ML inside one file
>
> So overall: simple UI, strong backend, real database, and proper external ML integration."

---

## PART 3 — PROJECT STRUCTURE (1 min)

**[Screen: Show project folder in VS Code]**

**SAY:**

> "My project has a clear folder structure:
>
> **`frontend/`** — what the user sees
> - `index.html` — form and patient table
> - `css/style.css` — custom styling
> - `js/app.js` — validation and API calls
>
> **`backend/`** — main application on port 8000
> - `main.py` — REST API routes
> - `models.py` — database table design
> - `schemas.py` — input validation
> - `crud.py` — Create, Read, Update, Delete logic
> - `database.py` — SQLite connection
> - `ml_client.py` — calls the ML API
> - `config.py` — settings like DB URL and ML API URL
>
> **`ml_api/`** — external AI/ML service on port 8001
> - `main.py` — `/predict` endpoint
> - `predictor.py` — model prediction logic
> - `train_model.py` — trains the ML model
> - `model/` — saved trained model file
>
> **`data/`** — SQLite database file `patients.db`
>
> **`requirements.txt`** — all Python libraries
>
> Each folder has one clear responsibility — frontend, backend, ML, and data."

---

## PART 4 — LIBRARIES (30 sec)

**SAY:**

> "Main Python libraries I used:
> - **FastAPI + Uvicorn** — REST API and server
> - **SQLAlchemy** — connect to SQLite and manage tables
> - **Pydantic** — validate email, DOB, blood values
> - **httpx** — backend calls ML API over HTTP
> - **scikit-learn, pandas, numpy, joblib** — train and run the ML model
>
> Frontend uses **Bootstrap 5** from CDN — no extra install needed."

---

## PART 5 — BASIC WORKFLOW (1 min)

**SAY:**

> "When a user opens the app at port 8000, they see a form and a patient table.
>
> **Create flow:**
> 1. User enters patient details and clicks **Save & Predict**
> 2. JavaScript validates the form
> 3. Frontend sends **POST** to `/api/patients`
> 4. Backend validates again with Pydantic
> 5. Backend calls **ML API** `/predict` with blood test values
> 6. ML API returns health risk and **Remarks**
> 7. Backend saves everything in **SQLite**
> 8. Frontend shows the new record in the table with AI remarks
>
> **Read** — page load or Refresh calls **GET** `/api/patients` and loads all records
>
> **Update** — Edit loads one record, user changes values, **PUT** sends update, ML re-predicts, remarks update
>
> **Delete** — **DELETE** removes record from database and table
>
> So the workflow is: **UI → REST API → ML API → Database → UI**."

---

## PART 6 — LIVE DEMO (follow DEMO_VIDEO_SCRIPT.md)

After explaining structure, show live:
1. Create → AI remarks appear
2. Read → table list
3. Update → remarks change
4. Delete → record removed
5. Validation → email, DOB, numeric errors

---

## PART 7 — CLOSING (15 sec)

**SAY:**

> "I chose this stack because it is **simple to run, easy to explain, and covers all task requirements** — CRUD, validation, SQLite storage, and external AI/ML integration in a clean, maintainable structure.
>
> Code and setup steps are on GitHub. Thank you for reviewing my submission."

---

## QUICK CHEAT SHEET (keep beside you)

| HR asks | You say |
|---------|---------|
| **Requirements** | CRUD, 7 fields, validation, SQLite, external ML API, UI |
| **Why FastAPI?** | Python required, REST API, validation, auto docs |
| **Why Bootstrap?** | Clean UI quickly, task allows any frontend |
| **Why SQLite?** | Persistent storage, no extra DB setup |
| **Why separate ML API?** | Task needs external AI/ML API integration |
| **Structure** | frontend / backend / ml_api / data |
| **Workflow** | Form → API → ML → DB → Table |
| **Libraries** | fastapi, sqlalchemy, pydantic, httpx, scikit-learn |

---

## RECOMMENDED ORDER FOR HR DEMO

| Step | What to do |
|------|------------|
| 1 | Explain task requirements |
| 2 | Explain why you chose each tool |
| 3 | Show folder structure in VS Code |
| 4 | Explain workflow (before live demo) |
| 5 | Live demo — Create, Read, Update, Delete, Validation |
| 6 | Optional — show http://127.0.0.1:8000/docs |
| 7 | Closing + GitHub link |

---

## ONE-PARAGRAPH VERSION (if HR wants short answer)

> "The task required a Python health prediction app with CRUD, validation, SQLite storage, and external AI/ML integration. I used FastAPI for the REST backend, Bootstrap and JavaScript for the frontend, SQLite for persistent storage, and a separate scikit-learn ML service as the external API. When a user saves a record, the backend validates data, calls the ML API for health risk remarks, saves to SQLite, and displays results in the UI. The project is split into frontend, backend, ml_api, and data folders for clear separation of concerns."

---

*Good luck with your HR demo!*
