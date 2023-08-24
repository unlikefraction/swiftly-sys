import sys
import time
import threading

class Loader:
    def __init__(self):
        self._spinner = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
        self._spin_count = 0
        self._running = False
        self._thread = None

    def _spin(self, message):
        while self._running:
            sys.stdout.write(f'\r{self._spinner[self._spin_count % len(self._spinner)]} {message}')
            sys.stdout.flush()
            time.sleep(0.2)
            self._spin_count += 1

    def start(self, message):
        self._running = True
        self._thread = threading.Thread(target=self._spin, args=(message,))
        self._thread.start()

    def end(self, message, failed=False):
        self._running = False
        self._thread.join()
        icon = "\033[91m✗\033[0m" if failed else "\033[92m✓\033[0m"  # \033[91m is red and \033[92m is green
        sys.stdout.write(f'\r{icon} {message} {" "*10}\n')
        sys.stdout.flush()

# Example usage:
# loader = Loader()
# loader.start("Loading...")
# time.sleep(5)  # Simulate some work
# loader.end("Completed successfully!")
