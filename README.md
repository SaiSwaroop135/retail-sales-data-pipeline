# Retail Sales Data Pipeline

An end-to-end Python ETL (Extract, Transform, Load) project that processes retail sales transactions, validates data quality, transforms records, loads cleaned data into SQLite, and generates SQL-based sales analytics.

The project demonstrates practical data engineering concepts, including modular pipeline development, data validation, database integration, logging, automated testing, and continuous integration using GitHub Actions.

## Technologies Used

- **Python 3.12** — ETL development and pipeline orchestration
- **SQLite & SQL** — Relational data storage and analytical queries
- **CSV** — Source data ingestion and processed data exports
- **Python Standard Library** — File handling, decimal calculations, and logging
- **pytest** — Automated unit testing
- **GitHub Actions** — Continuous integration and automated test execution
- **Git & GitHub** — Version control and source code management

## Project Architecture

```text
Raw Sales CSV
      |
      v
Data Extraction
      |
      v
Data Validation
      |
      +------> Invalid Records
      |              |
      |              v
      |       rejected_sales.csv
      v
Data Transformation
      |
      v
clean_sales.csv
      |
      v
SQLite Database
      |
      v
SQL Analytics
      |
      v
Sales Summary & Product Insights
```

## Project Structure

```text
retail-sales-data-pipeline/
|
|-- .github/
|   |-- workflows/
|       |-- tests.yml
|
|-- data/
|   |-- raw/
|   |   |-- sales.csv
|   |-- processed/
|       |-- clean_sales.csv (generated)
|       |-- rejected_sales.csv (generated)
|
|-- logs/
|   |-- pipeline.log (generated)
|
|-- src/
|   |-- extract_sales.py
|   |-- load_sales.py
|   |-- sales_analytics.py
|   |-- logger_config.py
|   |-- pipeline_runner.py
|
|-- tests/
|   |-- test_pipeline.py
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

The pipeline also creates or updates a local SQLite database during execution. Generated files, logs, and local databases are excluded from Git using `.gitignore`.

## ETL Pipeline Workflow

### Step 1: Extract

Reads retail transaction data from `data/raw/sales.csv` using Python's CSV library.

### Step 2: Validate

Validates incoming records to identify:

- Missing order IDs
- Missing product names
- Invalid quantities or prices
- Zero or negative quantities
- Negative prices

Valid and invalid records are separated to prevent rejected transactions from entering the cleaned dataset.

### Step 3: Transform

Transforms valid records by:

- Converting quantities into integers
- Converting monetary values into Decimal objects
- Calculating revenue for each transaction
- Preparing structured records for downstream processing

**Revenue = Quantity × Price**

### Step 4: Save Processed Data

Exports transformed transactions into `clean_sales.csv`.

Rejected transactions are stored separately in `rejected_sales.csv` for review and troubleshooting.

### Step 5: Load into SQLite

Loads validated sales transactions into a relational SQLite database for SQL-based analysis.

### Step 6: Generate Analytics

Executes SQL queries to calculate:

- Total revenue
- Total orders
- Total quantity sold
- Revenue by product
- Highest-revenue product

### Step 7: Logging and Error Handling

Uses Python logging to capture pipeline execution events and errors.

Supports troubleshooting of missing input files, file operations, database errors, and unexpected failures.

## Sample Pipeline Results

The included sample dataset contains six retail transactions.

| Metric | Result |
|---|---|
| Total Records Extracted | 6 |
| Valid Records | 4 |
| Rejected Records | 2 |
| Total Revenue | $43.00 |
| Total Orders | 4 |
| Total Quantity Sold | 8 |
| Highest-Revenue Product | Coffee |

### Revenue by Product

| Product | Revenue |
|---|---:|
| Coffee | $16.00 |
| Eggs | $15.00 |
| Milk | $9.00 |
| Bread | $3.00 |

These results are based on the included sample dataset and demonstrate pipeline functionality rather than large-scale performance.

## Installation and Setup

### Prerequisites

- Python 3.12 or compatible Python 3 version
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/SaiSwaroop135/retail-sales-data-pipeline.git
cd retail-sales-data-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Testing Dependencies

```bash
python -m pip install -r requirements.txt
```

The ETL application uses Python standard-library modules. pytest is included for automated testing.

### 4. Run the Complete ETL Pipeline

```bash
python src/pipeline_runner.py
```

The pipeline executes extraction, validation, transformation, processed-file generation, database loading, and analytics.

## Automated Testing

The project uses pytest to verify core ETL functionality.

Current tests cover:

1. Validation of valid sales records
2. Rejection of invalid sales records
3. Revenue calculation during transformation

Run the tests using:

```bash
python -m pytest -v
```

**Verified local test result: 3 passed.**

## Continuous Integration with GitHub Actions

The project includes an automated CI workflow configured in:

`.github/workflows/tests.yml`

The workflow runs when changes are pushed to the `main` branch or a pull request targets `main`.

The workflow:

1. Checks out the repository.
2. Configures Python 3.12.
3. Installs dependencies.
4. Executes automated pytest tests.
5. Reports the test results.

The initial GitHub Actions workflow completed successfully.

## Data Quality and Reliability

The pipeline includes:

- Input record validation
- Rejected-record separation
- Decimal-based financial calculations
- Structured data transformation
- Logging and exception handling
- Automated unit testing
- Continuous integration checks

These features help maintain data accuracy, reproducibility, and maintainability.

## Future Enhancements

- Expand automated test coverage
- Introduce configuration-driven execution
- Implement additional data quality checks
- Add larger datasets and performance testing
- Integrate cloud object storage
- Introduce workflow orchestration and scheduling
- Develop interactive analytics dashboards

## Project Status

**Core ETL implementation complete — testing and CI operational.**

The pipeline has been executed successfully against the sample dataset, three automated tests have passed locally, and the GitHub Actions CI workflow has completed successfully.

Additional testing and enhancements are planned to improve reliability and scalability.

## GitHub Repository

https://github.com/SaiSwaroop135/retail-sales-data-pipeline