# Strategic Product Placement Analysis — Full Stack Application

Unveiling Sales Impact with Tableau Visualization, Flask REST APIs, MySQL, and Machine Learning.

## 1. Overview
This application turns the SmartInternz capstone project ("Strategic Product Placement Analysis: Unveiling Sales Impact with Tableau Visualization") into a production-style full-stack system: a Flask REST API + MySQL backend, a responsive HTML/CSS/JS frontend, a trained ML model that predicts sales volume for placement scenarios, and the original Tableau dashboards/stories for executive visualization.

## 2. Folder Structure
```
SPPA/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models/models.py     # SQLAlchemy ORM models
│   │   ├── routes/              # auth, data/analytics, prediction APIs
│   │   └── ml/                  # train_model.py, predict.py, saved model files
│   ├── config/settings.py       # DB + JWT configuration
│   ├── scripts/                 # init_db.py, eda.py
│   ├── run.py                   # entry point
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/ (api.js, auth.js, dashboard.js, predict.js)
├── database/
│   ├── schema.sql               # MySQL DDL
│   └── seed_data.py             # CSV -> MySQL loader
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── render.yaml              # cloud deploy config
├── docs/                        # Project_Documentation.pdf, diagrams
└── README.md
```

## 3. Tech Stack
| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (Chart.js) |
| Backend | Python, Flask, Flask-JWT-Extended, REST |
| Database | MySQL (SQLAlchemy ORM) |
| ML | scikit-learn RandomForestRegressor |
| Visualization | Tableau Public, Chart.js |
| Deployment | Docker, Docker Compose, Render/Cloud |

## 4. Setup (Local)

### 4.1 Database
```bash
mysql -u root -p < database/schema.sql
```

### 4.2 Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # edit DB credentials
python scripts/init_db.py   # creates tables (alternative to schema.sql)
python app/ml/train_model.py --file ../database/placement_data.csv
python database/seed_data.py --file ../database/placement_data.csv
python run.py
```
Backend runs at `http://127.0.0.1:5000`.

### 4.3 Frontend
Open `frontend/index.html` directly in a browser, or serve it:
```bash
cd frontend
python -m http.server 8080
```
Visit `http://127.0.0.1:8080`.

## 5. API Summary
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/register | Create user |
| POST | /api/auth/login | Get JWT token |
| GET  | /api/auth/me | Current user profile |
| GET  | /api/data/products | List products |
| GET  | /api/data/sales | List/filter sales records |
| GET  | /api/data/analytics/summary | Avg sales by category |
| GET  | /api/data/analytics/by-position | Avg sales by placement |
| GET  | /api/data/analytics/foot-traffic | Avg sales by foot traffic |
| POST | /api/predict/sales | ML sales volume prediction |
| GET  | /api/predict/history | User's prediction history |

## 6. Machine Learning Pipeline
1. **Preprocessing**: drop duplicates, fill missing values, label-encode categoricals (Position, Promotion, Foot Traffic, Demographics, Category, Seasonal).
2. **Model**: RandomForestRegressor (200 trees, depth 10).
3. **Evaluation**: MAE and R² printed after training.
4. **Serving**: `app/ml/predict.py` loads the pickled model + encoders and is called from `/api/predict/sales`.

## 7. Tableau Dashboards
The original Tableau Public dashboard and story (7 dashboard visuals + 3 story visuals) referenced in the project documentation remain the executive-facing analytics layer. Links are listed in `docs/Project_Documentation.pdf`.

## 8. Deployment
- **Local**: see Section 4.
- **Docker**: `cd deployment && docker-compose up --build`
- **GitHub**: `git init && git add . && git commit -m "Initial commit" && git remote add origin <repo-url> && git push -u origin main`
- **Cloud**: `deployment/render.yaml` (Render.com); equivalent steps apply for Azure/AWS/Heroku — set env vars, point build/start commands at `backend/`.

## 9. Team
Team ID: LTVIP2026TMIDS55759 — Neriyanuru Vedapriya, Pavan Kumar Pola, Masetty Suvarna Linga Lakshmi Kanth, Mula Gopi (KHIT, Guntur).
