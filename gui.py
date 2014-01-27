import wx, re
import threading
import client

PORT = 8080

class UpdateChat(threading.Thread):
	def __init__(self, write):
		threading.Thread.__init__(self)
		self.write = write

	def run(self):
		while client.connected:
			self.write(client.message_in_buffer.get())

class Frame(wx.Frame):
	def __init__(self, parent, title):
		super(Frame, self).__init__(parent, title = title, size = (300, 500))
		self.init_gui()
		self.Centre()
		self.Show(True)

	def init_gui(self):
		self.main_panel = wx.Panel(self)
		self.conn_panel = wx.Panel(self.main_panel)
		self.chat_panel = wx.Panel(self.main_panel)
		self.talk_panel = wx.Panel(self.main_panel)

		self.init_conn_panel()
		self.init_chat_panel()
		self.init_talk_panel()

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer.Add(self.conn_panel, 0, wx.EXPAND)
		main_sizer.Add(self.chat_panel, 1, wx.EXPAND)
		main_sizer.Add(self.talk_panel, 0, wx.EXPAND)
		self.main_panel.SetSizer(main_sizer)

	def init_conn_panel(self):
		self.txConn = wx.TextCtrl(self.conn_panel)
		self.txConn.SetValue('localhost')
		btConn = wx.Button(self.conn_panel, label = 'Connect')

		connSizer = wx.BoxSizer(wx.HORIZONTAL)
		connSizer.Add(self.txConn, 1, wx.EXPAND)
		connSizer.Add(btConn)
		self.conn_panel.SetSizer(connSizer)

		self.Bind(wx.EVT_BUTTON, self.connect, btConn)

	def init_chat_panel(self):
		self.txChat = wx.TextCtrl(self.chat_panel, style = wx.TE_MULTILINE | wx.TE_READONLY)

		chatSizer = wx.BoxSizer(wx.HORIZONTAL)
		chatSizer.Add(self.txChat, 1, wx.EXPAND)
		self.chat_panel.SetSizer(chatSizer)

	def init_talk_panel(self):
		self.txTalk = wx.TextCtrl(self.talk_panel)

		talkSizer = wx.BoxSizer(wx.HORIZONTAL)
		talkSizer.Add(self.txTalk, 1, wx.EXPAND)
		self.talk_panel.SetSizer(talkSizer)

	def write_to_chat(self, message):
		self.txChat.AppendText(message + '\n')

	def validate_url(self, url):
		# from http://stackoverflow.com/questions/7160737

		regex = re.compile(
        	#r'^(?:http|ftp)s?://' # http:// or https://
        	r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        	r'localhost|' #localhost...
        	r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        	#r'(?::\d+)?' # optional port
        	r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		return regex.match(url)

	def connect(self, e):
		host = self.txConn.GetValue()

		if (self.validate_url(host) is None):
			self.write_to_chat('Invalid direction: ' + host)
		else:
			self.write_to_chat('Connecting to ' + host + ':' + str(PORT))
			client.connect(host, PORT)
			UpdateChat(self.write_to_chat).start()


if __name__ == '__main__':
	#app = wx.App(redirect=True,filename="log.txt")
	app = wx.App()
	frame = Frame(None, title='Chat')
	app.MainLoop()