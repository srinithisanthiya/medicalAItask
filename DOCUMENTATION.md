# MIRA Health Prediction — End-to-End Project Documentation

Simple guide to understand **how the full project works** — frontend, backend, REST API, SQLite, and AI/ML prediction.

---

## 1. What This Project Does

A **health prediction web app** where you:

1. Enter patient details + blood test values
2. Click **Save & Predict**
3. System calls **AI/ML API** → generates health risk **Remarks**
4. Data is saved in **SQLite database**
5. You can **Create, Read, Update, Delete** (CRUD) all records

---

## 2. Big Picture — How Everything Connects

```
USER (Browser)
    │
    │  HTML form + Bootstrap UI + JavaScript
    ▼
MAIN BACKEND (FastAPI — Port 8000)
    │  • Validates data
    │  • REST API /api/patients
    │  • CRUD functions
    │
    ├──► SQLite Database (data/patients.db)
    │
    └──► ML API (FastAPI — Port 8001)
              • RandomForest model
              • Returns health risk + remarks
```

**Simple flow when you click Save:**

```
Form → JavaScript → POST /api/patients → Backend validates
  → Calls ML API /predict → Gets remarks → Saves to SQLite → Shows in table
```

---

## 3. Project Folder Structure

```
medicalAI/
├── frontend/           ← What user sees (HTML, CSS, JS)
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
│
├── backend/            ← Main API server (Port 8000)
│   ├── main.py         ← Routes + serves frontend
│   ├── models.py       ← Database table design
│   ├── schemas.py      ← Input/output validation
│   ├── crud.py         ← Create, Read, Update, Delete
│   ├── database.py     ← SQLite connection
│   ├── ml_client.py    ← Calls ML API
│   └── config.py       ← Settings (DB URL, ML URL)
│
├── ml_api/             ← AI/ML service (Port 8001)
│   ├── main.py         ← /predict endpoint
│   ├── predictor.py    ← Model prediction logic
│   ├── train_model.py  ← Train the ML model
│   └── model/          ← Saved model file
│
├── data/
│   └── patients.db     ← SQLite database (auto-created)
│
├── requirements.txt    ← Python libraries
└── .env.example        ← Config template
```

---

## 4. Frontend (HTML + Bootstrap + JavaScript)

### 4.1 Files

| File | What it does |
|------|--------------|
| `index.html` | Page layout — form (left) + table (right) |
| `css/style.css` | Custom colors and spacing |
| `js/app.js` | All logic — validation, API calls, table update |

### 4.2 HTML — Form Fields

| Field | Type | User enters? |
|-------|------|--------------|
| Full Name | text | Yes |
| Date of Birth | date | Yes |
| Email | email | Yes |
| Glucose | number | Yes |
| Haemoglobin | number | Yes |
| Cholesterol | number | Yes |
| Remarks | — | **No — AI generates this** |

### 4.3 Bootstrap — What it gives us

- **Navbar** — app title bar
- **Cards** — form and table containers
- **Form controls** — styled inputs
- **Buttons** — Save, Edit, Delete
- **Alerts** — green success / red error messages
- **Table** — patient records list
- **Validation styles** — red border on invalid fields (`is-invalid`)

Loaded from CDN — no install needed.

### 4.4 JavaScript Functions (`app.js`)

| Function | Purpose | CRUD |
|----------|---------|------|
| `loadPatients()` | GET all records → fill table | **Read** |
| `savePatient()` | POST (new) or PUT (edit) → save | **Create / Update** |
| `editPatient(id)` | GET one record → fill form | Read (for edit) |
| `deletePatient(id)` | DELETE record | **Delete** |
| `validateForm()` | Check email, DOB, numbers | Validation |
| `getFormPayload()` | Build JSON from form | Helper |
| `renderPatients()` | Draw table rows | Helper |
| `resetForm()` | Clear form after save | Helper |
| `setEditMode()` | Switch form to Edit mode | Helper |
| `showAlert()` | Show success/error message | Helper |

### 4.5 Frontend Validation Rules

| Field | Rule |
|-------|------|
| Full Name | Min 2 characters |
| Date of Birth | Required, not in future |
| Email | Valid format (`name@domain.com`) |
| Glucose, Hb, Cholesterol | Must be numbers |

---

## 5. Backend (Python + FastAPI)

### 5.1 Module → Function Map

#### `main.py` — API Routes

| Route Function | HTTP | Endpoint | Action |
|----------------|------|----------|--------|
| `serve_frontend()` | GET | `/` | Show web page |
| `list_patients()` | GET | `/api/patients` | List all |
| `read_patient()` | GET | `/api/patients/{id}` | Get one |
| `create_patient()` | POST | `/api/patients` | Create + AI predict |
| `update_patient()` | PUT | `/api/patients/{id}` | Update + re-predict |
| `delete_patient()` | DELETE | `/api/patients/{id}` | Delete |

