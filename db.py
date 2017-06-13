import pymysql

class mdb:
    def test(self):

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='user',
                                     password='passwd',
                                     db='db',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `user` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            connection.close()

def main():
    query = ("SELECT first_name, last_name, hire_date FROM employees "
     "WHERE hire_date BETWEEN %s AND %s")
    try:
      cnx = mysql.connector.connect(user='root', password='123456789',
                             host='127.0.0.1',
                             database='rentacar')
      do_login(cnx, "admin@gmail.com", "admin")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
      cnx.close()
      
def do_login(cnx, email, password):
    query = ("SELECT * FROM login where email=%s AND password=%s".format(email, password))
    print query

    cursor = cnx.cursor()
    cursor.execute(query, (email,password))
    
    for e in cursor:
      print(e)   
if __name__ == '__main__':
   main()
    
    