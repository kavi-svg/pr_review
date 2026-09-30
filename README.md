# GitHub Pull Request Risk Analysis Platform

A Django REST API for collecting pull-request metadata, extracting reproducible features, and comparing explainable rule-based, supervised ML, and replaceable LLM analysis. It is designed for research demos: ML performance is reported only from a labeled, held-out evaluation set.

## Architecture
- `backend/prs`: persistence, REST resources, GitHub collection, and the shared feature extractor.
- `backend/risk_engine`: rule, persisted-ML, and LLM provider-boundary scorers.
- `backend/ml`: CSV validation, preprocessing/training, evaluation, persisted prediction artifacts.
- `backend/evaluation`: saved held-out metrics endpoint.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
cd backend
python manage.py migrate
python manage.py runserver
```
SQLite is the default. Set `DATABASE_URL` (for example a PostgreSQL URL) for deployment. Set `GITHUB_TOKEN` to enable live collection; it is never returned by the API. `LLM_PROVIDER` and `LLM_API_KEY` enable a future provider adapter; without both, the API honestly returns `not_configured` rather than fabricating a score.

## APIs
- `GET /api/prs/`, `GET /api/prs/<id>/`
- `POST /api/prs/fetch/` with `{"repository":"owner/repo","pr_number":123}`
- `POST /api/prs/analyze/` with `{"pr_id":1,"model":"random_forest"}`
- `POST /api/prs/ml/train/` with `{"dataset_path":"/absolute/data.csv","model":"random_forest"}`
- `POST /api/prs/ml/predict/` with `{"features":{...},"model":"random_forest"}`
- `GET /api/evaluation/`

## ML data and training
The CSV must include `is_risky` (binary) and every feature in `ml/features.py`: numeric PR metrics plus `pr_size_category`. Labels must come from documented historical outcomes (for example reverts, bug links, or defined hotfix events); GitHub metadata alone does **not** create those labels. A small demonstration dataset may be generated from transparently labeled records, but it is not research evidence.

```bash
cd backend
python -m ml.train /absolute/path/historical_prs.csv --model random_forest
# alternatives: logistic_regression, gradient_boosting, xgboost (optional install)
python manage.py test
python manage.py check
```
Training performs a stratified held-out split, fits preprocessing within the pipeline to avoid leakage, writes a joblib artifact and actual metrics to `ml/artifacts/`. Prediction loads an artifact and never retrains.

## Limitations
GitHub collection requires credentials and API availability. The initial LLM interface intentionally has no provider-specific implementation. Rule factors are heuristic; model feature importance, when available, is associative and not causal. Reliable evaluation requires sufficiently sized, time-aware, real labeled historical data.
