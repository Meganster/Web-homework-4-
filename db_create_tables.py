import connection


class Author:
    def __init__(self):
        self.connection = connection.Connection(host="localhost", db_name="ask_db", user="'yury'", password="89096547567")

    def create(self):
        with self.connection as c:
            cursor = c.cursor()
                #cursor.execute("""drop table ask_app_question""")
                #c.commit()
            cursor.execute("""create table
                ask_app_question (
                id INT(11) NOT NULL AUTO_INCREMENT,
                title CHAR(100) NOT NULL,
                author_id INT,
                text TEXT,
                create_date DATE,
                likes INT,
                FOREIGN KEY (author_id) REFERENCES grow_author(id),
                PRIMARY KEY(id)
                )""")
            c.commit()



author = Author()
# needed for first start of program
author.create()
