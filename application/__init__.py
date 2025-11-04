from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import getmac
from .settings_handling import get_jmena_posadky_for_user, get_jmena_posadky_for_admin, get_datetime_zacatku, set_jmena_posadky_from_admin, set_datetime_zacatku, toggle_pripojovani, get_pripojovani, get_port, set_port, get_prodleva, set_prodleva
from .message import Message
from .helpers import get_ip
from .settings_handling import ensure_settings

db = SQLAlchemy()
socketio = SocketIO()

def create_app() -> Flask:
    ensure_settings()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "sprcha-je-jen-ochoceny-vodopad"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///message_database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
    
    socketio.init_app(app)
    db.init_app(app)



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
        return render_template("chat.html", komunikacni_jmeno = session.get("jmeno"), messages = Message.get_history_on_join(), prodleva = get_prodleva(), is_admin = session.get("admin"))

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
                return render_template(
                    "admin.html", 
                    jmena_posadky = get_jmena_posadky_for_admin(), 
                    datetime_zacatku = get_datetime_zacatku(), 
                    pripojovani_sloveso = "zobrazuje" if get_pripojovani() else "nezobrazuje",
                    pripojovani_button = "Nezobrazovat" if get_pripojovani() else "Zobrazovat",
                    local_ip = f"{get_ip()}:{get_port()}",
                    mac_adress = getmac.get_mac_address(),
                    port = get_port(), 
                    prodleva = get_prodleva(),
                )
        else:
            if request.form.get("save_names"):
                set_jmena_posadky_from_admin(request.form.get("jmena_posadky"))
                return redirect(url_for("admin"))
            
            elif mode := request.form.get("connect_admin"):
                jmeno = request.form.get("admin_name")
                if jmeno == "":
                    return redirect(url_for("admin"))
                else:
                    jmeno = jmeno + "@EMMC"
                    if mode == "silent":
                        session["mode"] = "silent"
                    session["jmeno"] = jmeno
                    return redirect(url_for("chat"))
            
            elif request.form.get("datum_btn"):
                set_datetime_zacatku(request_form=request.form.to_dict())
                return redirect(url_for("admin"))
            
            elif request.form.get("admin_connect_visible"):
                toggle_pripojovani()
                return redirect(url_for("admin"))
            
            elif request.form.get("port_btn"):
                set_port(int(request.form.get("port")))
                return redirect(url_for("admin"))
            
            elif request.form.get("prodleva_btn"):
                set_prodleva(int(request.form.get("prodleva")))
                return redirect(url_for("admin"))
                
    @app.errorhandler(404)
    def not_found(e):
        return render_template("not_found.html")


    @socketio.on("connect")
    def connect():
        if session.get("admin") and not get_pripojovani():
            pass
        if session.get("mode") == "silent":
            pass
        else:
            m = Message(name=session.get("jmeno"), text="joined.", type="connection")
            m.save_and_send()
            

    @socketio.on("disconnect")
    def disconnect():
        if session.get("admin") and not get_pripojovani():
            pass
        if session.get("mode") == "silent":
            pass
        else:
            m = Message(name=session.get("jmeno"), text="disconnected.", type="connection")
            m.save_and_send()


    @socketio.on("message")
    def message(data):
        text = data["text"]
        type = "org" if session.get("admin") else "posadka"
        m = Message(name=session.get("jmeno"), text=text, type=type)
        m.save_and_send()

    return app

    