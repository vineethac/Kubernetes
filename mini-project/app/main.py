from fastapi import FastAPI, Response
import uvicorn
from datetime import datetime
import prometheus_client
from prometheus_client import CollectorRegistry, Counter


app = FastAPI()
registry = CollectorRegistry()

# prometheus counter metric
# value of counter can only increase or be reset to zero on restart
welcome_count = Counter("welcome_count", "count of welcome api", registry=registry)
testpage_count = Counter("testpage_count", "count of testpage api", registry=registry)
date_count = Counter("date_count", "count of date api", registry=registry)


@app.get("/")
def welcome():
    welcome_count.inc()
    return {"message": "welcome to using FastAPI"}


@app.get("/testpage")
def test_page():
    testpage_count.inc()
    return {"message": "this is a test page"}


@app.get("/date")
def date():
    date_count.inc()
    return {"date": datetime.now()}


@app.get("/metrics")
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest(registry=registry),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5000, log_level="info")
