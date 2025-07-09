import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/utils')

from logger import Logger, log_execution_time

class TestLogger(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.logger = Logger('test_logger')
    
    def test_logger_creation(self):
        self.assertIsNotNone(self.logger)
        self.assertEqual(len(self.logger.logger.handlers), 2)
    
    def test_log_levels(self):
        with patch.object(self.logger.logger, 'debug') as mock_debug:
            self.logger.debug('test debug')
            mock_debug.assert_called_once_with('test debug')
        
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.info('test info')
            mock_info.assert_called_once_with('test info')
    
    def test_log_execution_time_decorator(self):
        @log_execution_time
        def slow_function():
            import time
            time.sleep(0.1)
            return "done"
        
        with patch.object(self.logger, 'info') as mock_info:
            result = slow_function()
            self.assertEqual(result, "done")
            # Check that info was called with execution time
            self.assertTrue(mock_info.called)
    
    def tearDown(self):
        # Clean up
        if os.path.exists('logs'):
            import shutil
            shutil.rmtree('logs')

if __name__ == '__main__':
    unittest.main()