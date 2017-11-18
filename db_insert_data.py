import connection


class Author:
    def __init__(self, first_name, last_name, about, email, phone_number):
        self.connection = connection.Connection(host="localhost", db_name="ask_db", user="'yury'", password="89096547567")
        self.first_name = first_name
        self.last_name = last_name
        self.about = about
        self.email = email
        self.phone_number = phone_number

    def create(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""create table
                grow_author (
                id INT(11) NOT NULL AUTO_INCREMENT,
                firstName CHAR(30) NOT NULL,
                lastName CHAR(30) NOT NULL,
                about TEXT,
                email CHAR(50) NOT NULL,
                phone_number CHAR(50),
                PRIMARY KEY(id)
                )""")
            c.commit()
            cursor.execute("""create table
                grow_article (
                id INT(11) NOT NULL AUTO_INCREMENT,
                title CHAR(100) NOT NULL,
                author_id INT,
                content TEXT,
                snippet TEXT,
                pubdate DATE,
                likes INT,
                FOREIGN KEY (author_id) REFERENCES grow_author(id),
                PRIMARY KEY(id)
                )""")
            c.commit()
    
    def save(self):
        with self.connection as con:
            cursor = con.cursor()
            cursor.execute("""insert into ask_app_question (title, author_id, text, create_date, likes)
                values ("Animals", 1, "Exmaple of content", "1997-03-23", 11)""")
            con.commit()



author = Author("Alex", "Klein", "Photographer, traveller", "alex@klein.com", "467214")
# needed for first start of program
#author.create()
author.save()
