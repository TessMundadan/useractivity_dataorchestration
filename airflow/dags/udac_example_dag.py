    from datetime import datetime, timedelta
    import os
    from airflow import DAG
    from airflow.operators.dummy_operator import DummyOperator
    from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,LoadDimensionOperator, DataQualityOperator)
    from helpers import SqlQueries

    default_args = {
        'owner': 'udacity',
        'start_date': datetime(2019, 1, 12),
        'depends_on_past': False,
        'email_on_retry': False,
        'retry_delay': timedelta(minutes=5),
        'retries': 3
    }

    dag = DAG('udac_example_dag',
              default_args=default_args,
              description='Load and transform data in Redshift with Airflow',
              schedule_interval='0 * * * *',
              catchup=False
            )

    start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        dag=dag,
        table='staging_events',
        redshift_conn_id="redshift",
        s3_bucket="udacity-dend",
        s3_key='log_data',
        aws_credentials_id='aws_credentials',
        json='s3://udacity-dend/log_json_path.json'
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        dag=dag,
        table='staging_songs',
        redshift_conn_id="redshift",
        s3_bucket="udacity-dend",
        s3_key='song-data',
        aws_credentials_id='aws_credentials',
        json='auto'

    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        dag=dag,
        redshift_conn_id="redshift",
        target_db='public',
        target_table='songplays',
        select_sql=SqlQueries.songplay_table_insert,
        insert_mode='delete-load'
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        target_db='public',
        target_table='users',
        select_sql=SqlQueries.user_table_insert,
        insert_mode='delete-load'
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        target_db='public',
        target_table='songs',
        select_sql=SqlQueries.song_table_insert,
        insert_mode='delete-load'
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        target_db='public',
        target_table='artists',
        select_sql=SqlQueries.artist_table_insert,
        insert_mode='delete-load'
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        target_db='public',
        target_table='time',
        select_sql=SqlQueries.time_table_insert,
        insert_mode='delete-load'
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        dag=dag,
        redshift_conn_id="redshift",
        check_sql=[
            {'check_sql': "SELECT COUNT(*) FROM users WHERE userid is null", 'expected_result': 0},
            {'check_sql': "SELECT COUNT(*) FROM songs WHERE songid is null", 'expected_result': 0}
        ],

    )

    end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

    start_operator >> [stage_events_to_redshift,stage_songs_to_redshift] >> load_songplays_table
    load_songplays_table >> [load_user_dimension_table,load_song_dimension_table,load_artist_dimension_table,load_time_dimension_table] >> run_quality_checks
    run_quality_checks >> end_operator


