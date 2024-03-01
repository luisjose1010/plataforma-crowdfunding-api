import contextlib
import time
import threading
import uvicorn
from core.config import Settings

class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def server_action(callback):
    config = uvicorn.Config(app=Settings.SERVER_APP, host=Settings.SERVER_HOST, port=5000,
                reload=False, log_level=Settings.SERVER_LOG_LEVEL)
    server = Server(config=config)

    with server.run_in_thread():
        # Server is started.
        callback()
        # Server will be stopped once code put here is completed