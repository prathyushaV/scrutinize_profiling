import MySQLdb as mdb

class MySQLInterface():
	def __init__(self, host, database, user, password):
		self.host = host
		self.database = database
		self.user = user
		self.password = password

	def get_nodes(self, nodetype):
		connection = mdb.connect(self.host, self.user, self.password, self.database)
		cursor = connection.cursor()
		cursor.execute("select * from " + nodetype )
		rows = cursor.fetchall()
		return rows	
#added by prathyusha
	def get_rows(self, nodetype):
                connection = mdb.connect(self.host, self.user, self.password, self.database)
                cursor = connection.cursor()
                print type(nodetype)
                cursor.execute("select data from "+nodetype+" where task_uuid = (select task_uuid from "+nodetype+" order by created_at DESC limit 1)" )
                rows = cursor.fetchall()
                return rows
	

"""if __name__=='__main__':
    mysql_interface = MySQLInterface("localhost", "sys_manager_db", "root", "pass");
    print mysql_interface.get_nodes("event_collectors")
    mysql_interface.insert_nodes("enodebs", "11.11.11.11", "uuuiiid", "22.22.22.22")
"""
