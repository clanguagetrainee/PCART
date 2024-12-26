import unittest

suite=unittest.defaultTestLoader.discover("Test","test*.py")
with open("test_report.txt","a") as f:
    runer=unittest.TextTestRunner(stream=f,verbosity=2)
    runer.run(suite)