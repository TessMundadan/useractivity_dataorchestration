from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    
    insert_template = ("""INSERT INTO {target_db}.{target_table} """)
    delete_template = ("""DELETE FROM {target_db}.{target_table} """)

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 target_db="",
                 target_table="",
                 select_sql="",
                 insert_mode="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.target_db=target_db
        self.target_table=target_table
        self.select_sql=select_sql
        self.insert_mode=insert_mode

    def execute(self, context):
        self.log.info(f"Begin insertion to {self.target_table} dimension table")
                      
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        
        if self.insert_mode == 'delete-load':
            self.log.info(f"Delete from {self.target_table} dimension table")
            dimension_delete_sql=LoadDimensionOperator.delete_template.format(
                target_db=self.target_db,
                target_table=self.target_table
            )
            redshift.run(dimension_delete_sql)
       
        dimension_insert_template = LoadDimensionOperator.insert_template+self.select_sql
        dimension_insert_sql = dimension_insert_template.format(
            target_db=self.target_db,
            target_table=self.target_table
        )
        redshift.run(dimension_insert_sql)
        self.log.info(f"Insertion to {self.target_table} completed")
