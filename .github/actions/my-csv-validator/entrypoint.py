# .github/actions/my-csv-validator/entrypoint.py

import os
import pandas as pd
import sys

# Helper function to set action outputs
def set_action_output(name, value):
    """Sets an output variable for the GitHub Action."""
    # The GITHUB_OUTPUT environment variable points to a file where outputs should be written.
    # Format is: output_name=output_value
    env_file = os.getenv('GITHUB_OUTPUT')
    if env_file:
        with open(env_file, 'a') as f:
            f.write(f'{name}={value}\n')
    else:
        print(f"::set-output name={name}::{value}") # Fallback for older runners (less common now)


def main():
    print("--- Custom CSV Validator Action Starting ---")
    validation_status = "failure_unknown"
    rows_count = "0"
    columns_found_count = "0"

    try:
        # Retrieve input values from environment variables.
        # GitHub Actions converts input names to uppercase and prefixes with INPUT_.
        csv_path_input = os.getenv("INPUT_CSV_FILE_PATH")
        expected_columns_input = os.getenv("INPUT_EXPECTED_COLUMNS")

        # Basic input validation
        if not csv_path_input:
            print("Error: 'csv_file_path' input is missing!")
            validation_status = "failure_missing_input_path"
            # sys.exit(1) # Optionally fail the action step immediately
            return # Exit function early

        if not expected_columns_input:
            print("Error: 'expected_columns' input is missing!")
            validation_status = "failure_missing_input_columns"
            # sys.exit(1)
            return

        print(f"Input CSV Path: {csv_path_input}")
        print(f"Input Expected Columns: {expected_columns_input}")

        # Convert expected_columns to an integer
        try:
            expected_cols_int = int(expected_columns_input)
        except ValueError:
            print(f"Error: 'expected_columns' ({expected_columns_input}) must be an integer.")
            validation_status = "failure_invalid_column_type"
            # sys.exit(1)
            return

        # Check if the CSV file exists (path is relative to GITHUB_WORKSPACE)
        if not os.path.exists(csv_path_input):
            print(f"Error: CSV file not found at '{csv_path_input}'")
            validation_status = "failure_file_not_found"
            # sys.exit(1)
            return

        # Perform the data validation using pandas
        print(f"Reading CSV file: {csv_path_input}")
        df = pd.read_csv(csv_path_input)

        rows_count = str(len(df)) # Number of data rows (pandas excludes header)
        columns_found_count = str(len(df.columns)) # Number of columns

        print(f"File read successfully. Rows found: {rows_count}, Columns found: {columns_found_count}")

        # Compare found columns with expected columns
        if int(columns_found_count) == expected_cols_int:
            validation_status = "success"
            print(f"✅ Validation successful: Found {columns_found_count} columns as expected.")
        else:
            validation_status = "failure_column_mismatch"
            print(f"❌ Validation failed: Expected {expected_cols_int} columns, but found {columns_found_count}.")
            # If validation fails, you might want the action step to fail:
            # sys.exit(1)

    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")
        validation_status = f"failure_exception_{type(e).__name__}"
        # sys.exit(1) # Fail the action on any exception

    finally:
        # Set the action's outputs using the helper function
        print(f"\nSetting action outputs...")
        set_action_output("validation_status", validation_status)
        set_action_output("rows_count", rows_count)
        set_action_output("columns_found", columns_found_count)
        print(f"Output 'validation_status': {validation_status}")
        print(f"Output 'rows_count': {rows_count}")
        print(f"Output 'columns_found': {columns_found_count}")
        print("--- Custom CSV Validator Action Finished ---")

if __name__ == "__main__":
    main()