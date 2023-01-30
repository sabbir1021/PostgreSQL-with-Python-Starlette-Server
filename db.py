import psycopg2
import psycopg2.extras
from paginations import pagination

def db_connect():
   conn = psycopg2.connect(
      database="blog", user='sabbir1021', password='sabbir1021', host='localhost', port= '5432'
   )
   return conn


def view_all(sql, table, page_size, page):
   conn = db_connect()
   cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
   
   # count
   count_sql = """SELECT COUNT(*) FROM {};""".format(table)
   cursor.execute(count_sql)
   count = cursor.fetchone().get('count')

   # pagination 
   pagination_data = pagination(page_size, page, count)
   sql = sql+pagination_data.get('query')

   # Query
   cursor.execute(sql)
   all_data = cursor.fetchall()

   
   data = {}
   meta_data = {
      "total": count,
      "page_size": pagination_data.get('page_size'),
      "page": pagination_data.get('page'),
      "next_page": pagination_data.get('next_page'),
      "previous_page" : pagination_data.get('previous_page')
   }
   data['success'] = True
   data['meta_data'] = meta_data
   data['data'] = all_data
   conn.close()
   return data


def view_details(sql, data_type='all'):
   conn = db_connect()
   cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
   cursor.execute(sql)
   get_data = cursor.fetchone()
   data = {}
   data['success'] = True
   data['data'] = get_data
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
