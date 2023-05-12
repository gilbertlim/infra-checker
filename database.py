import psycopg2
import logging


class Database:
    def __init__(self, credential):
        self.credential = credential

    def check_connection(self):
        for dbname in self.credential.keys():
            for rw, v in self.credential[dbname].items():
                logging.info('Connecting to Database... (dbname={}, instance={}, host={}, port={})' .format(dbname, rw, v['host'], v['port']))

                try:
                    conn = psycopg2.connect(host=v['host'],
                                            dbname=dbname,
                                            user=self.credential[dbname][rw]['username'],
                                            password=self.credential[dbname][rw]['password'],
                                            port=v['port'])
                    cur = conn.cursor()
                    cur.execute('select 1')
                    rows = cur.fetchall()

                    if len(rows) > 0:
                        logging.info('Connection was successful. (dbname={}, instance={}, host={}, port={})' .format(dbname, rw, v['host'], v['port']))
                    else:
                        raise ConnectionError
                except Exception as e:
                    logging.error(e)
                    logging.error('Connection failed. (dbname={}, instance={}, host={}, port={})' .format(dbname, rw, v['host'], v['port']))

