import threading, socket

class ClientManager(threading.Thread):
	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr

	def run(self):
		global clients

		clients.append(self.conn)

		conn_alert = 'Connected ' + self.addr[0] + '/' + str(self.addr[1])
		print conn_alert
		self.conn.send('Connected to chat')
		self.conn.send('Users: ' + str(len(clients)))
		for client in clients:
			if client is not self.conn: client.send(conn_alert)

		connected = True
		while connected:
			msg = str(self.conn.recv(1024)).split('\n')
			for line in msg:
				if line != '':
					if '/exit' in line:
						connected = False
						clients.remove(self.conn)
						self.conn.send('/exit')
						for client in clients:
							logout_alert = self.addr[0] + '/' + str(self.addr[1]) + ' logged out'
							if client is not self.conn: client.send(logout_alert)
					else:
						response = self.addr[0] + '/' + str(self.addr[1]) + ' : ' + line
						for client in clients:
							if client is not self.conn: client.send(response)

		print self.addr[0] + '/' + str(self.addr[1]) + ' logout'
		self.conn.close()

if __name__ == '__main__':
	PORT = 8080
	clients = []

	main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#main_socket.bind((socket.gethostname(), PORT))
	main_socket.bind(('', PORT))
	main_socket.listen(5)

	print 'Starting server at port ' + str(PORT)

	while True:
		conn, addr = main_socket.accept()
		ClientManager(conn, addr).start()