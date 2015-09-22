#!/usr/bin/python3
import sys
import socketserver
import argparse
from datetime import datetime

CONTENT_LENGTH = 'content-length'
ENCODING = 'utf-8'
DEFAULT_PORT = 8000
DEFAULT_HOST = 'localhost'

def save_data(data_entry):
    f = open('server.log', 'a+')
    f.write(data_entry)
    f.write('\n')
    f.close()

def save_print(message):
    print(message)
    save_data(message)

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = self.client_address[0]
        save_data('%s - %s wrote:' % (datetime.now().strftime('%c'), client))
        try:
            headers = self.read_headers()
        except KeyboardInterrupt:
            save_print('\nServer was asked to terminate this request')
            return

        save_data('Current parsed headers are %s' % headers)
        if CONTENT_LENGTH in headers:
            self.read_request_data(headers)

        save_data('Request Finished\n')

    def read_headers(self):
        headers = {}    
        line = self.rfile.readline()
        line_number = 0
        while True:                
            save_data('Line %d: [%s]' % (line_number, line))
            self.save_known_header(headers, line)
            line_number += 1
            line = self.rfile.readline()

            if self.is_end_of_headers(line):
                save_data('Line %d was empty, headers finished.' % line_number)
                break
        return headers

    def save_known_header(self, headers, line):
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
    parser = argparse.ArgumentParser(description='A small HTTP server that logs requests into a log file.')
    parser.add_argument('-port', type=int, default=DEFAULT_PORT, 
                        help='port number (default: %s)' % DEFAULT_PORT, dest='port_number')
    parser.add_argument('-host', default=DEFAULT_HOST,
                        help='host to listen on (default: %s)' % DEFAULT_HOST, dest='host')
    args = parser.parse_args()

    server = socketserver.TCPServer((args.host, args.port_number), MyTCPHandler)
    server.timeout = 5
    save_print('Starting to serve requests on %s at %s' % (args.port_number, datetime.now().strftime('%c')))
    print('Press Ctrl+C to stop')
    while True:
        try:
            server.handle_request()
        except KeyboardInterrupt:
            save_print('\nServer was asked to shutdown')
            break
        except:
            save_print('Got exception: %s' % sys.exc_info()[0])
            break
