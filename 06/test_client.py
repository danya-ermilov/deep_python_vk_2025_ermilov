import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import queue
import socket
import json

from client import URLProcessor, URLClient


class TestURLProcessor(unittest.TestCase):
    @patch('client.socket.socket')
    def test_run_success(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_client_socket = MagicMock()

        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.__enter__.return_value = mock_client_socket

        response_data = {'test': 5}
        mock_client_socket.recv.return_value = json.dumps(response_data).encode('utf-8')

        url_queue = queue.Queue()
        url_queue.put("http://example.com")
        url_queue.put(None)

        processor = URLProcessor(1, url_queue, 'localhost', 5000)
        processor.start()

        url_queue.join()

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_client_socket.connect.assert_called_once_with(('localhost', 5000))
        mock_client_socket.sendall.assert_called_once_with(b'http://example.com')
        mock_client_socket.close.assert_not_called()


class TestURLClient(unittest.TestCase):
    @patch('client.URLProcessor')
    @patch('builtins.open')
    def test_empty_file(self, mock_open, _):
        mock_file = StringIO("")
        mock_open.return_value = mock_file

        client = URLClient('localhost', 5000, 2, 'empty.txt')
        client.start()

        self.assertEqual(client.url_queue.qsize(), 2)


if __name__ == '__main__':
    unittest.main()
