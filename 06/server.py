import argparse
import socket
import threading
import queue
import json
from collections import defaultdict
import requests
from bs4 import BeautifulSoup


class Worker(threading.Thread):
    def __init__(self, worker_id, task_queue, result_queue, k):
        super().__init__()
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.k = k
        self.daemon = True

    def run(self):
        while True:
            client_socket, url = self.task_queue.get()
            try:
                word_counts = self.process_url(url)
                response = json.dumps(word_counts)
                client_socket.sendall(response.encode('utf-8'))
                self.result_queue.put(1)
            except Exception as e:
                print(f"Worker {self.worker_id} error processing {url}: {e}")
                error_msg = json.dumps({"error": str(e)})
                client_socket.sendall(error_msg.encode('utf-8'))
            finally:
                client_socket.close()

    def process_url(self, url):
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        words = [word.lower() for word in text.split() if word.isalpha()]
        word_counts = defaultdict(int)
        for word in words:
            word_counts[word] += 1

        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:self.k]
        return dict(top_words)


class Master:
    def __init__(self, host, port, num_workers, k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.k = k
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.total_processed = 0
        self.lock = threading.Lock()

    def start(self):
        for i in range(self.num_workers):
            worker = Worker(i, self.task_queue, self.result_queue, self.k)
            self.workers.append(worker)
            worker.start()

        stats_thread = threading.Thread(target=self.update_stats, daemon=True)
        stats_thread.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = s.accept()
                print(f"Accepted connection from {addr}")

                url = client_socket.recv(1024).decode('utf-8').strip()
                if not url:
                    client_socket.close()
                    continue

                self.task_queue.put((client_socket, url))

    def update_stats(self):
        while True:
            self.result_queue.get()
            with self.lock:
                self.total_processed += 1
                print(f"Total URLs processed: {self.total_processed}")


def parse_args():
    parser = argparse.ArgumentParser(description='URL processing server')
    parser.add_argument(
        '-w',
        '--workers',
        type=int,
        required=True,
        help='Number of worker threads',
    )
    parser.add_argument(
        '-k',
        type=int,
        required=True,
        help='Number of top words to return',
    )
    parser.add_argument(
        '--host',
        default='localhost',
        help='Server host (default: localhost)',
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=5000,
        help='Server port (default: 5000)',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    master = Master(args.host, args.port, args.workers, args.k)
    master.start()


if __name__ == '__main__':
    main()
