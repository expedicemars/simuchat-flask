from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from .settings_handling import get_jmena_posadky_for_user, get_jmena_posadky_for_admin, get_datetime_zacatku, set_jmena_posadky_from_admin, set_pocet_zprav, set_datetime_zacatku, get_pocet_zprav, toggle_pripojovani, get_pripojovani
from .message import Message, archivovat


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sprcha-je-jen-ochoceny-vodopad'
socketio = SocketIO(app)


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
    return render_template("chat.html", komunikacni_jmeno = session.get("jmeno"), messages = Message.get_history_on_join(), is_admin = session.get("admin"))

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
            pripojovani_3ojc = "zobrazuje" if get_pripojovani() else "nezobrazuje"
            pripojovani_inf = "Nezobrazovat" if get_pripojovani() else "Zobrazovat"
            return render_template("admin.html", jmena_posadky = get_jmena_posadky_for_admin(), datetime_zacatku = get_datetime_zacatku(), pocet_zprav = get_pocet_zprav(), pripojovani_3ojc = pripojovani_3ojc, pripojovani_inf = pripojovani_inf)
    else:
        if request.form.get("save"):
            set_jmena_posadky_from_admin(request.form.get("jmena_posadky"))
            return redirect(url_for("admin"))
        elif request.form.get("admin_name"):
            session["jmeno"] = f"{request.form.get('admin_name')}@EMMC"
            return redirect(url_for("chat"))
        elif request.form.get("pocet_zprav_btn"):
            pocet_zprav = request.form.get("pocet_zprav")
            set_pocet_zprav(pocet_zprav)
            return redirect(url_for("admin"))
        elif request.form.get("datum_btn"):
            set_datetime_zacatku(request_form=request.form.to_dict())
            return redirect(url_for("admin"))
        elif request.form.get("archivovat"):
            archivovat()
            return redirect(url_for("admin"))
        elif request.form.get("pripojovani"):
            toggle_pripojovani()
            return redirect(url_for("admin"))

            
@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")


@socketio.on("connect")
def connect():
    if session.get("admin") and not get_pripojovani():
        pass
    else:
        m = Message(name=session.get("jmeno"), text="joined.", type="connection")
        m.save()
        m.send()
        


@socketio.on("disconnect")
def disconnect():
    if session.get("admin") and not get_pripojovani():
        pass
    else:
        m = Message(name=session.get("jmeno"), text="joined.", type="connection")
        m.save()
        m.send()


@socketio.on("message")
def message(data):
    text = data["text"]
    type = "org" if session.get("admin") else "posadka"
    m = Message(name=session.get("jmeno"), text=text, type=type)
    m.save()
    m.send()



    