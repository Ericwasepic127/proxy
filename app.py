#!/usr/bin/env python3
# Made by @Ericwasepic127

# IMPORTS
import flask, requests, os, threading as t
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

# VARIABLES
GETWARN = """<title>Proxy Server</title>
<h1>This is Proxy Server</h1>
<hr>
<p>Use POST to get API response</p>
<br>
<strong>Or else, you will end up here</strong>"""
API_KEY = os.environ.get("API_KEY")  
ENDPOINT = os.environ.get("ENDPOINT")
LIMIT = int(os.environ.get("LIMIT", "7"))
PROVIDER = os.environ.get("PROVIDER", "auto")
MODEL = os.environ.get("MODEL", "auto")
COUNT = 0
LOCK = t.Lock()

# HELPERS /FUNCTIONS/
def post(url, key, data):
    try:
        r = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=data
        )
        return r.text, r.status_code
    except (BaseException, Exception) as e:
        return jsonify({"error": {
            "message": str(e),
            "type":"api_error",
            "code": type(e).__name__
            }
        }), 500

def handleReq(f):
    global COUNT
    def w(*a, **k):
        global COUNT
        with LOCK:
            COUNT += 1
        try:
            s = f(*a, **k)
        except:
            raise
        else:
            return s
        finally:
            with LOCK:
                COUNT -= 1
    return w

# PREPARE
app = Flask(__name__)
CORS(app)

# HANDLERS
@app.route('/ready', methods=['GET'])
def ready():
     return "ok\n", 200

@app.route('/', methods=['POST', 'GET'])
@handleReq
def chat():
    if request.method == 'GET':
        return GETWARN, 200
    if COUNT > LIMIT:
        return jsonify({"error": {
                "message": "We're experiencing a high volume of traffic right now. Please hang tight and try again in a few minutes.",
                "type": "rate_limit_error",
                "code": "server_busy",
            }
        }), 503
    reqjson = request.json.copy()
    return post(ENDPOINT, API_KEY, reqjson)
