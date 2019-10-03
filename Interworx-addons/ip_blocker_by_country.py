#! /usr/bin/python
import os.path
import os
import subprocess
import datetime
import urllib.request
import json

x=datetime.datetime.now()
datum=(datetime.datetime.now().strftime("%Y-%m-%d"))
fajl =("/chroot/home/tophirde/var/tophirdetes.hu/logs/transfer-ssl-"+datum+".log")
feketelista=("/chroot/home/feketelista.txt")

with open(fajl) as f:
	text = f.readlines()
	size = len(text)
#print(size)
meret=size-10
#print(meret)


def listaban_keres2(ip):
	if os.path.isfile(feketelista):
		with open(feketelista) as fek:
			if ip in fek.read():
				print("Mar a listaban van.")
			else:
				os.system("/etc/apf/apf -d "+ip)
				print("IP cim letiltva!")
				with open(feketelista, 'a') as k:
					k.write(ip+'\n')
	else:
		file = open(feketelista, "w+")
		listaban_keres2(ip)	
	


def listaban_keres(ip):
	if os.path.isfile(feketelista):
		with open(feketelista, 'a') as f:
			f.write(ip+'\n')	
	else:
		file = open(feketelista, 'w+')
		listaban_keres(ip)


def ellenorzes(ip):
	with urllib.request.urlopen("https://geoip-db.com/json/"+ip) as url:
	    data = json.loads(url.read().decode())
	    orszag=(data['country_code'])
	if orszag == "FR" or orszag == "MY":
		print("Blacklistre fel :"+orszag+" "+ip)
		listaban_keres2(ip)
	else:
		print("Engedelyezett ip :"+orszag+" "+ip)
	

if os.path.isfile(fajl):
	#print("Van fajl.")
	f=open(fajl, 'r').readlines()
	while meret < size :
		sor=f[meret]
		ip=sor.split('-')[0]
		ellenorzes(ip)
		meret += 1	
else:
	print("Nincs fajl") 