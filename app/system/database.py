import mysql.connector

class connector_db:


     def __init__(self, host, port,user,password,database):
        
         self.mysql_user = host
         self.mysql_port = port
         self.mysql_user = user
         self.mysql_password = password
         self.mysql_host = database
        



     def create_connection(self):
        
        
         return  mysql.connector.connect(user=self.mysql_user, password=self.mysql_password,host= self.mysql_host,database= self.mysql_host)
            
          


