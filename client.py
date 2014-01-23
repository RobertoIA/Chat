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
				if line != '' and '/exit' not in line:
					print line
		print 'Logged out'
		self.conn.close()


class Send(threading.Thread):
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.conn = conn

	def run(self):
		global connected

		while connected:
			msg = raw_input('')
			self.conn.send(msg)
			if '/exit' in msg: connected = False
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