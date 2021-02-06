import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import CommentObj

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "2357"

class Comment(baseClass):
    def __init__(self):
        super().__init__("COMMENT", CommentObj)

    def add(self, comment):
        query = "INSERT INTO COMMENT (CUSTOMER_ID, EQ_ID, COMMENT_TITLE, COMMENT_STATEMENT) VALUES (%s, %s, %s, %s) RETURNING CUSTOMER_ID"
        fill = (comment.customer_id, comment.eq_id, comment.comment_title, comment.comment_statement)
        self.execute(query, fill)

    def update(self, comment_id, comment):
        query = "UPDATE COMMENT SET CUSTOMER_ID = %s, EQ_ID = %s, COMMENT_TITLE = %s, COMMENT_STATEMENT = %s, UPDATED_TIME = CURRENT_TIMESTAMP WHERE COMMENT_ID = %s"
        fill = (comment.customer_id, comment.eq_id, comment.comment_title, comment.comment_statement, comment_id)
        self.execute(query, fill)

    def delete(self, comment_key):
        query = "DELETE FROM COMMENT WHERE COMMENT_ID = %s"
        fill = (comment_key,)
        self.execute(query, fill)

    def get_row(self, comment_key):
        _comment = None

        query = "SELECT * FROM COMMENT WHERE COMMENT_ID = %s"
        fill = (comment_key,)

        with dbapi2.connect(dbname=DB_NAME,host=DB_HOST,user=DB_USER,password=DB_PASS) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            comment = cursor.fetchone()
            if comment is not None:
                _comment = CommentObj(comment[1], comment[2], comment[3], comment[4], added_time=comment[5], updated_time=comment[6], comment_id=comment[0])

        return _comment

    def get_table(self, eq_id=None):
        comments = []

        query = "SELECT * FROM COMMENT"
        if eq_id:
            query += " WHERE EQ_ID = %s"
            fill = (eq_id,)

        with dbapi2.connect(dbname=DB_NAME,host=DB_HOST,user=DB_USER,password=DB_PASS) as connection:
            cursor = connection.cursor()
            if eq_id:
                fill = (eq_id)
                cursor.execute(query, fill)
            else:
                cursor.execute(query)
            for comment in cursor:
                comment_ = CommentObj(customer_id = comment[1], eq_id = comment[2], comment_title=comment[3], comment_statement =comment[4], added_time=comment[5], updated_time=comment[6], comment_id=comment[0])
                comments.append(comment_)
            cursor.close()

        return comments