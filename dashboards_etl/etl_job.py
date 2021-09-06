def etl_logs(msg, fprint=False):
	import os, sys

	path = os.path.dirname(os.path.realpath(__file__))
	fv = path + "\\etl_logs.txt"
	with open(fv, 'a') as f:
		f.write(msg + "\n")
		f.close()
	if fprint: print(msg)
	


def job(
	DATABASE_NAME_FROM,
	DATABASE_NAME_TO,
	TABLE_SCHEMA_FROM,
	TABLE_SCHEMA_TO,
	TABLE_NAME_FROM,
	CREATE_TABLE_IF_NOT_EXISTS=None,
	WHERE_CONDITION_FROM=None,
	WHERE_CONDITION_TO=None,
	COLUMNS_FROM = '*',
	ETL_ID_COLUMNS='*',
	CLEAR_ALL_DATA_TABLE_TO_BEFORE_ETL=True,
	REMOVE_DUPLICATES_TABLE_TO=False,
	UPDATE_EXISTS_ROWS=False,
	INSERT_NEW_ROWS=False,
	INSERT_ALL_ROWS=True,
	STEPS_DELAY_SECONDS=2,
	ETL_NAME=None):

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
		if name == 'name':
			if ask =='initialieze':
				#engine = "sqlalchemy_sqlany://{user}:{pwd}@{host}:{port}/{db}".\
				engine = "sqlalchemy_sqlany://{user}:{pwd}@{host}:{port}/{db}?charset=utf8".\
				        format(
				            user='user', 
				            pwd='pwd',
				            host='host',  #'host2', 'host3', 
				            port='port', 
				            db='db') 
				properties = {
					'engine': create_engine(engine, echo=False),
				}
				return properties

		if name == 'name2':
			if ask =='initialieze':
				engine = "postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}".\
					format(
						user='user2', 
						pwd='pwd2',
						host='host2', 
						port='port2', 
						db='db2')
				properties = {
					'engine': create_engine(engine, connect_args={'options': '-csearch_path={}'.format('schema2')}, echo=False),
				}
				return properties

		if name == 'name3':
			if ask =='initialieze':
				engine = 'sqlite:///pathTO/db.sqlite3'
				properties = {
					'engine': create_engine(engine, echo=False),
				}
				return properties

		return None

	# ETL INITIALIZE PARAMS ######################################################
	CONN_FROM = conn(name=DATABASE_NAME_FROM, ask='initialieze')
	CONN_TO = conn(name=DATABASE_NAME_TO, ask='initialieze')
	TABLE_NAME_TO = f'remote_source_{DATABASE_NAME_FROM}_' + TABLE_NAME_FROM
	if not CREATE_TABLE_IF_NOT_EXISTS: CREATE_TABLE_IF_NOT_EXISTS = True
	if not WHERE_CONDITION_FROM: WHERE_CONDITION_FROM = 'and 2=2'
	if not WHERE_CONDITION_TO: WHERE_CONDITION_TO = 'and 2=2'
	if not COLUMNS_FROM: COLUMNS_FROM = '*'
	COLUMNS_TO = COLUMNS_FROM 
	if not ETL_ID_COLUMNS: ETL_ID_COLUMNS = '*' # '*' or ['col1', 'col2', 'col3']
	if not CLEAR_ALL_DATA_TABLE_TO_BEFORE_ETL: CLEAR_ALL_DATA_TABLE_TO_BEFORE_ETL = False
	if not REMOVE_DUPLICATES_TABLE_TO: REMOVE_DUPLICATES_TABLE_TO = False
	if not UPDATE_EXISTS_ROWS: UPDATE_EXISTS_ROWS = False # INSERT_ALL_ROWS = False   ===   INSERT_NEW_ROWS = True/False  UPDATE_EXISTS_ROWS = True/False
	if not INSERT_NEW_ROWS: INSERT_NEW_ROWS = False       # INSERT_ALL_ROWS = False   ===   INSERT_NEW_ROWS = True/False  UPDATE_EXISTS_ROWS = True/False
	if not INSERT_ALL_ROWS: INSERT_ALL_ROWS = True        # INSERT_ALL_ROWS = True    ===   INSERT_NEW_ROWS = False & UPDATE_EXISTS_ROWS = False   
	if not STEPS_DELAY_SECONDS: STEPS_DELAY_SECONDS = 2
	FORMATTED_TABLE_NAME_FROM = get_formatted_schema_table(schema=TABLE_SCHEMA_FROM, table=TABLE_NAME_FROM, delimiter='.')
	FORMATTED_TABLE_NAME_TO = get_formatted_schema_table(schema=TABLE_SCHEMA_TO, table=TABLE_NAME_TO, delimiter='.')
	if not ETL_NAME: ETL_NAME = f'{DATABASE_NAME_FROM}.{FORMATTED_TABLE_NAME_FROM} >> {DATABASE_NAME_TO}.{FORMATTED_TABLE_NAME_TO}'


	# ETL #########################################################################
	msg = f'ETL---[{ETL_NAME}]---DATE--[{str(datetime.datetime.now())[:-7]}]---START.'
	etl_logs(msg, fprint=True)

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
					return 0
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
		return 0

	# TRANSFORM ######################################
	time.sleep(STEPS_DELAY_SECONDS) 
	if is_created:
		try:
			msg = '...TRANSFORM.' 
			etl_logs(msg, fprint=False)
			#from
			SQL_FROM = f"""select {COLUMNS_FROM} from {FORMATTED_TABLE_NAME_FROM} where 1=1 {WHERE_CONDITION_FROM};"""
			df1 = pd.read_sql(SQL_FROM, con=conn1)

			def make_identifier(df):
			    str_id = df.apply(lambda x: '_'.join(map(str, x)), axis=1)
			    return str_id
			    #return pd.factorize(str_id)[0]
			if ETL_ID_COLUMNS == '*':
				df1['etl_id'] = make_identifier(df1[list(df1.columns.values)])  
			else:
				df1['etl_id'] = make_identifier(df1[ETL_ID_COLUMNS])

			df1 = df1.drop_duplicates(subset=['etl_id'], keep=False)
			if UPDATE_EXISTS_ROWS or INSERT_NEW_ROWS:
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
			return 0

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
				if CLEAR_ALL_DATA_TABLE_TO_BEFORE_ETL:
					SQL_TO = f"""delete from {FORMATTED_TABLE_NAME_TO};"""
					result = execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
					msg = f'......deleted old rows count from {FORMATTED_TABLE_NAME_TO}.: {result.rowcount}' 
					etl_logs(msg, fprint=False)

				if UPDATE_EXISTS_ROWS and not INSERT_ALL_ROWS:
					update_columns = get_server_properties(conn2, 'get_columns', TABLE_SCHEMA_TO, TABLE_NAME_TO)
					update_columns = [i.get('name') for i in update_columns if i.get('name') not in ['row_id', 'etl_created_at']]
					SQL_TO = f"""update {FORMATTED_TABLE_NAME_TO} t1 set "{'", "'.join([col+'" = t2."'+col for col in update_columns])}" from {FORMATTED_TABLE_NAME_TO}_tmp1 t2 where t1."etl_id" = t2."etl_id";"""
					SQL_TO = SQL_TO.replace('t2."etl_updated_at"', str(func.now()))
					result = execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
					msg = f'......updated exists rows count into {FORMATTED_TABLE_NAME_TO}.: {result.rowcount}'
					etl_logs(msg, fprint=False)

				if INSERT_NEW_ROWS and not INSERT_ALL_ROWS:
					insert_columns = get_server_properties(conn2, 'get_columns', TABLE_SCHEMA_TO, TABLE_NAME_TO)
					insert_columns = [i.get('name') for i in insert_columns if i.get('name') not in ['row_id', 'etl_created_at']]
					SQL_TO = f"""insert into {FORMATTED_TABLE_NAME_TO} ("{'", "'.join(insert_columns)}") select "{'", "'.join(insert_columns)}" from {FORMATTED_TABLE_NAME_TO}_tmp1 where etl_id not in (select distinct etl_id from {FORMATTED_TABLE_NAME_TO})"""
					result = execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
					msg = f'......inserted only new rows count into {FORMATTED_TABLE_NAME_TO}.: {result.rowcount}' 
					etl_logs(msg, fprint=False)

				if INSERT_ALL_ROWS:
					if TABLE_SCHEMA_TO:
						df1.to_sql(name=TABLE_NAME_TO, con=conn2, schema=TABLE_SCHEMA_TO, if_exists='append', index=False)
					else:
						df1.to_sql(name=TABLE_NAME_TO, con=conn2, if_exists='append', index=False)
					msg = f'......inserted all new rows count into {FORMATTED_TABLE_NAME_TO}.: {count_rows_df1}' 
					etl_logs(msg, fprint=False)

				#clear all duplicates after inserting new data
				if REMOVE_DUPLICATES_TABLE_TO:
					SQL_TO = f"""delete from {FORMATTED_TABLE_NAME_TO} where row_id in (select row_id from (select etl_id, row_id, row_number() over (partition by etl_id) rn from {FORMATTED_TABLE_NAME_TO}) t where t.rn > 1);"""
					execute_sql_via_transaction(conn=conn2, sql=SQL_TO)
				
				if UPDATE_EXISTS_ROWS or INSERT_NEW_ROWS:
					SQL_TO = f"""drop table {FORMATTED_TABLE_NAME_TO}"""+"_tmp1"
					execute_sql_via_transaction(conn=conn2, sql=SQL_TO)

				msg = '...LOAD DONE.'
				etl_logs(msg, fprint=False)
			except Exception as e:
				msg = f'......Cannot load data.: {str(e)}'
				etl_logs(msg, fprint=False)
				return 0

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
		return 0


	msg = f'ETL---[{ETL_NAME}]---DATE--[{str(datetime.datetime.now())[:-7]}]---END.'
	etl_logs(msg, fprint=True)
	return 1


#print('==========================================', status, '==========================================')
