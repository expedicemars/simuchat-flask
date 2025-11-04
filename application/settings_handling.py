from .paths import settings_path, settings_example_path
import json
from datetime import datetime


def ensure_settings() -> None:
    if not settings_path().exists():
        with open(settings_example_path()) as file:
            settings = file.read()
        with open(settings_path(), "w") as file:
            file.write(settings)


def get_settings() -> dict:
    with open(settings_path()) as file:
        return json.load(file)
    
    
def set_settings(settings: dict) -> None:
    with open(settings_path(), "w") as file:
        file.write(json.dumps(settings, indent=4))
        
        
def get_jmena_posadky_for_admin() -> str:
    settings = get_settings()
    return "\n".join(settings["jmena_posadky"])
    

def get_jmena_posadky_for_user() ->list[str]:
    settings = get_settings()
    return settings["jmena_posadky"]


def set_jmena_posadky_from_admin(data) -> None:
    settings = get_settings()
    settings["jmena_posadky"] = data.split("\n")
    set_settings(settings)
        
        
def set_datetime_zacatku(request_form: dict) -> None:
    rok = int(request_form.get("rok"))
    mesic = int(request_form.get("mesic"))
    den = int(request_form.get("den"))
    hodina = int(request_form.get("hodina"))
    minuta = int(request_form.get("minuta"))
    d = datetime(year=rok, month=mesic, day=den, hour=hodina, minute=minuta)
    settings = get_settings()
    settings["datetime_zacatku"] = d.isoformat()
    set_settings(settings=settings)


def get_datetime_zacatku() -> datetime:
    settings = get_settings()
    return datetime.fromisoformat(settings["datetime_zacatku"])


def toggle_pripojovani() -> int:
    settings = get_settings()
    settings["zobrazaovani_pripojeni_adminu"] = not settings["zobrazaovani_pripojeni_adminu"]
    set_settings(settings)
    
    
def get_pripojovani() -> bool:
    settings = get_settings()
    return settings["zobrazaovani_pripojeni_adminu"]


def get_port() -> int:
    settings = get_settings()
    return int(settings["port"])


def set_port(port: int) -> None:
    settings = get_settings()
    settings["port"] = port
    set_settings(settings)


def get_prodleva() -> int:
    settings = get_settings()
    return int(settings["prodleva"])


def set_prodleva(prodleva: int) -> None:
    settings = get_settings()
    settings["prodleva"] = prodleva
    set_settings(settings)