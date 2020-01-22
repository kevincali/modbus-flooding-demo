#!/usr/bin/python3
from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap
from subprocess import Popen, PIPE

# Notwendige Flask und Bootstrap Objekte
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Dictionary zum wiederverwenden der "read_register.py" Prozesse
proc_dict = {}

# Zeige auf der Hauptseite die "index.html" an
@app.route('/')
def index():
    return render_template('index.html')

# Dient zur simplen Überprüfung ob der Webserver noch läuft
# Wird in anderen Scripts verwendet
@app.route('/isUp')
def up():
    return "up"

# Wird verwendet um die aktuellen Werte aus den gewünschten Registern darzustellen
# Führt pro Aufruf jeweils einen "read_register.py" Script aus
@app.route('/register/<number>')
def read_register(number):
    def inner():
        # Existiert der gewünschte Prozess bereits, wird er wiederverwendet
        if proc_dict.get(number):
            proc = proc_dict.get(number)

        # Existiert er nicht, wird er erstellt
        else:
            proc = Popen(
                    ['python3 -u ../Modbus/read_register.py ' + number],
                    shell=True,
                    stdout=PIPE,
                    universal_newlines=True)

            proc_dict[number] = proc

        # Generiere jede Ausgabezeile des Scripts
        # Wird für die Echtzeitausgabe benötigt
        for line in iter(proc.stdout.readline,''):
            yield line

    # Sendet die Daten als HTML zur leichteren weiterverarbeitung
    return Response(inner(), mimetype='text/html')

# Führt den Angriff aus dem Python Script "run_attack.py" aus
@app.route('/attack')
def run_attack():
    def inner():
        proc = Popen(
                ['python3 -u ../Modbus/run_attack.py'],
                shell=True,
                stdout=PIPE,
                universal_newlines=True)

        # Generiere jede Ausgabezeile des Scripts
        # Wird für die Echtzeitausgabe benötigt
        for line in iter(proc.stdout.readline,''):
            yield line + '<br>'

    # Sendet die Daten als HTML zur leichteren weiterverarbeitung
    return Response(inner(), mimetype='text/html')

if __name__ == '__main__':
    # Ermöglicht die Verwendung von Bootstrap ohne Internetanbindung
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    # Erlaube den Netzwerk-Zugriff auf den Webserver
    app.run(host='0.0.0.0', debug=False, threaded=True)
