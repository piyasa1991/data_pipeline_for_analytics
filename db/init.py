from db import DB
import time
from pathlib import Path
import sys

# config
LOG_FILE_A = Path('.')/"logging"/"logs"/"log_a.txt"
LOG_FILE_B = Path('.')/"logging"/"logs"/"log_b.txt"

dbobj= DB()
session = dbobj.get_session()
if dbobj.isDatabaseEmpty():
    dbobj.create_table()
    
try:
    f_a = open(LOG_FILE_A, 'r')
    f_b = open(LOG_FILE_B, 'r')
    while True:
        where_a = f_a.tell()
        line_a = f_a.readline()
        where_b = f_b.tell()
        line_b = f_b.readline()

        if not line_a and not line_b:
            time.sleep(1)
            f_a.seek(where_a)
            f_b.seek(where_b)
            continue
        else:
            if line_a:
                line = line_a
            else:
                line = line_b

            line = line.strip()
            dbobj.insert_logs_to_table(line,session)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    f_a.close()
    f_b.close()
    sys.exit()
