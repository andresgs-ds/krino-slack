from ipaddress import ip_address
from flask import Flask, request, Response
import uuid
import datetime
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    data = {}

    data['unique_id'] = str(uuid.uuid4())
    data['ip'] = request.headers.get('Host')
    data['navegador'] = request.headers.get('Sec-Ch-Ua')
    data['is_mobile'] = request.headers.get('Sec-Ch-Ua-Mobile')
    data['plataforma'] = request.headers.get('Sec-Ch-Ua-Platform')
    data['fecha'] = datetime.datetime.now()

    data = json.dumps(data, indent=4, sort_keys=True, default=str)

    print(request.headers)

    return Response(data, status=200)