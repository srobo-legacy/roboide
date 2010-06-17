#!/usr/bin/python

#munge path to include roboide code
import sys
slice_end = __file__.rfind("/");
sys.path.append(__file__[0:slice_end+1]+"../")

#include turbogears config
from turbogears import update_config
update_config(configfile="../dev.cfg",modulename="roboide.config")

import unittest
import empty_state
import new_object_state
import httplib, socket, time

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromModule(empty_state))
suite.addTests(unittest.TestLoader().loadTestsFromModule(new_object_state))

if __name__ == "__main__":
    conn = httplib.HTTPConnection("localhost:8080")
    done = False
    while not done:
        try:
            conn.connect()
            done = True
        except socket.error:
            print 'Connection refused on localhost:8080. Is the IDE running?'
            print 'Retrying connection.'
            time.sleep(2)
    conn.close()

    unittest.TextTestRunner(verbosity=2).run(suite)

