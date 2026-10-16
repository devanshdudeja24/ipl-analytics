# IPL Analytics and Win Predictor

An end-to-end data analytics project: data cleaning, exploratory analysis, SQL, a win-probability model, and an interactive Streamlit dashboard.

**Note:** this project uses a simulated dataset with the same structure as the Kaggle IPL data. The insights are for practice, not real cricket facts.

## Questions answered
- Does winning the toss help?
- Which teams win the most?
- Who are the top run scorers?
- How do scores change by season and by phase of the innings?
- Can we predict the chasing team's win probability during a chase?

## Tools
Python, pandas, Plotly, SQLite, scikit-learn, Streamlit

## Project structure
- `generate_data.py`: creates the practice dataset
- `notebooks/`: cleaning, EDA, SQL, and the model
- `sql/queries.sql`: SQL queries
- `models/`: the saved win predictor
- `app/app.py`: the Streamlit dashboard

## Model
Logistic Regression and Random Forest were trained on second-innings features (runs left, balls left, wickets left, run rates) and compared against a simple baseline. The data was split by match to avoid leakage.

## How to run
```bash
pip install -r requirements.txt
python -m streamlit run app/app.py
```

## Live demo
Coming soon