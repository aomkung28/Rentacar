import mysql.connector
from mysql.connector import errorcode
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
    
    