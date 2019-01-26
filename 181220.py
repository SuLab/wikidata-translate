from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent")
    user_name = request.args.get("name")
    return "<p>Your browser is {}</p><p>Your name is {}</p>".format(user_agent, user_name)


@app.route("/users")
def get_users():
    users = ["Maomao", "Alicia"]
    resp = ["<p>{}</p>".format(user) for user in users]
    resp = "\n".join(resp)

    return resp


if __name__ == "__main__":
    app.run(port=5566, threaded=True, debug=True)
