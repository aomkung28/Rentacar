import pymysql
import os
import hashlib
from pymysql import OperationalError
class authentification:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='master',
                                     password='root',
                                     db='db_master',
                                     cursorclass=pymysql.cursors.DictCursor)
    def encrypt(self, password):
        return hashlib.sha224(password).hexdigest()

    def do_login_probe(self, email, password):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `login` WHERE `email`=%s AND  `password`=%s "

                cursor.execute(sql, (email, password))
                result = cursor.fetchone()
                if result == None:return False
                else:return result
        except OperationalError:
            # Open a file
            fd = os.open("foo.txt", os.O_RDWR | os.O_CREAT)

            # Write one string
            os.write(fd, "This is test")

            # Close opened file
            os.close(fd)
        finally:
            self.connection.close()
            return False
    def close(self):
        pass


if __name__ == '__main__':
    B = authentification()
    advo = B.do_login_probe("admin@gmail.com",'admin')
    print advo.get('username')
    print advo.get('lastlogin')
    print advo.get('id')