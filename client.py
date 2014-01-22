import threading, socket

class Receive(threading.Thread):
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.conn = conn

	def run(self):
		global connected
		while connected:
			msg = str(self.conn.recv(1024)).split('\n')
			for line in msg:
				if line != '':
					if 'EXIT' in line:
						connected = False
					else:
						print line
		print 'logout'
		self.conn.close()

class Send(threading.Thread):
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.conn = conn

	def run(self):
		global connected
		while connected:
			msg = raw_input('')
			# connection may be interrupted while waiting for input
			if connected: self.conn.send(msg)
		self.conn.close()


if __name__ == '__main__':
	PORT = 8080
	HOST = '127.0.0.1'
	connected = True

	main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#main_socket.connect((socket.gethostname(), PORT))
	main_socket.connect((HOST, PORT))

	Receive(main_socket).start()
	Send(main_socket).start()