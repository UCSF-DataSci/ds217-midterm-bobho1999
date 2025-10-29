#!/bin/bash

# TODO: Add shebang line: #!/bin/bash
# Assignment 5, Question 8: Pipeline Automation Script
# Run the clinical trial data analysis pipeline

# NOTE: This script assumes Q1 has already been run to create directories and generate the dataset
# NOTE: Q2 (q2_process_metadata.py) is a standalone Python fundamentals exercise, not part of the main pipeline
# NOTE: Q3 (q3_data_utils.py) is a library imported by the notebooks, not run directly
# NOTE: The main pipeline runs Q4-Q7 notebooks in order

echo "Starting clinical trial data pipeline..." > reports/pipeline_log.txt

# TODO: Run analysis notebooks in order (q4-q7) using nbconvert with error handling
# Use either `$?` or `||` operator to check exit codes and stop on failure
# Add a log entry for each notebook execution or failure
# jupyter nbconvert --execute --to notebook q4_exploration.ipynb
# Run notebooks in sequence
{
    jupyter nbconvert --execute --to notebook q4_exploration.ipynb
    echo "SUCCESS: Q4 exploratory data analysis executed" >> reports/pipeline_log.txt
} || {
    echo "ERROR: Q4 exploratory data analysis failed" >> reports/pipeline_log.txt
    exit 1
}

{
    jupyter nbconvert --execute --to notebook q5_missing_data.ipynb
    echo "SUCCESS: Q5 missing data analysis executed" >> reports/pipeline_log.txt
} || {
    echo "ERROR: Q5 missing data analysis failed" >> reports/pipeline_log.txt
    exit 1
}

{
    jupyter nbconvert --execute --to notebook q6_transformation.ipynb
    echo "SUCCESS: Q6 Data Transformation executed" >> reports/pipeline_log.txt
} || {
    echo "ERROR: Q6 Data Transformation failed" >> reports/pipeline_log.txt
    exit 1
}

{
    jupyter nbconvert --execute --to notebook q7_aggregation.ipynb
    echo "SUCCESS: Q7 Group Operations & Final Analysis executed" >> reports/pipeline_log.txt
} || {
    echo "ERROR: Q7 Group Operations & Final Analysis failed" >> reports/pipeline_log.txt
    exit 1
}

echo "Pipeline completed successfully!" >> reports/pipeline_log.txt
echo "Pipeline complete!" >> reports/pipeline_log.txt