#### `crud.py` — Database Operations

| Function | What it does |
|----------|--------------|
| `get_patients(db)` | SELECT all patients from SQLite |
| `get_patient(db, id)` | SELECT one patient by ID |
| `create_patient(db, data, remarks)` | INSERT new patient + remarks |
| `update_patient(db, id, data, remarks)` | UPDATE patient + new remarks |
| `delete_patient(db, id)` | DELETE patient by ID |

#### `schemas.py` — Validation (Pydantic)

| Class | Used for |
|-------|----------|
| `PatientCreate` | POST request body validation |
| `PatientUpdate` | PUT request body validation |
| `PatientResponse` | JSON response to frontend |

#### `models.py` — Database Table

| Class | Maps to |
|-------|---------|
| `Patient` | `patients` table in SQLite |

#### `database.py` — Connection

| Function/Item | Purpose |
|---------------|---------|
| `engine` | SQLite connection |
| `SessionLocal` | Database session factory |
| `get_db()` | Provides DB session to each API route |

#### `ml_client.py` — AI Integration

| Function | Purpose |
|----------|---------|
| `fetch_health_prediction()` | POST to ML API → returns remarks string |

#### `config.py` — Settings

| Setting | Default | Purpose |
|---------|---------|---------|
| `database_url` | `sqlite:///./data/patients.db` | DB file path |
| `ml_api_url` | `http://127.0.0.1:8001` | ML service URL |
| `ml_api_timeout_seconds` | `30` | API call timeout |

---

## 6. REST API Endpoints (Full Details)

### Main App — `http://127.0.0.1:8000`

Swagger docs: **http://127.0.0.1:8000/docs**

---

### GET `/api/patients` — List All (Read)

**Response `200`:**
```json
[
  {
    "id": 1,
    "full_name": "Jane Doe",
    "date_of_birth": "1990-05-15",
    "email": "jane@example.com",
    "glucose": 145.0,
    "haemoglobin": 11.5,
    "cholesterol": 220.0,
    "remarks": "AI Assessment: High health risk...",
    "created_at": "2026-06-14T10:00:00",
    "updated_at": "2026-06-14T10:00:00"
  }
]
```

---

### GET `/api/patients/{id}` — Get One (Read)

**Response `200`:** Single patient object  
**Response `404`:** Patient not found

---

### POST `/api/patients` — Create

**Request body:**
```json
{
  "full_name": "Jane Doe",
  "date_of_birth": "1990-05-15",
  "email": "jane@example.com",
  "glucose": 145.0,
  "haemoglobin": 11.5,
  "cholesterol": 220.0
}
```

**What happens inside:**
1. Pydantic validates input
2. `fetch_health_prediction()` → ML API
3. `create_patient()` → SQLite INSERT
4. Return patient with remarks

**Response `201`:** Created patient with remarks  
**Response `422`:** Validation error  
**Response `502`:** ML API not running

---

### PUT `/api/patients/{id}` — Update

**Request body:** Same as POST  
**Response `200`:** Updated patient (new remarks)  
**Response `404`:** Not found

---

### DELETE `/api/patients/{id}` — Delete

**Response `204`:** Deleted (no body)  
**Response `404`:** Not found

---

### ML API — `http://127.0.0.1:8001`

Swagger docs: **http://127.0.0.1:8001/docs**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check if model is loaded |
| POST | `/predict` | Get health risk prediction |

**POST `/predict` request:**
```json
{
  "date_of_birth": "1990-05-15",
  "glucose": 145.0,
  "haemoglobin": 11.5,
  "cholesterol": 220.0
}
```

**Response:**
```json
{
  "remarks": "AI Assessment: High health risk (72.5% model confidence)...",
  "risk_level": "High",
  "confidence": 0.725
}
```

---

## 7. CRUD Flow — Step by Step

### CREATE
```
User fills form → validateForm() → POST /api/patients
→ Backend validates → ML API /predict → INSERT SQLite
→ 201 response → Table refreshes → Remarks visible
```

### READ
```
Page load / Refresh → GET /api/patients
→ SELECT from SQLite → JSON array → renderPatients() → Table shown
```

### UPDATE
```
Click Edit → GET /api/patients/{id} → Form filled
→ User changes value → PUT /api/patients/{id}
→ ML API re-predicts → UPDATE SQLite → New remarks in table
```

### DELETE
```
Click Delete → Confirm → DELETE /api/patients/{id}
→ DELETE from SQLite → Row removed from table
```

---

## 8. SQLite Database

### 8.1 Basic Info

| Item | Value |
|------|-------|
| Type | SQLite 3 (file-based) |
| File | `data/patients.db` |
| ORM | SQLAlchemy |
| Auto-create | Yes, on first app start |

