import os
import redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv

from api import create_app

load_dotenv()

listen = ["default"]
redis_url = os.getenv("REDISTOGO_URL")
redis_conn = redis.from_url(redis_url)

if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_ENV", "development"))
    with app.app_context():
        with Connection(redis_conn):
            worker = Worker(list(map(Queue, listen)))
            worker.work()
