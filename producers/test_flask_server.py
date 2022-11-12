from flask import Flask, request


app = Flask(__name__)


@app.route("/getDetections", methods=["POST"])
def test() -> str:
    print(request.json)
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
