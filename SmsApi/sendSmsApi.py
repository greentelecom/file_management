#!"C:\Users\Hp\AppData\Local\Programs\Python\Python37\python.exe"
import base64
import requests
import http as http
# import http.client
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/rest/sms/push/api', methods=['POST'])
def record_subscribers():
    request_data = request.get_json()

    data = 'ConnectAdmin2:Jipime+2021'
    # Standard Base64 Encoding
    encodedBytes = base64.b64encode(data.encode('utf_8'))
    encodedStr = str(encodedBytes, "utf-8")
    print(encodedStr)

    base_server_url = "api.infobip.com"

    conn = http.client.HTTPSConnection(base_server_url)

    payload = "{\"from\":\"JIPIME\",\"to\":\"%s\",\"text\":\"%s\"}" % (request_data['msisdn'], request_data['message'])
    basic_authentication = "Basic " + str(encodedStr)

    headers = {
        'authorization': basic_authentication,
        'content-type': "application/json",
        'accept': "application/json"
    }
    conn.request("POST", "/sms/2/text/single", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return data.decode("utf-8")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8580)
