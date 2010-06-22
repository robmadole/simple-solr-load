"""
=======================
Simple Solr load tester
=======================

Puts a load on a Solr server until CTRL-C is pressed.  The wait time between
requests can be controlled with INTERVAL and the query used can be modified by
editing the query.txt file
"""
from os.path import dirname, join
from urllib import quote_plus
import sys
from httplib import HTTPConnection
import string
import time
import optparse

TIMEOUT = 10.0   # Timeout on the HTTP connection

parser = optparse.OptionParser()

parser.add_option('-q', '--query', dest='query', default='insurance',
    help='What to search for')
parser.add_option('--template', dest='query_template_file',
    default='query.txt', help='Where to get the query template file, defaults '
    'to query.txt in the same directory as load.py')
parser.add_option('-H', '--host', dest='host', default='localhost',
    help='The hostname Solr is running on, default localhost')
parser.add_option('-p', '--port', dest='port', default='8983',
    help='The port the the server is running on, default 8983')
parser.add_option('-i', '--interval', dest='interval', default='1.0',
    help='How long to wait between requests')
parser.add_option('-t', '--timeout', dest='timeout', default='10',
    help='How long to wait before the HTTP connection times out')


def run(query='insurance', query_template_file='query.txt', host='localhost',
        port='8953', interval='1.0', timeout='10'):
    with open(join(dirname(__file__), query_template_file)) as fh:
        url = string.Template(fh.read()).substitute(
            host=host,
            port=port,
            query=quote_plus(query))

    print 'Starting load'

    con = HTTPConnection(host, port, timeout=float(timeout))

    while True:
        try:
            con.request('GET', url)
            sys.stdout.write('.')
            sys.stdout.flush()
            response = con.getresponse()
            time.sleep(float(interval))
        except KeyboardInterrupt:
            break

    print '\nEnd'


if __name__ == '__main__':
    options, args = parser.parse_args()
    run(**options.__dict__)
