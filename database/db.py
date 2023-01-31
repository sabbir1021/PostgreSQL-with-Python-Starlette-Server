import psycopg2
import psycopg2.extras
from base.paginations import pagination

def db_connect():
   conn = psycopg2.connect(
      database="blog", user='sabbir1021', password='sabbir1021', host='localhost', port= '5432'
   )
   return conn


def view_all(sql, table, page_size=None, page=None, search=None, search_fields=None):
   conn = db_connect()
   cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

   # search
   if search:
      search = search.upper()
      search_field_text = ""
      for i in range(0,len(search_fields)):
         if i != len(search_fields) - 1:
            search_field_text = search_field_text + f"UPPER({search_fields[i]}) LIKE '%{search}%' OR "
         else:
            search_field_text = search_field_text + f"UPPER({search_fields[i]}) LIKE '%{search}%' "

      q = f" WHERE {search_field_text}"
      sql = sql+q
   else:
      q = ""
   
   # count
   count_sql = """SELECT COUNT(*) FROM {} """.format(table)
   count_sql = count_sql + q
   cursor.execute(count_sql)
   count = cursor.fetchone().get('count')

   # pagination 
   pagination_data = pagination(page_size, page, count)
   
   # Error check
   if pagination_data.get('status') !=200:
      return pagination_data

   sql = sql+pagination_data.get('query')


   print(sql)
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


def create(query, values):
   conn = db_connect()
   cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
   try:
      cursor.execute(query, values)
      data = cursor.fetchone()
   except Exception as e:
      conn.close()
      return {"message": str(e), "status": 400}
   conn.commit()
   conn.close()
   return {"message": "Created", "data": data }


def update(sql):
   conn = db_connect()
   cursor = conn.cursor()
   cursor.execute(sql)
   conn.commit()
   conn.close()
   return {"message": "Updated"}
