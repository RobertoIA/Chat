import threading, socket, Queue

class Receive(threading.Thread):
	def __init__(self, conn, client):
		threading.Thread.__init__(self)
		self.conn = conn
		self.client = client
		self.buffer = client.in_buffer

	def run(self):
		while self.client.connected:
			msg = str(self.conn.recv(1024)).split('\n')
			for line in msg:
				if line != '' and '/exit' not in line:
					self.buffer.put(line)
		self.conn.close()


class Send(threading.Thread):
	def __init__(self, conn, client):
		threading.Thread.__init__(self)
		self.conn = conn
		self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.client = client
		self.buffer = client.out_buffer

	def run(self):
		while self.client.connected:
			msg = self.buffer.get()
			self.conn.send(msg)
			if '/exit' in msg: self.client.connected = False
		self.conn.close()

class Client:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		
		# queues are thread safe
		self.in_buffer = Queue.Queue(maxsize=0)  # infinite queue size
		self.out_buffer = Queue.Queue(maxsize=0)
		
		self.connected = False
		
	def connect(self):	
		self.connected = True
		main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		main_socket.connect((self.host, self.port))
	
		Receive(main_socket, self).start()
		Send(main_socket, self).start()
	
	def disconnect(self):
		self.connected = False
		self.out_buffer.put('/exit')

if __name__ == '__main__':
	pass
	
