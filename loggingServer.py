#!/usr/bin/python3
import socketserver
from datetime import datetime

def save_data(data_entry):
    f = open('server.log', 'a+')
    f.write(data_entry)
    f.write('\n')
    f.close()

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        line1 = self.rfile.readline()
        line2 = self.rfile.readline()
        line3 = self.rfile.readline()
        line4 = self.rfile.readline()
        client = self.client_address[0]
        
        save_data('%s - %s wrote:' % (datetime.now().strftime('%c'), self.client_address[0]))
        save_data('Line 1: [%s]' % line1)
        save_data('Line 2: [%s]' % line2)
        save_data('Line 3: [%s]' % line3)
        save_data('Line 4: [%s]' % line4)
        save_data('Request Finished\n')

    def sendString(self, text):
        self.wfile.write(bytes('%s\n' % text, 'UTF-8'))

if __name__ == '__main__':
    HOST, PORT = '10.0.1.23', 8000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    start_message = 'Starting to serve requests on %s at %s' % (PORT, datetime.now().strftime('%c'))
    print(start_message)
    save_data(start_message)
    print('Press Ctrl+C to stop')
    server.serve_forever()

