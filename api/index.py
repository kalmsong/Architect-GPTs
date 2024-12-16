from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/geocode", methods=["GET"])
def geocode():
    address = request.args.get("address")
    type = request.args.get("type", "road")

    if not address:
        return jsonify({"error": "address 파라미터가 필요합니다."}), 400

    api_url = "https://api.vworld.kr/req/address"
    api_key = os.getenv("VWORLD_API_KEY")  # 환경 변수에서 인증키 가져오기
    params = {
    "service": "address",
    "request": "getcoord",
    "crs": "epsg:4326",
    "address": address,
    "format": "json",
    "type": type,
    "key": api_key
    }


    try:
        # 디버깅용 로그 출력
        print(f"API 요청 URL: {api_url}")
        print(f"요청 파라미터: {params}")

        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        # 응답 데이터 출력
        print(f"응답 데이터: {response.json()}")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"VWorld API 요청 실패: {e}")  # 디버깅 로그
        return jsonify({"error": "VWorld API 요청 실패", "details": str(e)}), 502
    except Exception as e:
        print(f"서버 내부 오류: {e}")  # 추가 디버깅 로그
        return jsonify({"error": "서버 내부 오류", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
