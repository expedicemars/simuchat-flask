from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from pathlib import Path
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sprcha-je-jen-ochoceny-vodopad'
socketio = SocketIO(app)
messages_path = Path.cwd() / "messages.json"
settings_path = Path.cwd() / "settings.json"


def get_jmena_posadky_for_admin() -> str:
    with open(settings_path) as file:
        file = json.load(file)
        return "\n".join(file["jmena_posadky"])


def set_jmena_posadky_from_admin(data) -> None:
    with open(settings_path) as file:
        settings = json.load(file)
    settings["jmena_posadky"] = data.split("\n")
    with open(settings_path, "w") as file:
        file.write(json.dumps(settings, indent=4))


def get_jmena_posadky_for_user() ->list[str]:
    with open(settings_path) as file:
        settings = json.load(file)
        return settings["jmena_posadky"]


def create_messages_file() -> None:
    if not messages_path.exists():
        messages_path.touch()
        with open(messages_path, "w") as file:
            file.write(json.dumps([], indent=4))
        
        
def new_message(name, text, type) -> None: # 3 typy: org, posadka, connection
    message = {
        "name": name,
        "text": text,
        "time": str(datetime.now()),
        "type": type
    }
    with open(messages_path) as file:
        messages = json.load(file)
    messages.append(message)
    with open(messages_path, "w") as file:
        file.write(json.dumps(messages, indent=4))
    
    send(message, broadcast=True)
    
def get_raw_messages() -> str:
    with open(messages_path) as file:
        return file.read()

def get_settings() -> dict:
    with open(settings_path) as file:
        return json.load(file)
    
def set_settings(settings: dict) -> None:
    with open(settings_path, "w") as file:
        file.write(json.dumps(settings, indent=4))

def set_pocet_zprav(pocet_zprav: int) -> None:
    settings = get_settings()
    settings["pocet_zprav"] = int(pocet_zprav)
    set_settings(settings)


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
    return render_template("chat.html", komunikacni_jmeno = session.get("jmeno"), messages = get_raw_messages())

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
        elif request.form.get("pocet_zprav_btn"):
            pocet_zprav = request.form.get("pocet_zprav")
            set_pocet_zprav(pocet_zprav)
            return redirect(url_for("admin"))

@socketio.on("connect")
def connect():
    new_message(name=session.get("jmeno"), text="joined.", type="connection")


@socketio.on("disconnect")
def disconnect():
    new_message(name=session.get("jmeno"), text="disconnected.", type="connection")


@socketio.on("message")
def message(data):
    text = data["text"]
    type = "org" if session.get("admin") else "posadka"
    new_message(name=session.get("jmeno"), text=text, type=type)


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")

  
if __name__ == '__main__':
    create_messages_file()
    socketio.run(app, debug=True)