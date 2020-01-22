#!/usr/bin/python3
import timeit

# Es wird überprüft in welchem Intervall der ModbusTcpClient die gewünschten Werte auf den Registern schreibt
code_to_test = """
from pymodbus.client.sync import ModbusTcpClient
import time
import sys

modbus_ip='10.0.0.42'
seconds=0
register=0
register_values=[1, 1400, 100]
client = ModbusTcpClient(modbus_ip)

if not client.connect():
    print("Der Modbus Server läuft nicht.")
    sys.exit(1)

print("Setze die Werte {} \t auf Register {} für {} Sekunden".format(register_values, register + 1, seconds))
time_end = time.time() + seconds
while time.time() < time_end:
    client.write_registers(register, register_values)

client.close()
"""

# Durchschnitt in Sekunden über 1000 Aufrufe bilden
elapsed_time = timeit.timeit(code_to_test, number=1000)/1000

print("Millisekunden pro Aufruf: {:f}".format(elapsed_time*1000))
