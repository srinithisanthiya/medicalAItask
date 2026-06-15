# MIRA Health Prediction — 20 Minute Demo Video Script

Use this while recording.** Speak naturally — you don't need to read word-for-word.

**Before recording:** Start both servers, open http://127.0.0.1:8000

```powershell
# Terminal 1
cd c:\medicalAI
.\venv\Scripts\activate
uvicorn ml_api.main:app --port 8001

# Terminal 2
cd c:\medicalAI
.\venv\Scripts\activate
uvicorn backend.main**:app --port 8000
```

---

## TIMING OVERVIEW

| Time | Topic |
|------|--------|
| 0:00 – 2:00 | Intro + what the project does |
| 2:00 – 4:00 | How the full project works (flow) |
| 4:00 – 7:00 | Frontend — HTML, Bootstrap, JavaScript |
| 7:00 – 10:00 | Backend — Python, FastAPI, REST API, modules |
| 10:00 – 12:00 | Database — SQLite |
| 12:00 – 14:00 | AI/ML — prediction service |
| 14:00 – 18:00 | Live demo — CRUD + validation |
| 18:00 – 20:00 | Challenges + GitHub + closing |

---

## PART 1 — INTRO (0:00 – 2:00)

**[Screen: Browser on http://127.0.0.1:8000]**

**SAY:**

> "Hello, I'm **[Your Full Name]**. This is my **Task 1 submission** for the Junior AI/ML Developer position — **MIRA Health Prediction**.
>
> This is a **health prediction web application**. Users can enter patient details and blood test results — glucose, haemoglobin, and cholesterol. When we save a record, the system **automatically calls an AI/ML service** and generates a **health risk remark**.
>
> The app supports full **CRUD** — Create, Read, Update, and Delete — with **input validation** and **permanent storage** in a database.
>
> I built this using **HTML, Bootstrap, and JavaScript** for the frontend, **Python and FastAPI** for the backend REST API, **SQLite** for the database, and a **separate ML API** for health predictions."

---

## PART 2 — HOW THE PROJECT WORKS (2:00 – 4:00)

**[Screen: Project folder in VS Code OR explain verbally]**

**SAY:**

> "Let me explain **how everything connects**.
>
> There are **three main parts**:
>
> **1. Frontend** — what you see in the browser. The form and the patient table.
>
> **2. Backend** — Python FastAPI server on **port 8000**. It handles API requests, validates data, saves to the database, and calls the ML service.
>
> **3. ML API** — a separate Python FastAPI service on **port 8001**. This is the **external AI/ML API** required by the task. It takes blood test values and returns a health risk prediction.
>
> **Flow when user clicks Save:**
> 1. Browser sends data to backend API
> 2. Backend validates the data
> 3. Backend calls ML API `/predict`
> 4. ML API returns remarks
> 5. Backend saves patient + remarks in SQLite
> 6. Frontend shows the record in the table
>
> So the user only sees one website, but **two Python services** work together behind the scenes."

---

## PART 3 — FRONTEND (4:00 – 7:00)

**[Screen: frontend folder — index.html, css/style.css, js/app.js]**

**SAY:**

> "Now the **frontend**.
>
> I used **HTML** for the page structure — the form fields, the patient table, and the layout.
>
> For styling I used **Bootstrap 5** — a CSS framework from CDN. It gives me a clean navbar, cards, buttons, form validation styles, and a responsive layout.
>
> For logic I used **vanilla JavaScript** in **`app.js`** — no React or Vue.
>
> **What JavaScript does:**
> - Validates the form — email format, date not in future, numbers only
> - Calls the backend using **`fetch()`** — GET, POST, PUT, DELETE
> - Renders the patient table dynamically
> - Handles Edit mode — loads a record back into the form
> - Shows success and error alerts
>
> **[Open index.html briefly]**
> Fields: Full Name, Date of Birth, Email, Glucose, Haemoglobin, Cholesterol. Remarks come from AI — user does not type them.
>
> **[Open app.js — validateForm and savePatient]**
> `validateForm()` checks input on the client. `savePatient()` sends JSON to `/api/patients`. On edit it uses PUT instead of POST.
>
> Frontend and backend are **separated by REST API** — the UI doesn't touch the database directly."

---

## PART 4 — BACKEND (7:00 – 10:00)

**[Screen: backend folder — main.py, models.py, schemas.py, crud.py, ml_client.py]**

**SAY:**

> "The **backend** is built with **Python** and **FastAPI**.
>
> FastAPI is a modern Python framework for building **REST APIs**. It gives automatic validation, JSON responses, and interactive API docs at `/docs`.
>
> **Backend modules:**
>
> | File | Purpose |
> |------|---------|
> | **main.py** | Main app — all API routes, serves frontend |
> | **models.py** | Database table — Patient model |
> | **schemas.py** | Request/response validation with Pydantic |
> | **crud.py** | Create, Read, Update, Delete operations |
> | **database.py** | SQLite connection and session |
> | **ml_client.py** | Calls the external ML API |
> | **config.py** | Settings — database URL, ML API URL |
>
> **[Open http://127.0.0.1:8000/docs]**
> This is **Swagger UI** — auto-generated API documentation.
>
> **REST API endpoints:**
>
> | Method | Endpoint | Action |
> |--------|----------|--------|
> | GET | `/api/patients` | List all patients |
> | GET | `/api/patients/{id}` | Get one patient |
> | POST | `/api/patients` | Create + AI predict |
> | PUT | `/api/patients/{id}` | Update + re-predict |
> | DELETE | `/api/patients/{id}` | Delete record |
>
> **Validation** uses **Pydantic** — valid email, DOB not in future, blood values numeric. Failed validation returns **422 error**.
>
> On **Create** and **Update**, backend calls ML API first, then saves remarks with the patient."

---

## PART 5 — DATABASE — SQLite (10:00 – 12:00)

**[Screen: models.py or data/patients.db]**

**SAY:**

> "For **persistent storage** I used **SQLite**.
>
> SQLite is a **file-based database** — no separate server. File: **`data/patients.db`**.
>
> I use **SQLAlchemy** — Python ORM — to map classes to tables.
>
> **Table:** `patients`
>
> **Columns:** id, full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks, created_at, updated_at
>
> Table is **created automatically** on first app start.
>
> **Why SQLite?** Simple, no extra install, data **persists after refresh**.
>
> **[Refresh browser]**
> Records stay after refresh — saved in SQLite, not browser memory."

---

## PART 6 — AI/ML PREDICTION (12:00 – 14:00)

**[Screen: ml_api folder — main.py, predictor.py, train_model.py]**

**SAY:**

> "The task requires an **external AI/ML API**. I built a **separate ML service** — main backend calls it over HTTP.
>
> **ML API on port 8001.**
>
> **Endpoints:**
> - `GET /health` — check model loaded
> - `POST /predict` — blood values in, health risk out
>
> **[Open http://127.0.0.1:8001/docs if possible]**
>
> **How ML works:**
> 1. **RandomForest** model trained with **scikit-learn**
> 2. Public diabetes dataset for training
> 3. Features: age, glucose, haemoglobin, cholesterol
> 4. Output: **Low, Moderate, or High** risk
> 5. Model file: **`health_risk_model.joblib`**
>
> **Train command:** `python -m ml_api.train_model`
>
> ML API builds a **remarks** string like: *'AI Assessment: High health risk, elevated glucose...'*
>
> Stored in **Remarks** column — user never types it."

---

## PART 7 — LIVE DEMO (14:00 – 18:00)

**[Screen: http://127.0.0.1:8000]**

### 7A — CREATE (14:00 – 15:00)

**DO:** Fill form → **Save & Predict**

**SAY:**

> "Live demo — **Create**. Name, DOB, email, glucose 145, haemoglobin 11.5, cholesterol 220. Save & Predict. Backend validated, called ML API, saved to SQLite. Green message and **AI Remarks** in the table."

---

### 7B — READ (15:00 – 15:30)

**DO:** Point at table → **Refresh**

**SAY:**

> "**Read** — all patients here. Refresh loads from database via GET `/api/patients`."

---

### 7C — UPDATE (15:30 – 16:30)

**DO:** **Edit** → change glucose to 95 → **Update & Re-predict**

**SAY:**

> "**Update** — Edit, change glucose, save. ML API called again — **remarks update**."

---

### 7D — DELETE (16:30 – 17:00)

**DO:** **Delete** → confirm

**SAY:**

> "**Delete** — removed from database and table."

---

### 7E — VALIDATION (17:00 – 18:00)

**DO:** Show 3 errors

**SAY:**

> "**Validation:**
> 1. Bad email `notanemail` — error
> 2. Future DOB 2030 — error
> 3. Non-numeric glucose `abc` — error
> Invalid data never reaches the database."

---

## PART 8 — CLOSING (18:00 – 20:00)

**SAY:**

> "**Challenges:**
> 1. Two services must run — app + ML API
> 2. Model must be trained first
> 3. Remarks must regenerate on update
>
> **Tech stack:**
> - Frontend: HTML, Bootstrap 5, JavaScript
> - Backend: Python, FastAPI, Pydantic, SQLAlchemy
> - Database: SQLite
> - AI/ML: scikit-learn, separate FastAPI ML service
>
> **GitHub** link in my email. README has setup steps.
>
> **Thank you. I'm [Your Name].**"

---

## QUICK REFERENCE CARD

```
INTRO     → Name, project, CRUD + AI remarks
FLOW      → Browser → Backend 8000 → ML 8001 → SQLite
FRONTEND  → HTML + Bootstrap + JS (fetch, validate)
BACKEND   → FastAPI, 5 endpoints, Pydantic
DATABASE  → SQLite, patients table
ML        → RandomForest, /predict, auto remarks
DEMO      → Create → Read → Update → Delete → Validation
CLOSE     → Challenges, GitHub, thank you
```

---

## LIBRARIES CHEAT SHEET

| Layer | Libraries |
|-------|-----------|
| Frontend | HTML5, Bootstrap 5.3, JavaScript |
| Backend | fastapi, uvicorn, pydantic, sqlalchemy, httpx |
| Database | SQLite |
| ML | scikit-learn, pandas, numpy, joblib |

---

*Good luck! Speak slowly, show screen clearly, pause after each action.*
