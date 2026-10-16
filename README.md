# Retail Sales Data Pipeline

## Project Overview

A Python-based ETL (Extract, Transform, Load) data engineering project that processes retail sales transactions from CSV files, validates and transforms records, stores cleaned data in a SQLite database, and generates sales analytics.

The project demonstrates a complete ETL workflow using Python, SQL, data validation, file handling, and logging.

## Technologies Used

- **Python 3** – Data processing and pipeline orchestration
- **SQLite** – Relational database storage
- **SQL** – Data aggregation and analysis
- **CSV** – Raw and processed data storage
- **pathlib** – File and directory management
- **decimal** – Accurate monetary calculations
- **logging** – Pipeline execution tracking

## Project Structure

```text
retail-sales-data-pipeline/
│
├── data/
│   ├── raw/
│   │   └── sales.csv
│   ├── processed/
│   │   ├── clean_sales.csv
│   │   └── rejected_sales.csv
│   └── retail_sales.db
│
├── logs/
│   └── pipeline.log
│
├── src/
│   ├── extract_sales.py
│   ├── load_sales.py
│   ├── sales_analytics.py
│   ├── logger_config.py
│   └── pipeline_runner.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## ETL Pipeline Workflow

### 1. Extract

Reads retail sales transaction data from `data/raw/sales.csv` using Python's built-in CSV library.

### 2. Validate

Checks transaction records for:

- Missing order IDs or product names
- Invalid quantity or price values
- Non-positive quantities
- Negative prices

Valid and invalid records are separated for further processing.

### 3. Transform

Converts quantities into integers and prices into decimal values.

Calculates revenue for each valid transaction:

`Revenue = Quantity × Price`

### 4. Save Processed Data

Exports validated and transformed transactions to `data/processed/clean_sales.csv`.

Invalid transactions are saved separately in `data/processed/rejected_sales.csv`.

### 5. Load

Loads cleaned sales records into a SQLite database using SQL.

### 6. Analyze

Runs SQL queries to calculate:

- Total sales revenue
- Total orders
- Total quantity sold
- Revenue by product
- Highest-revenue product

### 7. Logging

Records pipeline execution events in `logs/pipeline.log` to support troubleshooting and monitoring.

## Sample Results

The sample dataset contains six retail transactions.

| Metric | Result |
|---|---|
| Total records extracted | 6 |
| Valid records | 4 |
| Rejected records | 2 |
| Total revenue | $43.00 |
| Total quantity sold | 8 |
| Highest-revenue product | Coffee |

### Revenue by Product

| Product | Revenue |
|---|---:|
| Coffee | $16.00 |
| Eggs | $15.00 |
| Milk | $9.00 |
| Bread | $3.00 |

## How to Run the Project

### Prerequisites

- Python 3 installed
- Git (optional, for version control)

This project uses Python standard-library modules and does not require third-party packages.

### Run the Complete Pipeline

Open a terminal in the project root directory and execute:

```bash
python src/pipeline_runner.py
```

The pipeline will:

1. Read the raw sales data.
2. Validate transactions.
3. Transform valid records.
4. Generate cleaned and rejected CSV files.
5. Load cleaned records into SQLite.
6. Generate sales analytics.
7. Record execution logs.

## Future Improvements

- Add automated unit tests with `unittest`
- Support larger datasets
- Add configuration files
- Implement data quality reporting
- Integrate cloud storage
- Add workflow scheduling
- Build analytics dashboards

## Project Status