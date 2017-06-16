import pymysql
import os
import hashlib
from pymysql import OperationalError
class authentification:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456789',
                                     db='rentacars',
                                     cursorclass=pymysql.cursors.DictCursor)


    def encrypt(self, password):
        return hashlib.sha224(password).hexdigest()

    def do_login_probe(self, email, password):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `login` WHERE `email`=%s AND  `password`=%s AND `isAdmin`=%s"

                cursor.execute(sql, (email, password, 1))
                result = cursor.fetchone()
                if result == None:return False
                else:
                    self.profileid = result['id']
                    return result
        except OperationalError, e:
            # Open a file
            print e.message

    def close(self):
        self.connection.close()

    def load_brands(self):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `car_brand`"
                cursor.execute(sql)
                result = cursor.fetchall()
                if result == None:return False
                else:return result
        except OperationalError, e:
            # Open a file
            print e.message

    def add_car(self, args):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `car_brand`"
                cursor.execute(sql)
                result = cursor.fetchall()
                if result == None:
                    return False
                else:
                    return result
        except OperationalError, e:
            # Open a file
            print e.message
        finally:
            self.connection.close()
    def get_profile(self , id):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = 'SELECT * FROM staff, login WHERE `staff`.staff_id = %s'
                cursor.execute(sql , (id))
                result = cursor.fetchone()
                return result
        except OperationalError, e:
            # Open a file
            print e.message
        finally:
            self.connection.close()


if __name__ == '__main__':
    B = authentification()
    advo = B.do_login_probe("admin@gmail.com",'admin')
    print advo

    Brands = B.load_brands()
    print Brands

    #B.close()