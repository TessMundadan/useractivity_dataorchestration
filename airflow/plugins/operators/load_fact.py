from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
    insert_template = ("""INSERT INTO {target_db}.{target_table} """)

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 target_db="",
                 target_table="",
                 select_sql="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.target_db=target_db
        self.target_table=target_table
        self.select_sql=select_sql
        
    def execute(self, context):
        self.log.info('Begin insertion to {} fact table'.format(self.target_table))
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        facts_insert_template = LoadFactOperator.insert_template+self.select_sql
        facts_insert_sql = facts_insert_template.format(
            target_db=self.target_db,
            target_table=self.target_table
        )
        redshift.run(facts_insert_sql)
        self.log.info('Insertion to {} fact completed'.format(self.target_table))

