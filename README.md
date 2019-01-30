# Altering packets with scapy on the fly - 2019


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This tool is used to modify on the fly modbus packets. 
Scapy + NetfilterQueue + IPTables + Interfaces bridging

**Host system**: Debian 9
**Network configuration**: 

    auto eht1
    iface eth1 inet manual
    auto eth2
    iface eth2 inet manual
    auto br0
    iface br0 inet manual
	    bridge_ports eth1 eth2



**Scapy libraries:**
 - NetfilterQueue 
 
**IPTables rules:**

    iptables -A FORWARD -m physdev --physdev-in eth1 -j NFQUEUE --queue-num 0
    iptables -A FORWARD -m physdev --physdev-out eth1 -j NFQUEUE --queue-num 0
