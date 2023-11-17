from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from pathlib import Path
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
messages_path = Path.cwd() / "messages.json"


def get_jmena_posadky_for_admin() ->str:
    with open("jmena_posadky.txt") as file:
        return file.read()


def set_jmena_posadky_from_admin(data) -> None:
    with open("jmena_posadky.txt", "w") as file:
        file.write(data)


def get_jmena_posadky_for_user() ->list[str]:
    with open("jmena_posadky.txt") as file:
        return file.read().split("\n")

def create_messages_file() -> None:
    if not messages_path.exists():
        messages_path.touch()
        with open(messages_path, "w") as file:
            file.write(json.dumps([], indent=4))
        
def new_message(name, text) -> None:
    message = {
        "name": name,
        "text": text,
        "time": str(datetime.now())
    }
    with open(messages_path) as file:
        messages = json.load(file)
    messages.append(message)
    with open(messages_path, "w") as file:
        file.write(json.dumps(messages, indent=4))
    
    send(message, broadcast=True)
    
def get_messages() -> list[dict]:
    with open(messages_path) as file:
        return json.load(file)


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
    return render_template("chat.html", komunikacni_jmeno = session.get("jmeno"), messages = get_messages())

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    else:
        if request.form.get("heslo") == "hroch314":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("admin_login"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        else:
            session.clear()
            session["admin"] = True
            return render_template("admin.html", jmena_posadky = get_jmena_posadky_for_admin())
    else:
        if request.form.get("save"):
            set_jmena_posadky_from_admin(request.form.get("jmena_posadky"))
            return redirect(url_for("admin"))
        elif request.form.get("admin_name"):
            session["jmeno"] = f"{request.form.get('admin_name')}@EMC"
            return redirect(url_for("chat"))
        

@socketio.on("connect")
def connect():
    new_message(session.get("jmeno"), "joined.")


@socketio.on("disconnect")
def disconnect():
    new_message(session.get("jmeno"), "disconnected.")


@socketio.on("message")
def message(data):
    new_message(session.get("jmeno"), data["data"])


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")


            
if __name__ == '__main__':
    create_messages_file()
    socketio.run(app, debug=True)