def etl_logs(msg, fprint=False):
	import os, sys

	path = os.path.dirname(os.path.realpath(__file__))
	fv = path + "\\etl_logs.txt"
	with open(fv, 'a') as f:
		f.write(msg + "\n")
		f.close()
	if fprint: print(msg)
	


def job(
	JOB_ID,
	DATABASE_NAME_FROM,
	DATABASE_NAME_TO,
	TABLE_SCHEMA_FROM,
	TABLE_SCHEMA_TO,
	TABLE_NAME_FROM,
	TABLE_NAME_PREFIX='-',
	CREATE_TABLE_IF_NOT_EXISTS=False,
	WHERE_CONDITION_FROM='-',
	WHERE_CONDITION_TO='-',
	COLUMNS_FROM='*',
	COLUMNS_FOR_UNIQUE_ID='*',
	CLEAR_ALL_DATA_BEFORE_INSERT=True,
	REMOVE_DUPLICATES_TABLE_TO=False,
	UPDATE_EXISTS_ROWS=False,
	INSERT_ONLY_NEW_ROWS=False,
	INSERT_ALL_ROWS=True,
	LIMIT_ROWS=30000,
	STEPS_DELAY_SECONDS=2,
	DROP_TABLE_TO=False,
	ETL_NAME='-',
	ETL_ERROR_FLAG=0,
	ETL_IS_ACTUAL=False):

	if ETL_IS_ACTUAL:


		import os, sys
		import datetime
		from datetime import timedelta
		import time

		import sqlalchemy
		from sqlalchemy import inspect
		from sqlalchemy import create_engine, MetaData, Table, select, asc
		from sqlalchemy import Column, Integer, DateTime, Text
		from sqlalchemy.sql import func
		from sqlalchemy.orm import sessionmaker, close_all_sessions
		from sqlalchemy.ext.declarative import declarative_base

		from decouple import config

		import pandas as pd
		# ETL METHODS #########################################################
		def get_formatted_schema_table(schema, table, delimiter):
			if schema:
				return f'{schema}{delimiter}{table}'
			else:
				return table

		def get_server_properties(conn, prop_name, schema_name=None, table_name=None):
			if prop_name == 'get_schema_names':
				return inspect(conn).get_schema_names()
			if prop_name == 'get_table_names':
				if schema_name:
					return inspect(conn).get_table_names(schema_name)
				else:
					return inspect(conn).get_table_names()
			if prop_name == 'get_columns':
				if schema_name:
					return inspect(conn).get_columns(table_name, schema_name)
				else:
					return inspect(conn).get_columns(table_name)
			return None

		def execute_sql(conn, sql):
			try:
				results = conn.execute(sql)
				return results
			except Exception as e:
				msg = f'execute_sql -- error -- {str(e)}'
				etl_logs(msg, fprint=False)

		def execute_sql_via_transaction(conn, sql):
			trans = conn.begin()
			try:
				results = conn.execute(sql)
				trans.commit()
				return results
			except Exception as e:
				trans.rollback()
				msg = f'execute_via_transaction -- error -- {str(e)}'
				etl_logs(msg, fprint=False)

		def clean_sql_data(results):
			row, data_list = {}, []
			for rowproxy in results:
				# rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
				for column, value in rowproxy.items():
					# build up the dictionary
					row = {**row, **{column: value}}
				data_list.append(row)
			return data_list

		def conn(name, ask):
			if name == 'khd':
				if ask =='conn_type': return 'SYBASE'
				if ask =='initialieze':
					#engine = "sqlalchemy_sqlany://{user}:{pwd}@{host}:{port}/{db}".\
					engine = "sqlalchemy_sqlany://{user}:{pwd}@{host}:{port}/{db}?charset=utf8".\
					        format(
					            user=os.getenv('BusinessObjects_Login_os', config('BusinessObjects_Login_env')), 
					            pwd=os.getenv('BusinessObjects_Password_os', config('BusinessObjects_Password_env')),
					            host=os.getenv('BusinessObjects_Host_os', config('BusinessObjects_Host_env')), 
					            port=os.getenv('BusinessObjects_Port_os', config('BusinessObjects_Port_env')), 
					            db=os.getenv('BusinessObjects_Database_os', config('BusinessObjects_Database_env'))) 
					properties = {
						'engine': create_engine(engine, echo=False),
					}
					return properties

			if 'djangoanalytics' in name:
				if ask =='conn_type': return 'POSTGRES'
				if ask =='initialieze':
					engine = "postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}".\
						format(
							user=os.getenv('Postgresql_Login_os', config('Postgresql_Login_env')), 
							pwd=os.getenv('Postgresql_Password_os', config('Postgresql_Password_env')),
							host=os.getenv('Postgresql_Host_os', config('Postgresql_Host_env')), 
							port=os.getenv('Postgresql_Port_os', config('Postgresql_Port_env')), 
							db=os.getenv('Postgresql_Database_os', config('Postgresql_Database_env')))

					if name == 'djangoanalytics':
						properties = {
							'engine': create_engine(engine, connect_args={'options': '-csearch_path={}'.format(os.getenv('Postgresql_Schema_Portal_os', config('Postgresql_Schema_Portal_env')))}, echo=False),
						}
					else:
						if name == 'djangoanalytics_dashboards':
							properties = {
								'engine': create_engine(engine, connect_args={'options': '-csearch_path={}'.format(os.getenv('Postgresql_Schema_Metabase_os', config('Postgresql_Schema_Metabase_env')))}, echo=False),
							}
					return properties
	        
			if name == 'sqllite_djangoservices':
				if ask =='conn_type': return 'SQLITE'
				if ask =='initialieze':
					engine = 'sqlite:///' #+ os.getenv('sqlite3_os', config('sqlite3_env'))
					properties = {
						'engine': create_engine(engine, echo=False),
					}
					return properties

			return None

		# ETL INITIALIZE PARAMS ######################################################
		output = {'status': 1, 'rows_count': 0, 'error_message': ''}
		CONN_FROM = conn(name=DATABASE_NAME_FROM, ask='initialieze')
		CONN_TO = conn(name=DATABASE_NAME_TO, ask='initialieze')
		TABLE_NAME_TO = TABLE_NAME_FROM
		if TABLE_NAME_PREFIX != '-': 
			TABLE_NAME_TO = f'{DATABASE_NAME_FROM}_' + f'{TABLE_NAME_PREFIX}_'+ TABLE_NAME_TO
		else:
			TABLE_NAME_TO = f'{DATABASE_NAME_FROM}_' + TABLE_NAME_TO
		TABLE_NAME_TO = TABLE_NAME_TO.lower()
		if not CREATE_TABLE_IF_NOT_EXISTS: CREATE_TABLE_IF_NOT_EXISTS = True
		if WHERE_CONDITION_FROM == '-': WHERE_CONDITION_FROM = 'and 2=2'
		if WHERE_CONDITION_TO == '-': WHERE_CONDITION_TO = 'and 2=2'
		if not COLUMNS_FROM: COLUMNS_FROM = '*'
		COLUMNS_TO = COLUMNS_FROM
		if not COLUMNS_FOR_UNIQUE_ID: COLUMNS_FOR_UNIQUE_ID = '*' # '*' or ['col1', 'col2', 'col3']
		if not CLEAR_ALL_DATA_BEFORE_INSERT: CLEAR_ALL_DATA_BEFORE_INSERT = True
		if not REMOVE_DUPLICATES_TABLE_TO: REMOVE_DUPLICATES_TABLE_TO = False
		if not UPDATE_EXISTS_ROWS: UPDATE_EXISTS_ROWS = False # INSERT_ALL_ROWS = False   ===   INSERT_ONLY_NEW_ROWS = True/False  UPDATE_EXISTS_ROWS = True/False
		if not INSERT_ONLY_NEW_ROWS: INSERT_ONLY_NEW_ROWS = False       # INSERT_ALL_ROWS = False   ===   INSERT_ONLY_NEW_ROWS = True/False  UPDATE_EXISTS_ROWS = True/False
		if not INSERT_ALL_ROWS: INSERT_ALL_ROWS = True        # INSERT_ALL_ROWS = True    ===   INSERT_ONLY_NEW_ROWS = False & UPDATE_EXISTS_ROWS = False   
		if not STEPS_DELAY_SECONDS: STEPS_DELAY_SECONDS = 5
		FORMATTED_TABLE_NAME_FROM = get_formatted_schema_table(schema=TABLE_SCHEMA_FROM, table=TABLE_NAME_FROM, delimiter='.')
		FORMATTED_TABLE_NAME_TO = get_formatted_schema_table(schema=TABLE_SCHEMA_TO, table=TABLE_NAME_TO, delimiter='.')
		ETL_NAME = f'{DATABASE_NAME_FROM}.{FORMATTED_TABLE_NAME_FROM} >> {DATABASE_NAME_TO}.{FORMATTED_TABLE_NAME_TO}'



		# ETL #########################################################################
		msg = f'ETL---[{ETL_NAME}]---DATE--[{str(datetime.datetime.now())[:-7]}]---START.'
		etl_logs(msg, fprint=True)

		# ETL error status ############################################################
		if ETL_ERROR_FLAG == 1: 
			msg = f'......ETL_ERROR_FLAG 1. table from {FORMATTED_TABLE_NAME_FROM}.'
			etl_logs(msg, fprint=False)
			output['status'] = 0
			return output

		# CONNECTION FROM ################################
		conn1 = CONN_FROM.get('engine').connect()
		metadata1 = MetaData(bind=conn1)
		Session1 = sessionmaker(conn1)
		_session1 = Session1()
		# CONNECTION TO ##################################
		conn2 = CONN_TO.get('engine').connect()
		metadata2 = MetaData(bind=conn2)
		Session2 = sessionmaker(conn2)
		_session2 = Session2()

		# EXTRACT ########################################
		# Drop table TO if exists
		if DROP_TABLE_TO == True:
			db_tables = get_server_properties(conn2, 'get_table_names', TABLE_SCHEMA_TO)
			table_to = [t for t in db_tables if t.lower() == f'{TABLE_NAME_TO}'.lower()]
			if len(table_to) != 0:
				SQL_TO = f"""drop table {FORMATTED_TABLE_NAME_TO};"""
				execute_sql(conn=conn2, sql=SQL_TO)
			msg = f'......DROP_TABLE_TO - DONE. table to {FORMATTED_TABLE_NAME_TO}.'
			etl_logs(msg, fprint=False)
			output['status'] = 0
			return output


		time.sleep(STEPS_DELAY_SECONDS) 
		# create TABLE_NAME_TO if not exits
		try:
			msg = '...EXTRACT.' 
			etl_logs(msg, fprint=False)
			if CREATE_TABLE_IF_NOT_EXISTS:
				is_created = False
				if conn1 and conn2:
					# copy table structure from === to
					db_tables = get_server_properties(conn1, 'get_table_names', TABLE_SCHEMA_FROM)
					table_from = [t for t in db_tables if t.lower() == f'{TABLE_NAME_FROM}'.lower()]

					db_tables = get_server_properties(conn2, 'get_table_names', TABLE_SCHEMA_TO)
					table_to = [t for t in db_tables if t.lower() == f'{TABLE_NAME_TO}'.lower()]

					if len(table_from) == 0:
						msg = f'......table {FORMATTED_TABLE_NAME_FROM} does not exists! Script was stopped!'
						etl_logs(msg, fprint=False)
						_session1.close()
						_session2.close()
						conn1.close()
						conn2.close()
						output['status'] = 0
						output['error_message'] = str(msg)
						return output
					else:
						table_from = table_from[0]

					if len(table_to) == 0:
						msg = f'......table {FORMATTED_TABLE_NAME_TO} not exists. creating..'
						etl_logs(msg, fprint=False)
						if TABLE_SCHEMA_FROM:
							t = Table(table_from, metadata1, autoload=True, autoload_with=conn1, schema=TABLE_SCHEMA_FROM)
							t.schema = TABLE_SCHEMA_TO
						else:
							t = Table(table_from, metadata1, autoload=True, autoload_with=conn1)
						t.name = TABLE_NAME_TO
						created_at = Column('etl_created_at', DateTime(timezone=True), server_default=func.now(), nullable=True)
						updated_at = Column('etl_updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=True)
						etl_id = Column('etl_id', Text(), nullable=True)
						row_id = Column('row_id', Integer(), primary_key=True) 
						t.append_column(created_at)
						t.append_column(updated_at)
						t.append_column(etl_id)
						t.append_column(row_id)
						t.create(conn2)
					else:
						table_to = table_to[0]
						is_created = True
						msg = f'......table {FORMATTED_TABLE_NAME_TO} exists. do nothing..'
						etl_logs(msg, fprint=False)

				else:
					msg = '......connection problem with conn1 or conn2.'
					etl_logs(msg, fprint=False)
					sys.exit()
			else:
				is_created = True
			msg = '...EXTRACT DONE.' 
			etl_logs(msg, fprint=False)
		except Exception as e:
			msg = f'......Cannot extract data.: {str(e)}' 
			etl_logs(msg, fprint=False)
			output['status'] = 0
			output['error_message'] = str(e)
			return output

		# TRANSFORM ######################################
		time.sleep(STEPS_DELAY_SECONDS) 
		if is_created:
			try:
				msg = '...TRANSFORM.' 
				etl_logs(msg, fprint=False)
				#from
				DATABASE_TYPE = conn(name=DATABASE_NAME_FROM, ask='conn_type')
				LIMIT = LIMIT_ROWS
				if DATABASE_TYPE == 'POSTGRES':
					SQL_FROM = f"""select {COLUMNS_FROM} from {FORMATTED_TABLE_NAME_FROM} where 1=1 {WHERE_CONDITION_FROM} LIMIT {LIMIT};"""
				if DATABASE_TYPE == 'SYBASE':
					SQL_FROM = f"""select TOP {LIMIT} {COLUMNS_FROM} from {FORMATTED_TABLE_NAME_FROM} where 1=1 {WHERE_CONDITION_FROM};"""
				if DATABASE_TYPE == 'ORACLE':
					SQL_FROM = f"""select {COLUMNS_FROM} from {FORMATTED_TABLE_NAME_FROM} where 1=1 {WHERE_CONDITION_FROM} ROWNUM <= {LIMIT};"""
				if DATABASE_TYPE == 'MSSQL':
					SQL_FROM = f"""select TOP {LIMIT} {COLUMNS_FROM} from {FORMATTED_TABLE_NAME_FROM} where 1=1 {WHERE_CONDITION_FROM};"""
				if DATABASE_TYPE == 'SQLITE':
					SQL_FROM = f"""select TOP {LIMIT} {COLUMNS_FROM} from {FORMATTED_TABLE_NAME_FROM} where 1=1 {WHERE_CONDITION_FROM};"""
				
				df1 = pd.read_sql(SQL_FROM, con=conn1)

				def make_identifier(df):
				    str_id = df.apply(lambda x: '_'.join(map(str, x)), axis=1)
				    return str_id
				    #return pd.factorize(str_id)[0]
				if COLUMNS_FOR_UNIQUE_ID == '*':
					df1['etl_id'] = make_identifier(df1[list(df1.columns.values)])  
				else:
					df1['etl_id'] = make_identifier(df1[COLUMNS_FOR_UNIQUE_ID])

				df1 = df1.drop_duplicates(subset=['etl_id'], keep=False)
				if UPDATE_EXISTS_ROWS or INSERT_ONLY_NEW_ROWS:
					#create temporarty table with similar structure FROM_DB_TB > 
					db_tables = get_server_properties(conn2, 'get_table_names', TABLE_SCHEMA_TO)
					table_to = [t for t in db_tables if t.lower() == f'{TABLE_NAME_TO}_tmp1'.lower()]
					if len(table_to) != 0:
						SQL_TO = f"""drop table {FORMATTED_TABLE_NAME_TO}_tmp1;"""
						execute_sql(conn=conn2, sql=SQL_TO)
					SQL_TO = f"""select * into {FORMATTED_TABLE_NAME_TO}_tmp1 from {FORMATTED_TABLE_NAME_TO} where 1 = 2;"""
					execute_sql(conn=conn2, sql=SQL_TO)
					if TABLE_SCHEMA_TO:
						df1.to_sql(name=TABLE_NAME_TO+'_tmp1', con=conn2, schema=TABLE_SCHEMA_TO, if_exists='append', index=False)
					else:
						df1.to_sql(name=TABLE_NAME_TO+'_tmp1', con=conn2, if_exists='append', index=False)

				count_rows_df1 = df1[df1.columns[0]].count()

				msg = '...TRANSFORM DONE.' 
				etl_logs(msg, fprint=False)
			except Exception as e:
				msg = f'......Cannot transform data.: {str(e)}' 
				etl_logs(msg, fprint=False)
				output['status'] = 0
				output['error_message'] = str(e)
				return output

		# LOAD ###########################################
		time.sleep(STEPS_DELAY_SECONDS) 
		if is_created:
			msg = '...LOAD.'
			etl_logs(msg, fprint=False)
			if count_rows_df1 == 0:
				msg = f'......new rows count into {FORMATTED_TABLE_NAME_TO}.: {count_rows_df1} ETL Aborted !' 
				etl_logs(msg, fprint=False)
			else:
				try:
					if CLEAR_ALL_DATA_BEFORE_INSERT:
						SQL_TO = f"""delete from {FORMATTED_TABLE_NAME_TO};"""
						result = execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
						msg = f'......deleted old rows count from {FORMATTED_TABLE_NAME_TO}.: {result.rowcount}' 
						output['rows_count'] = str(result.rowcount)
						etl_logs(msg, fprint=False)

					if UPDATE_EXISTS_ROWS and not INSERT_ALL_ROWS:
						update_columns = get_server_properties(conn2, 'get_columns', TABLE_SCHEMA_TO, TABLE_NAME_TO)
						update_columns = [i.get('name') for i in update_columns if i.get('name') not in ['row_id', 'etl_created_at']]
						SQL_TO = f"""update {FORMATTED_TABLE_NAME_TO} t1 set "{'", "'.join([col+'" = t2."'+col for col in update_columns])}" from {FORMATTED_TABLE_NAME_TO}_tmp1 t2 where t1."etl_id" = t2."etl_id";"""
						SQL_TO = SQL_TO.replace('t2."etl_updated_at"', str(func.now()))
						result = execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
						msg = f'......updated exists rows count into {FORMATTED_TABLE_NAME_TO}.: {result.rowcount}'
						output['rows_count'] = str(result.rowcount)
						etl_logs(msg, fprint=False)

					if INSERT_ONLY_NEW_ROWS and not INSERT_ALL_ROWS:
						insert_columns = get_server_properties(conn2, 'get_columns', TABLE_SCHEMA_TO, TABLE_NAME_TO)
						insert_columns = [i.get('name') for i in insert_columns if i.get('name') not in ['row_id', 'etl_created_at']]
						SQL_TO = f"""insert into {FORMATTED_TABLE_NAME_TO} ("{'", "'.join(insert_columns)}") select "{'", "'.join(insert_columns)}" from {FORMATTED_TABLE_NAME_TO}_tmp1 where etl_id not in (select distinct etl_id from {FORMATTED_TABLE_NAME_TO})"""
						result = execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
						msg = f'......inserted only new rows count into {FORMATTED_TABLE_NAME_TO}.: {result.rowcount}' 
						output['rows_count'] = str(result.rowcount)
						etl_logs(msg, fprint=False)

					if INSERT_ALL_ROWS:
						if TABLE_SCHEMA_TO:
							df1.to_sql(name=TABLE_NAME_TO, con=conn2, schema=TABLE_SCHEMA_TO, if_exists='append', index=False)
						else:
							df1.to_sql(name=TABLE_NAME_TO, con=conn2, if_exists='append', index=False)
						msg = f'......inserted all new rows count into {FORMATTED_TABLE_NAME_TO}.: {count_rows_df1}' 
						output['rows_count'] = str(count_rows_df1)
						etl_logs(msg, fprint=False)

					#clear all duplicates after inserting new data
					if REMOVE_DUPLICATES_TABLE_TO:
						SQL_TO = f"""delete from {FORMATTED_TABLE_NAME_TO} where row_id in (select row_id from (select etl_id, row_id, row_number() over (partition by etl_id) rn from {FORMATTED_TABLE_NAME_TO}) t where t.rn > 1);"""
						execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
					
					if UPDATE_EXISTS_ROWS or INSERT_ONLY_NEW_ROWS:
						SQL_TO = f"""drop table {FORMATTED_TABLE_NAME_TO}"""+"_tmp1"
						execute_sql_via_transaction(conn=conn2, sql=SQL_TO)

					msg = '...LOAD DONE.'
					etl_logs(msg, fprint=False)
				except Exception as e:
					msg = f'......Cannot load data.: {str(e)}'
					etl_logs(msg, fprint=False)
					output['status'] = 0
					output['error_message'] = str(e)
					return output

		# DONE #3#########################################
		time.sleep(STEPS_DELAY_SECONDS)
		try:
			_session1.close()
			_session2.close()
			conn1.close()
			conn2.close()
		except Exception as e:
			msg = f'......Cannot close connections.: {str(e)}'
			etl_logs(msg, fprint=False)
			output['status'] = 0
			output['error_message'] = str(e)
			return output


		msg = f'ETL---[{ETL_NAME}]---DATE--[{str(datetime.datetime.now())[:-7]}]---END.'
		etl_logs(msg, fprint=True)
	return output


#print('==========================================', status, '==========================================')
