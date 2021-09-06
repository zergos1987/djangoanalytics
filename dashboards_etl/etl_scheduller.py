import schedule
import threading, queue, sys, os
from datetime import datetime, timedelta
import time
from etl_job import job, etl_logs




def job_1():
	status = job(DATABASE_NAME_FROM='DATABASE_NAME_FROM',
	DATABASE_NAME_TO='DATABASE_NAME_TO',
	TABLE_SCHEMA_FROM='TABLE_SCHEMA_FROM',
	TABLE_SCHEMA_TO='TABLE_SCHEMA_TO',
	TABLE_NAME_FROM='TABLE_NAME_FROM',
	COLUMNS_FROM = '*',
	ETL_ID_COLUMNS='*',
	CLEAR_ALL_DATA_TABLE_TO_BEFORE_ETL=True,
	REMOVE_DUPLICATES_TABLE_TO=False,
	UPDATE_EXISTS_ROWS=False,
	INSERT_NEW_ROWS=False,
	INSERT_ALL_ROWS=True,
	STEPS_DELAY_SECONDS=4
	)
	if status == 0:
		etl_logs('!!!!!! ETL JOB ERROR !!!!!! os._exit(1) >>> job_1', fprint=False)
		os._exit(1)

def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()

jobqueue = queue.Queue()

for i in ["09:30", "10:00"]:
	schedule.every().monday.at(i).do(jobqueue.put, job_1)
	schedule.every().tuesday.at(i).do(jobqueue.put, job_1)
	schedule.every().wednesday.at(i).do(jobqueue.put, job_1)
	schedule.every().thursday.at(i).do(jobqueue.put, job_1)
	schedule.every().friday.at(i).do(jobqueue.put, job_1)

worker_thread = threading.Thread(target=worker_main, daemon=True)
worker_thread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
