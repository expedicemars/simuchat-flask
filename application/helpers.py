import socket
from application.settings_handling import get_datetime_zacatku
from datetime import datetime


def get_ip():
    try:
        # Create a socket object and connect to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Using a well-known external server (Google's public DNS)
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return "127.0.0.1"  # Default to localhost if there's an error
    
    
def pretty_cas_zpravy(time: datetime = None) -> str:
    datetime_zacatku = get_datetime_zacatku()
    datetime_zpravy = time if time else datetime.now()
    dt = datetime_zpravy - datetime_zacatku
    diff = dt.total_seconds()
    sign = ""
    if diff < 0:
        sign = "- "
    diff = abs(diff)
    hours = int(diff / 3600)
    leftover = diff - hours*3600
    minutes = int(leftover/60)
    leftover = leftover - minutes*60
    sec = int(leftover)
    return f"{sign}{str(hours).rjust(2, '0')} : {str(minutes).rjust(2, '0')} : {str(sec).rjust(2, '0')}"
