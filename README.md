# Retail Sales Data Pipeline

An end-to-end Python ETL (Extract, Transform, Load) project that ingests retail sales transactions from CSV files, performs data validation and transformation, loads cleaned records into SQLite, and generates SQL-based sales analytics.

The project demonstrates practical data engineering skills, including modular ETL development, data quality monitoring, relational database integration, automated testing, structured logging, and continuous integration with GitHub Actions.

## Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.12 |
| Database | SQLite, SQL |
| Data Processing | CSV, Decimal, pathlib |
| Data Quality | Custom validation, rejection tracking, quality reporting |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Logging | Python logging |
| Version Control | Git, GitHub |

## ETL Architecture

```text
              RAW SALES DATA
                 sales.csv
                     |
                     v
              DATA EXTRACTION
                     |
                     v
              DATA VALIDATION
                     |
           +---------+---------+
           |                   |
           v                   v
      VALID RECORDS      INVALID RECORDS
           |                   |
           v                   v
    DATA TRANSFORMATION   REJECTION TRACKING
           |                   |
           v                   v
     clean_sales.csv     rejected_sales.csv
           |
           v
      SQLITE DATABASE
           |
           v
       SQL ANALYTICS
           |
           v
      SALES INSIGHTS

     DATA QUALITY REPORTING
     LOGGING & ERROR HANDLING
     AUTOMATED TESTING
     GITHUB ACTIONS CI
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
|   |   |-- clean_sales.csv
|   |   |-- rejected_sales.csv
|   |   |-- data_quality_report.csv
|   |-- retail_sales.db
|
|-- logs/
|   |-- pipeline.log
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
|   |-- test_database.py
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

Processed files, the SQLite database, and execution logs are generated locally and excluded from version control.

## ETL Pipeline Implementation

### 1. Data Extraction

Reads raw retail sales transactions using Python's built-in CSV library.

- Supports structured CSV input.
- Extracts transaction records for validation.
- Uses pathlib for portable file management.
- Checks input-file availability before pipeline execution.

### 2. Data Validation

Applies validation rules to identify incomplete or invalid transactions.

Validation checks include:

- Missing order IDs
- Missing product names
- Invalid quantity formats
- Zero or negative quantities
- Invalid price formats
- Negative or non-finite prices

Valid records proceed to transformation, while invalid records are separated for review.

### 3. Data Transformation

Converts validated transaction fields into appropriate Python data types.

- Converts quantities to integers.
- Converts monetary values to Decimal.
- Calculates transaction-level revenue.
- Produces structured records for downstream loading.

**Revenue = Quantity × Unit Price**

Decimal arithmetic is used to avoid common floating-point precision issues during monetary calculations.

### 4. Data Quality Reporting

Generates a data quality report to summarize validation results and rejected transactions.

The report includes:

- Total records processed
- Valid record count
- Invalid record count
- Data quality percentage
- Rejection reasons and their frequencies

**Data Quality Score = (Valid Records / Total Records) × 100**

For the included sample dataset:

| Metric | Result |
|---|---:|
| Total Records | 6 |
| Valid Records | 4 |
| Rejected Records | 2 |
| Data Quality Score | 66.67% |

Detected rejection reasons include invalid quantity formats and non-positive quantities.

The report is exported to `data/processed/data_quality_report.csv`.

### 5. Data Loading

Loads validated and transformed transactions into a SQLite relational database.

The database loading implementation includes:

- Automated table creation
- SQL-based record insertion
- Parameterized SQL statements
- Primary-key-based record replacement
- Transaction commits
- Record-count verification

The loader uses `INSERT OR REPLACE` to prevent duplicate primary-key rows during repeated loads.

### 6. SQL Analytics

Executes SQL aggregation queries against the SQLite database to generate sales insights.

Analytics include:

- Total sales revenue
- Total order count
- Total quantity sold
- Revenue by product
- Highest-revenue product

### 7. Logging and Error Handling

Uses Python's logging module to track ETL execution.

The pipeline logs extraction, validation, transformation, data quality reporting, database loading, and analytics completion.

Error handling covers missing input files, file-system operations, SQLite errors, and unexpected execution failures.

## Sample Pipeline Results

The included demonstration dataset contains six transactions.

| Metric | Result |
|---|---:|
| Records Extracted | 6 |
| Valid Transactions | 4 |
| Rejected Transactions | 2 |
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

These results demonstrate functional correctness on a small sample dataset and do not represent large-scale performance benchmarks.

## Installation and Setup

### Prerequisites

- Python 3.12
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/SaiSwaroop135/retail-sales-data-pipeline.git
cd retail-sales-data-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The ETL application primarily uses Python standard-library modules. pytest is used for automated testing.

### 4. Run the ETL Pipeline

```bash
python src/pipeline_runner.py
```

The pipeline extracts, validates, transforms, and saves transaction data, generates data quality information, loads records into SQLite, and executes SQL analytics.

## Automated Testing

The project uses pytest to validate ETL processing and database behavior.

**29 automated tests passed locally.**

Test coverage includes:

- Valid transaction processing
- Missing mandatory fields
- Invalid quantities and prices
- Zero and negative quantities
- Revenue calculations
- CSV extraction and export
- Empty datasets
- Multiple valid transactions
- Missing input files
- SQLite database integration
- Database loading behavior

Run all tests:

```bash
python -m pytest -v
```

Verified result:

```text
29 passed
```

The test suite verifies the implemented functionality against defined test cases. It does not imply complete coverage of all possible inputs or production scenarios.

## Continuous Integration

GitHub Actions automatically executes the project's test suite.

Workflow file:

`.github/workflows/tests.yml`

The workflow runs on:

- Pushes to the `main` branch
- Pull requests targeting `main`

### CI Workflow

1. Check out the repository.
2. Configure Python 3.12.
3. Install project dependencies.
4. Execute pytest.
5. Report the workflow result.

The GitHub Actions workflow has completed successfully following the project's testing and database integration updates.

## Data Quality and Reliability Features

The project demonstrates several reliability practices:

- Record-level validation
- Rejected-record isolation
- Data quality metrics and rejection reporting
- Decimal-based financial calculations
- Parameterized SQL operations
- Primary-key-based record replacement
- Execution logging
- Exception handling
- Automated unit and integration testing
- Continuous integration

## Future Enhancements

Potential improvements include:

- Configuration-driven pipeline execution
- Larger datasets and performance benchmarking
- Incremental data ingestion
- Stronger database constraints and transaction handling
- Cloud object storage integration using AWS S3
- Workflow scheduling with Apache Airflow
- Data warehouse integration
- Interactive dashboards using Power BI
- Expanded edge-case and failure-recovery testing

## Project Status

**Core ETL pipeline implemented and validated against the sample dataset.**

- End-to-end CSV-to-SQLite pipeline operational
- Data validation and transformation implemented
- Data quality reporting operational
- SQL-based analytics implemented
- Execution logging enabled
- 29 automated tests passed locally
- GitHub Actions CI verified successfully
- Source code maintained in GitHub

This project serves as a hands-on demonstration of foundational data engineering practices and provides a base for future cloud and orchestration enhancements.

## Repository

https://github.com/SaiSwaroop135/retail-sales-data-pipeline