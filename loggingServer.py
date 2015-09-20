#!/usr/bin/python3
import sys
import socketserver
from datetime import datetime

CONTENT_LENGTH = 'content-length'
ENCODING = 'utf-8'

def save_data(data_entry):
    f = open('server.log', 'a+')
    f.write(data_entry)
    f.write('\n')
    f.close()

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        headers = {}
        client = self.client_address[0]
        save_data('%s - %s wrote:' % (datetime.now().strftime('%c'), client))
        try:
            line = self.rfile.readline()
            line_number = 0
            while True:                
                save_data('Line %d: [%s]' % (line_number, line))
                self.read_known_header(headers, line)
                line_number += 1
                line = self.rfile.readline()
                if self.is_end_of_headers(line):
                    save_data('Line %d was empty, headers finished.' % line_number)
                    break

            save_data('Current parsed headers are %s' % headers)
            if CONTENT_LENGTH in headers:
                self.read_request_data(headers)
        except:
           print('Got exception: %s' % sys.exc_info()[0])
           save_data('Got exception: %s' % sys.exc_info()[0])

        save_data('Request Finished\n')

    def read_known_header(self, headers, line):
        known_headers = [CONTENT_LENGTH]
        line_str = line.decode(ENCODING)
        split_header = line_str.split(':')
        header_key = split_header[0].lower()
        if header_key in known_headers:
            header_value = split_header[1].strip()
            save_data('Header %s was known, saving value [%s]' % (header_key, header_value))
            headers[header_key] = header_value

    def is_end_of_headers(self, line):
        return line.decode(ENCODING).strip() is ''

    def read_request_data(self, headers):
        bytes_to_read = int(headers[CONTENT_LENGTH])
        save_data('Trying to read %d bytes of data...' % bytes_to_read)
        request_data = self.rfile.read(bytes_to_read)
        save_data('Received data [%s]' % request_data)

if __name__ == '__main__':
    HOST, PORT = '10.0.1.23', 8000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.timeout = 5
    start_message = 'Starting to serve requests on %s at %s' % (PORT, datetime.now().strftime('%c'))
    print(start_message)
    save_data(start_message)
    print('Press Ctrl+C to stop')
    while True:
        server.handle_request()

