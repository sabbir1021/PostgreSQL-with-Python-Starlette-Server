import psycopg2
conn = psycopg2.connect(
   database="blog", user='sabbir1021', password='sabbir1021', host='localhost', port= '5432'
)

cursor = conn.cursor()

import random
import factory
from faker import Faker
fake = Faker()

# User 
# try:
#     for i in range(0,200):
#         username = fake.user_name()
#         phone = fake.user_name()
#         sql = '''INSERT INTO users(username, phone, email) VALUES ('{}', '01758514752', 'sab@gmail.com')'''.format(username)
#         cursor.execute(sql)
# except Exception as e:
#     print(e)


# Blog Category 
try:
    for i in range(0,500):
        name = fake.last_name()
        user = random.randrange(990, 1600)
        sql = '''INSERT INTO blog_categories(name, created_by, show_in) VALUES ('{}', {}, true)'''.format(name, user)
        cursor.execute(sql)
except Exception as e:
    print(e)


# Blog tag 
# try:
#    for i in seeder.tags:
#       sql = '''INSERT INTO blog_tags(name, created_by, show_in) VALUES ('{}', 1, true)'''.format(i)
#       cursor.execute(sql)
# except Exception as e:
#     print(e)


# Blog 
# try:
#    for i in seeder.blogs:
#       sql = '''INSERT INTO blogs(title, description, thumbnail, category, created_by, show_in, publish_date)
#        VALUES ('{}','{}','https://google.com', {}, 1, true, '2023-01-22 10:00:00')'''.format(i[0],i[1],i[3])
#       cursor.execute(sql)
# except Exception as e:
#     print(e)


# blogs tags
# try:
#     cursor.execute('''INSERT INTO blogs_tags(blog, tag) 
#         VALUES 
#         (1,1),
#         (1,5),
#         (2,4),
#         (2,5),
#         (3,3),
#         (4,1),
#         (4,3)
#         ''')
# except Exception as e:
#     print(e)

conn.commit()
conn.close()
