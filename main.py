from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def get_jmena_posadky_for_admin() ->str:
    with open("jmena_posadky.txt") as file:
        return file.read()


def set_jmena_posadky_from_admin(data) -> None:
    with open("jmena_posadky.txt", "w") as file:
        file.write(data)


def get_jmena_posadky_for_user() ->list[str]:
    with open("jmena_posadky.txt") as file:
        return file.read().split("\n")


@app.route("/", methods=["GET", "POST"])
def join():
    session.clear()
    if request.method == "GET":
        return render_template("join.html", jmena_posadky = get_jmena_posadky_for_user())
    else:
        if jmeno := request.form.get("jmeno"):
            session["jmeno"] = f"{jmeno}@posadka"
            return redirect(url_for("chat"))


@app.route("/chat")
def chat():
    if not session.get("jmeno"):
        return redirect(url_for("join"))
    return render_template("chat.html", komunikacni_jmeno = session.get("jmeno"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    session.clear()
    if request.method == "GET":
        return render_template("admin.html", jmena_posadky = get_jmena_posadky_for_admin())
    else:
        if request.form.get("save"):
            set_jmena_posadky_from_admin(request.form.get("jmena_posadky"))
            return redirect(url_for("admin"))
        elif request.form.get("join"):
            session["jmeno"] = f"{request.form.get('admin_name')}@EMC"
            return redirect(url_for("chat"))
        

@socketio.on("connect")
def connect():
    jmeno = session.get("jmeno")
    print(f"connected {jmeno}")
    send({"name": session.get("jmeno"), "message": "joinnul."}, broadcast=True)


@socketio.on("disconnect")
def disconnect():
    jmeno = session.get("jmeno")
    print(f"disconnected {jmeno}")
    send({"name": session.get("jmeno"), "message": "se odpojil."}, broadcast=True)


@socketio.on("message")
def message(data):
    content = {"name": session.get("jmeno"), "message": data["data"]}
    send(content , broadcast=True)

            
if __name__ == '__main__':
    socketio.run(app, debug=True)