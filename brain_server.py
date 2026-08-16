from brain.server import Handler
from http.server import HTTPServer
import os


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler).serve_forever()
