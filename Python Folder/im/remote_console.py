from im import Server
import sys

class RemoteConsole(Server):
	
	def post(self, msg, client):
		
		self.log.append(msg)
		try:
			exec msg
			s = """Command "%s" recieved from client "%s" """ % (msg, client.name)
		except:
			s = "Invalid command: " + msg + " from client " + client.name
			print sys.excepthook(*sys.exc_info())
		print s
		
		for c in self.clients:
			c.post(s)

def main():
	RemoteConsole().start()

if __name__ == '__main__':
	main()