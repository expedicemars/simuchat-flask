# Komunikace pro simulace Expedice Mars
Cílem projektu je zajistit komunikaci mezi posádkou a organizátory po síti tak, aby nebyl potřeba internet.

## TODO

- přidělat kroky ke spuštění
- upozornění na novou zprávu
- postupné archivování konverzace

## Použití

### Posádka

- navštíví IP serveru `/` a zvolí jméno komunikujícího

### Organizátoři

- navštíví IP serveru `/admin` a zadají heslo `hroch314`
- nastaví jména členů posádky, začátek simulace, 


## Kroky pro spuštění

### MacOS

### Windows

## Použité technologie

- Flask
- Flask-SocketIO
- natvrdo stažený bootstrap a socketio.js proto, aby server fungoval zcela bez internetu.

by Josef Lát