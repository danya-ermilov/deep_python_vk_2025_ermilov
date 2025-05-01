import unittest
from unittest.mock import patch, MagicMock
import threading
import queue
import socket
import json
import time

from server import Worker, Master


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.k = 3
        self.worker = Worker(1, self.task_queue, self.result_queue, self.k)

    @patch('server.requests.get')
    @patch('server.BeautifulSoup')
    def test_process_url_success(self, mock_soup, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body>test test word word word</body></html>"
        mock_get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_soup_instance.get_text.return_value = "test test word word word"
        mock_soup.return_value = mock_soup_instance

        result = self.worker.process_url("http://example.com")

        expected = {'word': 3, 'test': 2}
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with("http://example.com", timeout=5)

    @patch('server.requests.get')
    def test_process_url_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        with self.assertRaises(Exception):
            self.worker.process_url("http://example.com")

    @patch('server.Worker.process_url')
    def test_run_success(self, mock_process):
        mock_process.return_value = {'test': 1}
        mock_socket = MagicMock(spec=socket.socket)

        self.task_queue.put((mock_socket, "http://example.com"))

        self.worker.daemon = True
        self.worker.start()

        time.sleep(0.1)

        mock_process.assert_called_once_with("http://example.com")
        mock_socket.sendall.assert_called_once_with(
            json.dumps({'test': 1}).encode('utf-8'))
        mock_socket.close.assert_called_once()
        self.assertEqual(self.result_queue.get(), 1)


class TestMaster(unittest.TestCase):
    @patch('server.socket.socket')
    def test_master_start(self, mock_socket):
        mock_server_socket = MagicMock()
        mock_client_socket = MagicMock()

        mock_socket.return_value = mock_server_socket
        mock_server_socket.accept.return_value = (mock_client_socket, ('127.0.0.1', 12345))

        master = Master('localhost', 5000, 1, 3)
        master.task_queue = queue.Queue()

        master_thread = threading.Thread(target=master.start)
        master_thread.daemon = True
        master_thread.start()

        mock_client_socket.recv.return_value = b'http://example.com\n'

        time.sleep(0.5)

        self.assertEqual(master.task_queue.qsize(), 0)

        mock_server_socket.close()

    def test_update_stats(self):
        master = Master('localhost', 5000, 1, 3)
        master.result_queue = queue.Queue()

        stats_thread = threading.Thread(target=master.update_stats)
        stats_thread.daemon = True
        stats_thread.start()

        master.result_queue.put(1)
        master.result_queue.put(1)

        time.sleep(0.1)

        self.assertEqual(master.total_processed, 2)


if __name__ == '__main__':
    unittest.main()
