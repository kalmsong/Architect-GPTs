from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/geocode", methods=["GET"])
def geocode():
    address = request.args.get("address")
    type = request.args.get("type", "road")  # 기본값: 도로명 주소

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
        print(f"요청 URL: {api_url}")  # 디버깅용 로그
        print(f"요청 파라미터: {params}")  # 디버깅용 로그

        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        print(f"응답 데이터: {response.json()}")  # 디버깅용 로그

        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"VWorld API 요청 실패: {e}")  # 디버깅용 로그
        return jsonify({"error": "VWorld API 요청 실패", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
