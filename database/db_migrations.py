import psycopg2

conn = psycopg2.connect(
   database="blog", user='sabbir1021', password='sabbir1021', host='localhost', port= '5432'
)

cursor = conn.cursor()


cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL NOT NULL PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            phone VARCHAR(50),
            email VARCHAR(50)
        );
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_categories (
            id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            created_by INT NOT NULL,
            show_in BOOLEAN NOT NULL,
            CONSTRAINT fk_created_by FOREIGN KEY(created_by) REFERENCES users(id)
            
        );
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_tags (
            id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            created_by INT NOT NULL,
            show_in BOOLEAN NOT NULL,
            CONSTRAINT fk_created_by FOREIGN KEY(created_by) REFERENCES users(id)
        );
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id SERIAL NOT NULL PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            description text NOT NULL,
            thumbnail VARCHAR(255) NOT NULL,
            category INT NOT NULL,
            created_by INT NOT NULL,
            show_in BOOLEAN NOT NULL,
            publish_date timestamp with time zone DEFAULT now(),

            CONSTRAINT fk_category FOREIGN KEY(category) REFERENCES blog_categories(id),
            CONSTRAINT fk_created_by FOREIGN KEY(created_by) REFERENCES users(id)
        );
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs_tags (
            id SERIAL NOT NULL PRIMARY KEY,
            blog INT NOT NULL,
            tag INT NOT NULL,

            CONSTRAINT fk_blog FOREIGN KEY(blog) REFERENCES blogs(id),
            CONSTRAINT fk_tag FOREIGN KEY(tag) REFERENCES blog_tags(id)
        );
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_comment (
            id SERIAL NOT NULL PRIMARY KEY,
            blog INT NOT NULL,
            name VARCHAR(50),
            phone VARCHAR(50),
            email VARCHAR(50),
            comment text NOT NULL,
            created_at timestamp with time zone DEFAULT now(),
            show_in BOOLEAN NOT NULL DEFAULT TRUE,
            
            CONSTRAINT fk_blog FOREIGN KEY(blog) REFERENCES blogs(id)
        );
    """)


# cursor.execute("""
#         CREATE TABLE IF NOT EXISTS blog_comment_reply (
#             id BIGINT,
#             username VARCHAR(50),
#             phone VARCHAR(50),
#             email VARCHAR(50),
#             PRIMARY KEY (id)
#         );
#     """)



conn.commit()

conn.close()