import unittest
from unittest.mock import patch

import threading
import socket
import time
import json

from server import Master
from client import URLClient


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master = Master('localhost', 5001, 2, 3)
        cls.server_thread = threading.Thread(target=cls.master.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        time.sleep(0.1)

    def test_single_request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 5001))

        test_url = "http://example.com"
        s.sendall(test_url.encode('utf-8'))

        response = s.recv(4096).decode('utf-8')
        result = json.loads(response)

        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) <= 3)

        s.close()

    @patch('builtins.print')
    @patch('builtins.open')
    def test_client_server_interaction(self, mock_open, mock_print):
        mock_file = ["http://example.com\n", "http://test.com\n"]
        mock_open.return_value.__enter__.return_value = mock_file

        client = URLClient('localhost', 5001, 2, 'URLS.txt')
        client.start()

        self.assertTrue(mock_print.called)

    @patch('builtins.open')
    def test_parallel_processing(self, mock_open):
        mock_open.return_value.__enter__.return_value = [
            "http://test1.com\n", "http://test2.com\n",
            "http://test3.com\n", "http://test4.com\n",
            "http://test5.com\n",
        ]

        with patch('server.requests.get') as mock_get:
            mock_get.return_value.text = "test"

            start_time = time.time()
            client = URLClient('localhost', 5002, 5, 'urls.txt')
            client.start()
            elapsed = time.time() - start_time

            self.assertLess(elapsed, 0.5)


if __name__ == '__main__':
    unittest.main()
