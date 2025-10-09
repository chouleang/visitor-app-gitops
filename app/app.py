from flask import Flask, render_template
import redis
import os
import socket
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis-service')
redis_port = int(os.getenv('REDIS_PORT', 6379))
environment = os.getenv('ENVIRONMENT', 'development')
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def index():
    try:
        count = redis_client.incr('visitor_count')
    except redis.ConnectionError:
        count = "Unable to connect to Redis"
    
    hostname = socket.gethostname()
    
    return render_template('index.html', 
                         count=count, 
                         environment=environment,
                         hostname=hostname)

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
