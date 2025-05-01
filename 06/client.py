import argparse
import socket
import threading
import queue
import json


class URLProcessor(threading.Thread):
    def __init__(self, thread_id, url_queue, host, port):
        super().__init__()
        self.thread_id = thread_id
        self.url_queue = url_queue
        self.host = host
        self.port = port
        self.daemon = True

    def run(self):
        while True:
            url = self.url_queue.get()
            if url is None:
                self.url_queue.task_done()
                break

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((self.host, self.port))
                    s.sendall(url.encode('utf-8'))
                    response = s.recv(4096).decode('utf-8')
                    result = json.loads(response)
                    print(f"{url}: {result}")
            except Exception as e:
                print(f"Thread {self.thread_id} error processing {url}: {e}")

            self.url_queue.task_done()


class URLClient:
    def __init__(self, host, port, num_threads, url_file):
        self.host = host
        self.port = port
        self.num_threads = num_threads
        self.url_file = url_file
        self.url_queue = queue.Queue()
        self.threads = []

    def start(self):
        for i in range(self.num_threads):
            thread = URLProcessor(i, self.url_queue, self.host, self.port)
            self.threads.append(thread)
            thread.start()

        with open(self.url_file, 'r', encoding="utf-8") as f:
            for line in f:
                url = line.strip()
                if url:
                    self.url_queue.put(url)

        self.url_queue.join()

        for _ in range(self.num_threads):
            self.url_queue.put(None)

        for thread in self.threads:
            thread.join()


def parse_args():
    parser = argparse.ArgumentParser(description='URL processing client')
    parser.add_argument(
        'num_threads',
        type=int,
        help='Number of client threads',
    )
    parser.add_argument(
        'url_file',
        help='File containing URLs to process (one per line)',
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
    client = URLClient(args.host, args.port, args.num_threads, args.url_file)
    client.start()


if __name__ == '__main__':
    main()
