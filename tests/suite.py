#!/usr/bin/python

#munge path to include roboide code
import sys
slice_end = __file__.rfind("/");
sys.path.append(__file__[0:slice_end+1]+"../")

from turbogears import update_config, config

import unittest
import empty_state
import new_object_state
import httplib, socket, time

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromModule(empty_state))
suite.addTests(unittest.TestLoader().loadTestsFromModule(new_object_state))

if __name__ == "__main__":
    #grab the config file
    if len(sys.argv) > 1:
        update_config(configfile=sys.argv[1],modulename="roboide.config")
    else:
        sys.exit('No config file specified')

    #check that the IDE is running
    port =  config.get('server.socket_port')
    host =  config.get('server.socket_host')
    conn = httplib.HTTPConnection(host, port)
    done = False
    while not done:
        try:
            conn.connect()
            done = True
        except socket.error:
            print 'Connection refused on %s:%s. Is the IDE running?' % (host, port)
            print 'Retrying connection.'
            time.sleep(2)
    conn.close()

    #Run the tests
    unittest.TextTestRunner(verbosity=2).run(suite)

