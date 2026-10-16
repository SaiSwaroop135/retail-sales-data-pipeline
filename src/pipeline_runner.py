import logging
import sqlite3
from pathlib import Path

import logger_config

from extract_sales import (
    extract_sales,
    validate_sales,
    transform_sales,
    generate_pipeline_summary,
    save_processed_sales,
    save_rejected_sales
)

from load_sales import load_sales
from sales_analytics import analyze_sales


# ==========================================
# PROJECT CONFIGURATION
# ==========================================

logger = logging.getLogger("retail_sales_pipeline")

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "sales.csv"

CLEAN_FILE = BASE_DIR / "data" / "processed" / "clean_sales.csv"

REJECTED_FILE = BASE_DIR / "data" / "processed" / "rejected_sales.csv"


# ==========================================
# COMPLETE ETL PIPELINE
# ==========================================

def run_pipeline():

    logger.info("Pipeline execution started")

    try:

        # STEP 1: CHECK INPUT FILE

        if not INPUT_FILE.is_file():
            raise FileNotFoundError(
                f"Input file not found: {INPUT_FILE}"
            )

        logger.info("Input file found successfully")


        # STEP 2: EXTRACT DATA

        print("\nSTEP 1: EXTRACTING SALES DATA")

        records = extract_sales(INPUT_FILE)

        logger.info("Extracted %s records", len(records))

        print("Total Records Extracted:", len(records))


        # STEP 3: VALIDATE DATA

        print("\nSTEP 2: VALIDATING SALES DATA")

        valid_sales, invalid_sales = validate_sales(records)

        logger.info(
            "Validation completed: %s valid, %s invalid",
            len(valid_sales),
            len(invalid_sales)
        )

        print("Valid Records:", len(valid_sales))
        print("Invalid Records:", len(invalid_sales))


        # STEP 4: TRANSFORM DATA

        print("\nSTEP 3: TRANSFORMING SALES DATA")

        clean_sales = transform_sales(valid_sales)

        logger.info(
            "Transformed %s records",
            len(clean_sales)
        )

        print("Total Transformed Records:", len(clean_sales))


        # STEP 5: SAVE PROCESSED FILES

        print("\nSTEP 4: SAVING PROCESSED DATA")

        save_processed_sales(clean_sales, CLEAN_FILE)

        save_rejected_sales(invalid_sales, REJECTED_FILE)

        logger.info("Processed CSV files saved successfully")

        print("Cleaned sales data saved successfully!")
        print("Rejected sales data saved successfully!")


        # STEP 6: GENERATE PIPELINE SUMMARY

        print("\nSTEP 5: GENERATING PIPELINE SUMMARY")

        total_revenue = generate_pipeline_summary(
            records,
            clean_sales,
            invalid_sales
        )

        logger.info(
            "Total pipeline revenue: %s",
            total_revenue
        )


        # STEP 7: LOAD DATA INTO SQLITE

        print("\nSTEP 6: LOADING DATA INTO DATABASE")

        load_sales()

        logger.info("Database loading completed")


        # STEP 8: GENERATE SALES ANALYTICS

        print("\nSTEP 7: GENERATING SALES ANALYTICS")

        analyze_sales()

        logger.info("Sales analytics completed")


        # PIPELINE COMPLETED

        print("\n====================================")
        print("RETAIL SALES ETL PIPELINE COMPLETED")
        print("====================================")

        logger.info("Pipeline execution completed successfully")

        return True


    except (FileNotFoundError, OSError, sqlite3.Error) as error:

        logger.exception("Pipeline failed")

        print("\nPIPELINE FAILED:", error)

        return False


    except Exception:

        logger.exception("Unexpected pipeline failure")

        raise


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    if not run_pipeline():
        raise SystemExit(1)
