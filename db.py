import psycopg2
import psycopg2.extras

def db_connect():
   conn = psycopg2.connect(
      database="blog", user='sabbir1021', password='sabbir1021', host='localhost', port= '5432'
   )
   return conn


def view(sql, data_type='all'):
   conn = db_connect()
   cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
   cursor.execute(sql)
   if data_type == "one":
      data = cursor.fetchone()
   else:
      data = cursor.fetchall()
   conn.close()
   return data


def create(sql):
   conn = db_connect()
   cursor = conn.cursor()
   cursor.execute(sql)
   conn.commit()
   conn.close()
   return {"message": "created"}


def update(sql):
   conn = db_connect()
   cursor = conn.cursor()
   cursor.execute(sql)
   conn.commit()
   conn.close()
   return {"message": "created"}
