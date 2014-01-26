import threading, socket, Queue

# queues are thread safe
message_in_buffer = Queue.Queue(maxsize = 0) # infinite queue size
message_out_buffer = Queue.Queue(maxsize = 0)

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
					message_in_buffer.put(line)
		print 'Logged out'
		self.conn.close()


class Send(threading.Thread):
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.conn = conn
		self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

	def run(self):
		global connected

		while connected:
			msg = message_out_buffer.get()
			self.conn.send(msg)
			if '/exit' in msg: connected = False
		self.conn.close()

def connect(host, port):
	global connected

	connected = True
	main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#main_socket.connect((socket.gethostname(), PORT))
	main_socket.connect((HOST, PORT))

	Receive(main_socket).start()
	Send(main_socket).start()

if __name__ == '__main__':
	PORT = 8080
	HOST = '127.0.0.1'
	
	connect(HOST, PORT)

	# read-only
	while connected:
		print message_in_buffer.get()

	