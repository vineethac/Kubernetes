from flask import Flask
from flask_healthz import healthz, HealthError
import logging, time

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")

def verify_liveness():
    time.sleep(5)
    logging.info("Liveness probe OK")

def verify_readiness():
    time.sleep(20)
    logging.info("Readiness probe OK")

def liveness():
    try:
        verify_liveness()
    except Exception:
        raise HealthError("Liveness error!!!")

def readiness():
    try:
        verify_readiness()
    except Exception:
        raise HealthError("Readiness error!!!")

app.config.update(
    HEALTHZ = {
        "live": "app.liveness",
        "ready": "app.readiness",
    }
)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)