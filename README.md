# Data Science Salaries Analysis

Exploratory analysis of the DS Salaries dataset using a Jupyter notebook, plus a Streamlit dashboard.

## Contents

- `ds_salaries.ipynb`: Primary analysis notebook with data loading, cleaning, and visuals.
- `ds_salaries.csv`: Source dataset used by the notebook.
- `app.py`: Streamlit dashboard app.
- `requirements.txt`: Dashboard dependencies.

## Getting started

1. Create and activate a Python virtual environment.
2. Install dependencies used in the notebook or dashboard.
3. Open the notebook and run cells top to bottom, or run the dashboard.

Example setup (macOS/Linux):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app.py
```

## Notes

- If you add new packages in the notebook, update the requirements file above.
- For large outputs, consider clearing notebook output before committing.
