
import asyncore
from smtpd import SMTPServer
import pymongo

class PDebuggingServer(SMTPServer):
	M = pymongo.Connection()
	# Do something with the gathered message
	def process_message(self, peer, mailfrom, rcpttos, data):

		lines = data.split('\n')
		print '---------- MESSAGE FOLLOWS ----------'
		for line in lines:
			# headers first
			print line

		print '------------ END MESSAGE ------------'

	def sendmail(self, mailfrom, mailto, string):
		#self.process_message( mailto, mailfrom, [], string)
		self.M.db.fakesmtp.insert( {'from':mailfrom, 'to':mailto, 'data':string}, safe=True)

if __name__ == '__main__':
    PDebuggingServer( ('localhost',25), ('localhost',25))
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
