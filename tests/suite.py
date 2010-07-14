#!/usr/bin/python

#munge path to include roboide code
import sys
slice_end = __file__.rfind("/");
sys.path.append(__file__[0:slice_end+1]+"../")

# config imports
from helpers.confighelper import global_config_helper

# Standard imports
import subprocess
import unittest
import httplib, socket, time

# Test related imports
import empty_state
import new_object_state
import project_exists_state
import dontcare_state
import file_exists_state

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromModule(empty_state))
suite.addTests(unittest.TestLoader().loadTestsFromModule(new_object_state))
suite.addTests(unittest.TestLoader().loadTestsFromModule(project_exists_state))
suite.addTests(unittest.TestLoader().loadTestsFromModule(dontcare_state))
suite.addTests(unittest.TestLoader().loadTestsFromModule(file_exists_state))

if __name__ == "__main__":
    #grab the config file
    if len(sys.argv) > 1:
        global_config_helper.update_configuration(sys.argv[1])
    else:
        sys.exit('No config file specified')

    ide_run_cmd = './start-roboide.py'
    run_proc = subprocess.Popen([ide_run_cmd, sys.argv[1]],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)

    #check that the IDE is running
    port =  global_config_helper.get('server:main.port')
    host =  global_config_helper.get('server:main.host')
    conn = httplib.HTTPConnection(host, port)
    done = False
    while not done:
        try:
            conn.connect()
            done = True
        except socket.error:
            print 'Connection refused on %s:%s. Waiting for the IDE to start.' % (host, port)
            print 'Retrying connection.'
            time.sleep(2)
    conn.close()

    #Run the tests
    unittest.TextTestRunner(verbosity=2).run(suite)

    # Kill the IDE process.
    run_proc.terminate()
    run_proc.wait()
