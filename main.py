from application import app, socketio
from application.create_files import create_messages_file
from application.settings_handling import get_port

if __name__ == '__main__':
    create_messages_file()
    socketio.run(app, host='0.0.0.0', port=get_port(), debug=True)


    

