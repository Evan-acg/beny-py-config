import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_modified_time = {}

    def on_modified(self, event):
        if event.is_directory:
            return
        if "cache" in event.src_path:
            return
        if not event.src_path.endswith(".py"):
            return

        file_path = event.src_path
        c_time = time.time()
        last_time = self.last_modified_time.get(file_path, 0)
        duration = c_time - last_time
        if duration <= 2:
            self.last_modified_time[file_path] = c_time
            return
        else:
            self.last_modified_time[file_path] = c_time

        self.do_handler(event)

    def do_handler(self, event):
        print(f"{event.src_path} is modified.")
        os.system("cls && uv run pytest")


class Ob:
    def __init__(self, paths: list[str] | None = None) -> None:
        self.watch_paths: list[str] = [] if paths is None else paths

    def start(self) -> None:
        handler = Handler()
        ob = Observer()
        for p in self.watch_paths:
            p = os.path.abspath(p)
            print(f"watching {p}")
            ob.schedule(handler, p, recursive=True)

        ob.start()

        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt as _:
            ob.stop()

        ob.join()


if __name__ == "__main__":
    default_paths: list[str] = [r".\tests", r".\src"]
    ob = Ob(default_paths)
    ob.start()
