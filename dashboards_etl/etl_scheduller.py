import schedule
from decouple import config
import threading, queue, sys, os
from datetime import datetime, timedelta
import time
from etl_job import job, etl_logs
import requests
import json

#Base launch settings
ETL_CURRENT_LOAD_DAY = datetime.today().day
ETL_API_KEY = os.getenv('ETL_API_KEY_os', config('ETL_API_KEY_env'))

#getting new list from RESTapi for ETL processing update every day once.
ETL_API_URL = os.getenv('ETL_API_URL_os', config('ETL_API_URL_env'))
URL = ETL_API_URL + ETL_API_KEY + "/etl_scheduller/get/?format=json"
response = requests.get(URL, verify=False)
data = None
if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
	data = response.json().get('results')

etl_tables = []
for row in data:
	job_tmp = {}
	job_tmp['JOB_ID'] = row.get('id')
	job_tmp['DATABASE_NAME_FROM'] = row.get('database_name_from')
	job_tmp['DATABASE_NAME_TO'] = row.get('database_name_to')
	job_tmp['TABLE_SCHEMA_FROM'] = row.get('table_schema_from')
	job_tmp['TABLE_SCHEMA_TO'] = row.get('table_schema_to')
	job_tmp['TABLE_NAME_FROM'] = row.get('table_name_from')
	job_tmp['TABLE_NAME_PREFIX'] = row.get('table_name_prefix', '-')
	job_tmp['CREATE_TABLE_IF_NOT_EXISTS'] = row.get('create_table_if_not_exists', False)
	job_tmp['WHERE_CONDITION_FROM'] = row.get('where_condition_from', '-')
	job_tmp['WHERE_CONDITION_TO'] = row.get('where_condition_to', '-')
	job_tmp['COLUMNS_FROM'] = row.get('columns_from', '*')
	job_tmp['COLUMNS_FOR_UNIQUE_ID'] = row.get('columns_for_unique_id', '*')
	job_tmp['CLEAR_ALL_DATA_BEFORE_INSERT'] = row.get('clear_all_data_before_insert', True)
	job_tmp['REMOVE_DUPLICATES_TABLE_TO'] = row.get('remove_duplicates_table_to', False)
	job_tmp['UPDATE_EXISTS_ROWS'] = row.get('update_exists_rows', False)
	job_tmp['INSERT_ONLY_NEW_ROWS'] = row.get('insert_only_new_rows', False)
	job_tmp['INSERT_ALL_ROWS'] = row.get('insert_all_rows', True)
	job_tmp['STEPS_DELAY_SECONDS'] = row.get('steps_delay_seconds', 4)
	job_tmp['LIMIT_ROWS'] = row.get('limit_rows', 30000)
	job_tmp['UPDATE_TIME_LIST'] = [i.get('update_time_list') for i in row.get('update_time_list', None)]#['11:30', '12:31', '13:02']#
	job_tmp['UPDATE_WORK_DAYS'] = [i.get('update_week_days_list') for i in row.get('update_week_days_list', None)]
	job_tmp['DROP_TABLE_TO'] = row.get('drop_table_to', False)
	etl_error_flag = row.get('etl_error_flag', None)
	if etl_error_flag == True: etl_error_flag = 1
	if etl_error_flag == False: etl_error_flag = 0
	job_tmp['ETL_ERROR_FLAG'] = etl_error_flag
	job_tmp['ETL_IS_ACTUAL'] = row.get('is_actual', False)

	if etl_error_flag == 0 and job_tmp['ETL_IS_ACTUAL'] == True:
		etl_tables.append(job_tmp)


#getting IS_ACTUAL status from RESTapi.
# URL = ETL_API_URL + ETL_API_KEY + "/etl_scheduller/update/5/"
# requests.put(URL, data={'etl_error_flag': 'true'}, verify=False)

jobs_count = len(etl_tables)
launch_delay_intervals = [x * 30 for x in range(0, jobs_count)]


# RUN ETL 
msg = f'###### ETL DAILY START >>> {str(datetime.today())} <<< ######' 
etl_logs(msg, fprint=False)

