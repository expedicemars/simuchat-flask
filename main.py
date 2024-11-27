from application import app, socketio
from application.settings_handling import get_port

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=get_port(), debug=True)


    

