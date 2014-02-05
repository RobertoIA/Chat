import wx, re
import threading
from client import Client

PORT = 8080

class UpdateChat(threading.Thread):
	def __init__(self, write, client):
		threading.Thread.__init__(self)
		self.write = write
		self.client = client

	def run(self):
		while self.client.connected:
			self.write(self.client.in_buffer.get())

class Frame(wx.Frame):
	def __init__(self, parent, title):
		super(Frame, self).__init__(parent, title=title, size=(300, 500))
		self.client = None
		self.last_user = None
		self.init_gui()
		self.Bind(wx.EVT_CLOSE, self.close)
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
		self.btConn = wx.Button(self.conn_panel, label='Connect')

		connSizer = wx.BoxSizer(wx.HORIZONTAL)
		connSizer.Add(self.txConn, 1, wx.EXPAND)
		connSizer.Add(self.btConn)
		self.conn_panel.SetSizer(connSizer)

		self.Bind(wx.EVT_BUTTON, self.connect_disconnect, self.btConn)

	def init_chat_panel(self):
		self.txChat = wx.TextCtrl(self.chat_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

		chatSizer = wx.BoxSizer(wx.HORIZONTAL)
		chatSizer.Add(self.txChat, 1, wx.EXPAND)
		self.chat_panel.SetSizer(chatSizer)

	def init_talk_panel(self):
		self.txTalk = wx.TextCtrl(self.talk_panel, style=wx.TE_PROCESS_ENTER)
		self.txTalk.SetFocus()

		talkSizer = wx.BoxSizer(wx.HORIZONTAL)
		talkSizer.Add(self.txTalk, 1, wx.EXPAND)
		self.talk_panel.SetSizer(talkSizer)
		
		self.txTalk.Bind(wx.EVT_KEY_DOWN, self.send_message)

	def write_to_chat(self, message):
		user = message[:message.find(':')]
		if self.last_user and self.last_user == user:
			self.txChat.AppendText('\t' + message[message.find(':') + 2:] + '\n')
		else:
			self.txChat.AppendText(message + '\n')
		self.last_user = user

	def send_message(self, event):
		if self.client and self.client.connected and event.GetKeyCode() == wx.WXK_RETURN:
			message = self.txTalk.GetValue()
			self.txTalk.Clear()
			self.client.out_buffer.put(message)
		else:
			event.Skip()
			
	def close(self, event):
		if self.client and self.client.connected:
			self.client.disconnect()
		event.Skip()

	def validate_url(self, url):
		# from http://stackoverflow.com/questions/7160737

		regex = re.compile(
        	# r'^(?:http|ftp)s?://' # http:// or https://
        	r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        	r'localhost|'  # localhost...
        	r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        	# r'(?::\d+)?' # optional port
        	r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		return regex.match(url)

	def connect_disconnect(self, e):
		if not self.client or not self.client.connected:
			host = self.txConn.GetValue()
			
			self.client = Client(host, PORT)
	
			if (self.validate_url(host) is None):
				self.write_to_chat('Invalid direction: ' + host)
			else:
				self.write_to_chat('Connecting to ' + host + ':' + str(PORT))
				self.client.connect()
				UpdateChat(self.write_to_chat, self.client).start()
			self.btConn.SetLabel('Disconnect')
			self.txConn.Disable()
			self.txTalk.SetFocus()
		else:
			self.write_to_chat('Logged out.\n')
			self.client.disconnect()
			self.btConn.SetLabel('Connect')
			self.txConn.Enable()
			self.txTalk.SetFocus()


if __name__ == '__main__':
	# app = wx.App(redirect=True,filename="log.txt")
	app = wx.App()
	frame = Frame(None, title='Chat')
	app.MainLoop()
