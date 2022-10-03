import unittest

loader = unittest.TestLoader()
start_dir = "src/test"
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)
