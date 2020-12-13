# useractivity_dataorchestration
Automate and monitor the user activity data pipelines using Airflow.
There are four custom operators:
Stage Operator - loaded JSON formatted files from S3 to Amazon Redshift.
Fact and Dimension Operators - SQL helper class is used to run the data transformations.
Data Quality Operator- used to run checks on the data itself.
