#munge path to include roboide code
import sys
slice_end = __file__.rfind("/");
sys.path.append(__file__[0:slice_end+1]+"../")

#include turbogears config
from turbogears import update_config
update_config(configfile="../dev.cfg",modulename="roboide.config")

import unittest
import empty_state

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromModule(empty_state))

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)

