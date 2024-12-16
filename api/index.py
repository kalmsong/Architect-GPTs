from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/geocode", methods=["GET"])
def geocode():
    address = request.args.get("address")
    type = request.args.get("type", "road")  # 기본값: 도로명 주소

    if not address:
        return Response("address 파라미터가 필요합니다.", status=400)

    # VWorld API 호출
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
    response = requests.get(api_url, params=params)
    
    # 결과 반환
    return Response(response.text, status=response.status_code, content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True)
