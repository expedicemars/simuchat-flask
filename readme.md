# Komunikace pro simulace Expedice Mars
Cílem projektu je zajistit komunikaci mezi posádkou a organizátory po síti tak, aby nebyl potřeba internet. 

## TODO

- přidělat kroky ke spuštění

## Použití

### Posádka

- navštíví IP serveru `/` a zvolí jméno komunikujícího

### Organizátoři

- navštíví IP serveru `/admin` a zadají heslo `hroch314`
- počítač, který slouží jako server, může použít `127.0.0.1:5000/admin`, po přihlášení je tam vidět IP pro ostatní
- nastaví jména členů posádky, začátek simulace a další nastavení.

## Kroky pro spuštění

### MacOS

1. nainstalovat python. Dělal jsem to na 3.11 a mělo by to fungovat na novějších.
2. clone tohoto repa někam do složky
3. v terminálu:
    - `pip install pipenv`
    - `cd path/to/cloned/folder`
    - `pipenv install`
    - `pipenv run python main.py`

### Windows

Nemám windows, prosím odzkoušet a doplnit sem / říct Pípovi

## Použité technologie

- Flask
- Flask-SocketIO
- natvrdo stažený bootstrap a socketio.js proto, aby server fungoval zcela bez internetu.

by Josef Lát