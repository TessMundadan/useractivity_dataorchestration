# useractivity_dataorchestration
Automate and monitor the user activity data pipelines using Airflow.</p>
There are four custom operators:</p>
Stage Operator - loaded JSON formatted files from S3 to Amazon Redshift.</p>
Fact and Dimension Operators - SQL helper class is used to run the data transformations.</p>
Data Quality Operator- used to run checks on the data itself.</p>