#getting IS_ACTUAL status from RESTapi.
for idx, etl_job in enumerate(etl_tables):
	if len(etl_job.get('UPDATE_TIME_LIST', [])) > 0 and len(etl_job.get('UPDATE_WORK_DAYS', [])) > 0:
		json_put = {"data": {"etl_error_flag": "false"}, "logs": {"rows_count": "0", "error_message": ""}}
		headers={'content-type': 'application/json'}
		job_text = f"""def call_job_{idx} ():
			time.spleep(launch_delay_intervals[{idx}])
			json_put = {json_put}
			headers = {headers}
			URL = ETL_API_URL + ETL_API_KEY + "/etl_scheduller/get/{etl_job.get('JOB_ID')}/?format=json"
			response = requests.get(URL, verify=False)
			data = None
			if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
				data = response.json().get('results')

			check_ETL_IS_ACTUAL = {etl_job.get('ETL_IS_ACTUAL', False)}
			check_ETL_ERROR_FLAG = {etl_job.get('ETL_ERROR_FLAG', False)}
			for row in data:
				check_ETL_IS_ACTUAL = row.get('is_actual', False)
				check_ETL_ERROR_FLAG = row.get('etl_error_flag', None)
			if check_ETL_IS_ACTUAL == True and check_ETL_ERROR_FLAG == False:
				output = job(
					JOB_ID='{etl_job.get('JOB_ID')}',
					DATABASE_NAME_FROM='{etl_job.get('DATABASE_NAME_FROM')}',
					DATABASE_NAME_TO='{etl_job.get('DATABASE_NAME_TO')}',
					TABLE_SCHEMA_FROM='{etl_job.get('TABLE_SCHEMA_FROM')}',
					TABLE_SCHEMA_TO='{etl_job.get('TABLE_SCHEMA_TO')}',
					TABLE_NAME_FROM='{etl_job.get('TABLE_NAME_FROM')}',
					TABLE_NAME_PREFIX='{etl_job.get('TABLE_NAME_PREFIX', '-')}',
					CREATE_TABLE_IF_NOT_EXISTS={etl_job.get('CREATE_TABLE_IF_NOT_EXISTS', False)},
					WHERE_CONDITION_FROM='{etl_job.get('WHERE_CONDITION_FROM', '-')}',
					WHERE_CONDITION_TO='{etl_job.get('WHERE_CONDITION_TO', '-')}',
					COLUMNS_FROM='{etl_job.get('COLUMNS_FROM', '*')}',
					COLUMNS_FOR_UNIQUE_ID='{etl_job.get('COLUMNS_FOR_UNIQUE_ID', '*')}',
					CLEAR_ALL_DATA_BEFORE_INSERT={etl_job.get('CLEAR_ALL_DATA_BEFORE_INSERT', True)},
					REMOVE_DUPLICATES_TABLE_TO={etl_job.get('REMOVE_DUPLICATES_TABLE_TO', False)},
					UPDATE_EXISTS_ROWS={etl_job.get('UPDATE_EXISTS_ROWS', False)},
					INSERT_ONLY_NEW_ROWS={etl_job.get('INSERT_ONLY_NEW_ROWS', False)},
					INSERT_ALL_ROWS={etl_job.get('INSERT_ALL_ROWS', True)},
					LIMIT_ROWS={etl_job.get('LIMIT_ROWS', 30000)},
					STEPS_DELAY_SECONDS={etl_job.get('STEPS_DELAY_SECONDS', 5)},
					DROP_TABLE_TO={etl_job.get('DROP_TABLE_TO', False)},
					ETL_NAME='{etl_job.get('ETL_NAME', '-')}',
					ETL_ERROR_FLAG={etl_job.get('ETL_ERROR_FLAG', 0)},
					ETL_IS_ACTUAL={etl_job.get('ETL_IS_ACTUAL', False)},
				)

				if output.get('status') == 0:
					json_put["data"]["etl_error_flag"] = "true"
					json_put["logs"]["error_message"] = output.get('error_message')

				json_put["logs"]["rows_count"] = output.get("rows_count")
				URL = ETL_API_URL + ETL_API_KEY + "/etl_scheduller/update/{etl_job.get('JOB_ID')}/"
				requests.put(URL, data=json.dumps(json_put), headers=headers, verify=False)
				if output.get('status') == 0:
					s = '!!!!!! ETL JOB ERROR !!!!!! ID: {etl_job.get('JOB_ID')}. os._exit(1) >>> call_job_{idx}: {etl_job.get('TABLE_NAME_FROM')}'
					etl_logs(s, fprint=False)"""
		exec(job_text)

		jobqueue_text = f"""jobqueue_{idx} = queue.Queue()"""
		exec(jobqueue_text) 
		scheduler_text = f"""scheduler_{idx} = schedule.Scheduler()"""
		exec(scheduler_text)

		for i in etl_job.get('UPDATE_TIME_LIST', []): #["09:30", "10:00", "14:42"]:
			if 'monday' in etl_job.get('UPDATE_WORK_DAYS', []): 
				add_job_to_shedule_text = f"""scheduler_{idx}.every().monday.at(i).do(jobqueue_{idx}.put, call_job_{idx})"""
				exec(add_job_to_shedule_text)
			if 'tuesday' in etl_job.get('UPDATE_WORK_DAYS', []): 
				add_job_to_shedule_text = f"""scheduler_{idx}.every().tuesday.at(i).do(jobqueue_{idx}.put, call_job_{idx})"""
				exec(add_job_to_shedule_text)
			if 'wednesday' in etl_job.get('UPDATE_WORK_DAYS', []): 
				add_job_to_shedule_text = f"""scheduler_{idx}.every().wednesday.at(i).do(jobqueue_{idx}.put, call_job_{idx})"""
				exec(add_job_to_shedule_text)
			if 'thursday' in etl_job.get('UPDATE_WORK_DAYS', []): 
				add_job_to_shedule_text = f"""scheduler_{idx}.every().thursday.at(i).do(jobqueue_{idx}.put, call_job_{idx})"""
				exec(add_job_to_shedule_text)
			if 'friday' in etl_job.get('UPDATE_WORK_DAYS', []): 
				add_job_to_shedule_text = f"""scheduler_{idx}.every().friday.at(i).do(jobqueue_{idx}.put, call_job_{idx})"""
				exec(add_job_to_shedule_text)

		worker_main_text = f"""def worker_main_{idx}():
				while 1:
					job_func_{idx} = jobqueue_{idx}.get()
					job_func_{idx}()
					jobqueue_{idx}.task_done()"""
		exec(worker_main_text)
		worker_thread_text = f"""worker_thread_{idx} = threading.Thread(target=worker_main_{idx}, daemon=True)"""
		exec(worker_thread_text)
		worker_thread_text = f"""worker_thread_{idx}.start()"""
		exec(worker_thread_text)


while True:
	for idx, etl_job in enumerate(etl_tables):
		if len(etl_job.get('UPDATE_TIME_LIST', [])) > 0 and len(etl_job.get('UPDATE_WORK_DAYS', [])) > 0:
			run_pending_text = f"""scheduler_{idx}.run_pending()"""
			exec(run_pending_text)
	time.sleep(1)
