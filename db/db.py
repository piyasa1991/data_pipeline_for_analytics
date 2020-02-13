from datetime import datetime

from sqlalchemy import create_engine, inspect
from os import environ
import os
from dotenv import load_dotenv
from models import Base, Logs
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import csv
from sqlalchemy.ext.horizontal_shard import ShardedSession

from pathlib import Path

ENV_DIRECTORY:Path = Path(__file__).parents[1]/ "envs"
load_dotenv(dotenv_path= ENV_DIRECTORY/".env")


class DB(object):
    def __init__(self):
        print(os.getenv("DATABASE_URI"))
        self.db = create_engine(os.getenv("DATABASE_URI"))

    def isDatabaseEmpty(self):
        table_names=inspect(self.db).get_table_names()
        if len(table_names)>0:
            return False
        else:
            return True
    def create_table(self):
        Base.metadata.create_all(self.db)
        print('Tables created...')

    def drop_table(self):
        Base.metadata.drop_all(self.db)
        print('Tables deleted...')

    def insert_logs_to_table(self,line,session):
        data = self.parse_line(line)
        log=Logs(**data)
        session.add(log)
        session.commit()

    def parse_line(self,line):
        split_line = line.split(" ")
        if len(split_line) < 12:
            return []
        remote_addr = split_line[0]
        time_local = split_line[3] + " " + split_line[4]
        request_type = split_line[5]
        request_path = split_line[6]
        status = split_line[8]
        body_bytes_sent = split_line[9]
        http_referer = split_line[10]
        http_user_agent = " ".join(split_line[11:])
        created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        return {'raw_log':line,
            'remote_addr':remote_addr,
            'time_local':time_local,
            'request_type':request_type,
            'request_path':request_path,
            'status':status,
            'body_bytes_sent':body_bytes_sent,
            'http_referer':http_referer,
            'http_user_agent':http_user_agent,
            'created':created }

    def get_session(self):
        # create a session
        create_session = sessionmaker()
        return create_session(bind=self.db)

 

    




        
       