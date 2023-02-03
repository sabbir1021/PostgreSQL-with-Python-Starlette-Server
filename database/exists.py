from database.db import db_connect

def exists_check(value, table):
    try:
        conn = db_connect()
        cursor = conn.cursor()
        text = ' AND '.join([f"{table}.{key} = '{values}'" for key,values in value.items()])
        cursor.execute("""
            select id from {} where {}
        """.format(table, text)
        )
        count = cursor.rowcount
        conn.close()
        if count == 1:
            return True
        else:
            return False

    except Exception as e:
        print('--------------', e)
        conn.close()
        return False