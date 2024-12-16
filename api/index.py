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
        "key": "C4D98874-5F18-3AF8-90AC-25913420D1DF"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # VWorld API에서 액세스 거부나 오류 처리
        if data.get("response", {}).get("status") != "OK":
            return jsonify({"error": "VWorld API 오류", "details": data}), 502

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API 요청 실패", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
