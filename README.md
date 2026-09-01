# Health Risk Prediction & Prevention

This repository contains a Python Flask backend that serves health risk predictions based on machine learning models, plus a modern **Next.js + Tailwind** frontend UI for a premium dashboard experience.

---

## 🧠 Backend (Flask)

The backend runs on **http://localhost:5000** and exposes a `POST /predict` endpoint:

- Uses pre-trained scikit-learn models stored under `models/*.pkl`
- Accepts JSON input with health metrics
- Returns risk predictions and recommended prevention tips

### Run backend

```bash
python app.py
```

---

## 🎨 Frontend (Next.js)

The frontend is located in `frontend/` and is built with:

- Next.js (App Router)
- Tailwind CSS
- Framer Motion (animations)
- Recharts (risk charts)

### Setup

1) From the root, install dependencies:

```bash
cd frontend
npm install
```

2) Create `.env.local` from the example (optional):

```bash
cp .env.local.example .env.local
```

3) Run the dev server:

```bash
npm run dev
```

The UI will run on **http://localhost:3000** and will call the backend on **http://localhost:5000**.

---

## 🚀 Notes

- If you’d prefer to keep using the Flask-rendered UI, that is still available at `http://localhost:5000/`.
- To switch to the Next.js UI, start the Next server and ensure the Flask backend is running.
