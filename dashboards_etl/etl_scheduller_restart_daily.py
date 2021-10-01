from decouple import config
import threading, queue, sys, os
from datetime import datetime, timedelta
from etl_job import etl_logs
import time


#NSSM 
ETL_API_KEY = os.getenv('NSSM_PATH_os', config('NSSM_PATH_env'))
ETL_CURRENT_LOAD_DAY = datetime.today().day
service_stop = ETL_API_KEY + "nssm.exe stop CreditBlockETLService"
service_start = ETL_API_KEY + "nssm.exe start CreditBlockETLService"

os.system(service_start)

while True:
	if ETL_CURRENT_LOAD_DAY < datetime.today().day:
		msg = f'###### ETL DAILY RELOAD >>> {str(datetime.today())} <<< ######' 
		etl_logs(msg, fprint=False)
		ETL_CURRENT_LOAD_DAY +=1
		os.system(service_stop)
		time.sleep(30)
		os.system(service_start)
	time.sleep(1)