### 8.2 Table: `patients`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto increment) |
| `full_name` | VARCHAR(120) | Patient name |
| `date_of_birth` | DATE | DOB |
| `email` | VARCHAR(255) | Email (indexed) |
| `glucose` | FLOAT | Blood glucose mg/dL |
| `haemoglobin` | FLOAT | Haemoglobin g/dL |
| `cholesterol` | FLOAT | Cholesterol mg/dL |
| `remarks` | TEXT | AI-generated health remark |
| `created_at` | DATETIME | When record was created |
| `updated_at` | DATETIME | When record was last updated |

### 8.3 SQL Equivalent

```sql
CREATE TABLE patients (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     VARCHAR(120) NOT NULL,
    date_of_birth DATE NOT NULL,
    email         VARCHAR(255) NOT NULL,
    glucose       FLOAT NOT NULL,
    haemoglobin   FLOAT NOT NULL,
    cholesterol   FLOAT NOT NULL,
    remarks       TEXT NOT NULL DEFAULT '',
    created_at    DATETIME NOT NULL,
    updated_at    DATETIME NOT NULL
);
```

### 8.4 View Data

```powershell
# Python
python -c "import sqlite3; c=sqlite3.connect('data/patients.db'); print(c.execute('SELECT id, full_name, remarks FROM patients').fetchall())"
```

---

## 9. AI/ML Prediction

### 9.1 How It Works

| Step | What happens |
|------|--------------|
| 1 | User saves patient data |
| 2 | Backend sends blood values to ML API |
| 3 | ML API calculates age from DOB |
| 4 | RandomForest model predicts: Low / Moderate / High |
| 5 | Builds readable remarks text |
| 6 | Backend saves remarks in database |

### 9.2 ML Files

| File | Purpose |
|------|---------|
| `train_model.py` | Train model from public diabetes dataset |
| `predictor.py` | Load model + run prediction |
| `main.py` | Expose `/predict` as REST API |
| `model/health_risk_model.joblib` | Saved trained model |

### 9.3 Train Model (first time only)

```powershell
python -m ml_api.train_model
```

### 9.4 Model Input → Output

**Input:** age, glucose, haemoglobin, cholesterol  
**Output:** risk_level (Low/Moderate/High), confidence %, remarks text

---

## 10. Python Libraries (`requirements.txt`)

### Web & API

| Library | Version | Why we use it |
|---------|---------|---------------|
| **fastapi** | 0.115.6 | Build REST API, auto validation, Swagger docs |
| **uvicorn** | 0.34.0 | Run FastAPI server |
| **python-multipart** | 0.0.20 | Form data support |

### Database

| Library | Version | Why we use it |
|---------|---------|---------------|
| **sqlalchemy** | 2.0.36 | Connect to SQLite, ORM for Patient table |

### Validation & Config

| Library | Version | Why we use it |
|---------|---------|---------------|
| **pydantic** | 2.10.3 | Validate request/response JSON |
| **pydantic-settings** | 2.7.0 | Load `.env` config |

### HTTP Client

| Library | Version | Why we use it |
|---------|---------|---------------|
| **httpx** | 0.28.1 | Backend calls ML API asynchronously |

### Machine Learning

| Library | Version | Why we use it |
|---------|---------|---------------|
| **scikit-learn** | 1.6.0 | RandomForest classifier |
| **pandas** | 2.2.3 | Load training dataset |
| **numpy** | 2.2.1 | Numeric arrays for model |
| **joblib** | 1.4.2 | Save/load trained model file |

---

## 11. How to Run

```powershell
cd c:\medicalAI
.\venv\Scripts\activate
pip install -r requirements.txt
python -m ml_api.train_model

# Terminal 1
uvicorn ml_api.main:app --reload --port 8001

# Terminal 2
uvicorn backend.main:app --reload --port 8000
```

Open: **http://127.0.0.1:8000**

---

## 12. Quick Reference — For Demo

| Topic | One-line explanation |
|-------|----------------------|
| **Frontend** | HTML form + Bootstrap UI + JavaScript fetch API |
| **Backend** | FastAPI REST API with 5 CRUD endpoints |
| **Database** | SQLite file stores all patient records permanently |
| **AI/ML** | Separate ML API predicts health risk → fills Remarks |
| **Create** | Form → API → ML → SQLite → table |
| **Read** | GET API → SQLite → table |
| **Update** | Edit → API → ML re-predict → SQLite update |
| **Delete** | DELETE API → remove from SQLite |
| **Validation** | Frontend JS + Backend Pydantic — email, DOB, numbers |

---

## 13. HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | GET, PUT success |
| 201 | Created | POST success |
| 204 | No Content | DELETE success |
| 404 | Not Found | Patient ID missing |
| 422 | Validation Error | Bad email, future DOB, etc. |
| 502 | Bad Gateway | ML API not reachable |
| 503 | Service Unavailable | ML model not trained |

---

*MIRA Health Prediction — Task 1 Documentation*
