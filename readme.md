# Komunikace pro simulace Expedice Mars
Cílem projektu je zajistit komunikaci mezi posádkou a organizátory po síti tak, aby nebyl potřeba internet. 

## Archivování zpráv

Archivovat zprávy je nutné, protože dlouhá načtená historie způsobuje zpomalení aplikace. Archivuje se buď manuálně, nebo automaticky.

## TODO

- přidělat kroky ke spuštění

## Použití

### Posádka

- navštíví IP serveru `/` a zvolí jméno komunikujícího

### Organizátoři

- navštíví IP serveru `/admin` a zadají heslo `hroch314`
- počítač, který slouží jako server, může použít `127.0.0.1:8000/admin`, po přihlášení je tam vidět IP pro ostatní
- nastaví jména členů posádky, začátek simulace a další nastavení.

## Kroky pro spuštění

### MacOS / Linux

1. nainstalovat python. Dělal jsem to na 3.11 a mělo by to fungovat na novějších.
2. clone tohoto repa někam do složky
3. v terminálu:
    - `pip install pipenv`
    - `cd path/to/cloned/folder`
    - `pipenv install` pro instalaci knihoven
    - `pipenv shell` pro zapnutí venv
4. Několik možností spuštění:
    - (dopoučeno): Gunicorn: `gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 --access-logfile - 'application:create_app()'`
    - Gunicorn bez requestů: `gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 'application:create_app()'`

### Windows

Nemám windows, prosím odzkoušet a doplnit sem / říct Pípovi

### Docker
1. Nainstalovat docker a docker-compose
2. clone tohoto repa někam do složky
3. v terminálu:
    - cd path/to/cloned/folder
    - sudo docker-compose up -d --build

## Použité technologie

- Flask
- Flask-SocketIO
- natvrdo stažený bootstrap a socketio.js proto, aby server fungoval zcela bez internetu.
- gunicorn s workerem eventlet

by Josef Lát
