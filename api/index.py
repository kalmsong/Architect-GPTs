from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/geocode", methods=["GET"])
def geocode():
    address = request.args.get("address")
    type = request.args.get("type", "road")

    if not address:
        return jsonify({"error": "address 파라미터가 필요합니다."}), 400

    api_url = "https://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": address,
        "format": "json",
        "type": type,
        "key": "F9FCE3A7-B027-3AD4-909A-50C85F322CCA"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "VWorld API 요청 실패", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
