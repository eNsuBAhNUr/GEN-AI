# Natural Language to SQL Query Interface (FastAPI + SQLite + Vanilla JS)

## Overview

This project provides a simple web interface where users can ask natural language questions about sales data and receive SQL query results from a backend SQLite database.

---

## Features

- Takes user input in plain English (e.g., "Top 5 selling products")
- Maps predefined questions to SQL queries
- Executes those queries against a local SQLite database
- Returns formatted tabular results to the frontend
- Frontend and backend communicate using a REST API (FastAPI)
- Built-in request logging
- Lightweight UI with refresh, clear, and exit controls

---

## Dataset

Three CSV files were used to create the SQLite database:

1. **Product-Level Eligibility Table**
2. **Product-Level Ad Sales and Metrics**
3. **Product-Level Total Sales and Metrics**

These were parsed and converted into SQL tables at the beginning of the project setup.

---

## Architecture

- Frontend (index.html + JS):
  - User inputs a question
  - Calls backend API using `fetch`
  - Displays result in a formatted text area
  - Includes optional request logging and clearing
  
- Backend (FastAPI - main.py):
  - Endpoint: `/ask`
  - Accepts JSON payload with `question`
  - Maps the question to a SQL query using a rule-based mapping
  - Executes the query using `sqlite3`
  - Returns the result in a structured format (rows + columns)

---

## Research/Experimental Work

- A parallel prototype was built in **Google Colab** using the **Gemini Pro API** to generate SQL queries dynamically from raw user input.
- The Gemini model was used to:
  - Translate natural questions into executable SQL
  - Handle generic or novel queries beyond predefined mappings
  - Generate plots from SQL results using `matplotlib`
- However, Gemini and plotting are **not integrated** in this final FastAPI version due to local execution constraints and stability issues.

---

## Future Scope

- Integrate live LLM-to-SQL translation for dynamic query handling
- Add persistent logging and history
- Support downloadable CSV reports or charts
- Include optional Gemini API integration via secure API keys

---

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite3
- Vanilla JavaScript (Frontend)

---

## Run the App

```bash
uvicorn main:app --reload
