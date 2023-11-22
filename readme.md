# Komunikace pro simulace Expedice Mars
Cílem projektu je zajistit komunikaci mezi posádkou a organizátory po síti tak, aby nebyl potřeba internet. 

## TODO

- přidělat kroky ke spuštění
- upozornění na novou zprávu

## Použití

### Posádka

- navštíví IP serveru `/` a zvolí jméno komunikujícího

### Organizátoři

- navštíví IP serveru `/admin` a zadají heslo `hroch314`
- nastaví jména členů posádky, začátek simulace a další nastavení.


## Kroky pro spuštění

### MacOS

1. nainstalovat python
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