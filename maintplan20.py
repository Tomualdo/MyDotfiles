#! /usr/bin/env python3

import nclib
import time
from datetime import datetime
import mysql.connector
import sys

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	RED = '\033[0;31m'

proface = { 
	'SCR_02_A': 	{'IP' :'10.210.202.60', 'type': 'WD'},
	'SCR_02_B': 	{'IP' :'10.210.202.61', 'type': 'WD'},
	'SCR_03_A': 	{'IP' :'10.210.202.62', 'type': 'LT'},
	'SCR_03_B': 	{'IP' :'10.210.202.63', 'type': 'LT'},
	'SCR_04_CMB': 	{'IP' :'10.210.202.64', 'type': 'WD'},
	'SCR_05_LEAK': 	{'IP' :'10.210.202.65', 'type': 'LT'},
	'LNT_01_02': 	{'IP' :'10.210.202.66', 'type': 'WD1'},
	'LNT_01_03': 	{'IP' :'10.210.202.67', 'type': 'WD1'},
	'LNT_01_04': 	{'IP' :'10.210.202.68', 'type': 'WD1'},
	'LNT_01_05': 	{'IP' :'10.210.202.69', 'type': 'LT'},
	'LNT_01_06': 	{'IP' :'10.210.202.70', 'type': 'WD'},
	'LNT_01_07': 	{'IP' :'10.210.202.71', 'type': 'SP'},
	#'LNT_01_08': 	{'IP' :'10.210.202.72', 'type': 'PR'},#CLINCHING
	'LNT_01_09': 	{'IP' :'10.210.202.73', 'type': 'SP'},
	'LNT_01_10': 	{'IP' :'10.210.202.74', 'type': 'SP1'},
	'LNT_01_11': 	{'IP' :'10.210.202.75', 'type': 'BO'},
	'LNT_01_12': 	{'IP' :'10.210.202.76', 'type': 'LT'},
	'QL_CTR': 		{'IP' :'10.210.202.77', 'type': 'CTR'},
	'QL_MAIN_02':	{'IP' :'10.210.202.78', 'type': 'WD'},
	'QL_MAIN_03':	{'IP' :'10.210.202.79', 'type': 'WDLT'},
	'KAPPA_WCC':	{'IP' :'10.210.202.80', 'type': 'ST'}
			
}

requestPoziadavka = { 
		"WD": 	{0 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},
				
		"WD1": 	{0 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Porucha dopravníka',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},	
				
		"BO": 	{0 : {1:'Chyba uťahovania',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},
				
		"LT": 	{0 : {1:'Výmena tesnenia',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Porucha lasera',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha INKJET tlačiarne',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},
				
		"SP": 	{0 : {1:'Nastavenie bodového zvaru',2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Výmena bodovacieho hrotu',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Chyba chladenia',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},
		"SP1": 	{0 : {1:'Nastavenie bodového zvaru',2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Výmena bodovacieho hrotu',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Chyba chladenia',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Porucha lasera',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},
		"ST": 	{0 : {1:'Nastavenie bodového zvaru',2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #KAPPA STUFFING
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Výmena bodovacieho hrotu',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha serva',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				11 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #KAPPA WELD 1
				12 : {1:'Nastavenie stroja',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				13 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				14 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				15 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				16 : {1:'Nastavenie kamery',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				17 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				18 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				19 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				21 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #KAPPA WELD 2
				22 : {1:'Nastavenie stroja',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				23 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				24 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				25 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				26 : {1:'Nastavenie kamery',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				27 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				28 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				29 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				},
		"WDLT": {0 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #MAIN 03 WE
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				11 : {1:'Výmena tesnenia',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #MAIN 04 LT
				12 : {1:'Nastavenie stroja',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				13 : {1:'Porucha lasera',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				14 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				15 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				16 : {1:'Nastavenie kamery',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				17 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				18 : {1:'Porucha INKJET tlačiarne',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				19 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}
				},
		"CTR": 	{0 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #CTR WELD
				1 : {1:'Nastavenie stroja',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				2 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				3 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				4 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				5 : {1:'Nastavenie kamery',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				6 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				7 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				8 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				11 : {1:'Nastavenie dráhy zvaru',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #CTR BOLTING
				12 : {1:'Nastavenie stroja',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				13 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				14 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				15 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				16 : {1:'Nastavenie kamery',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				17 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				18 : {1:'Porucha robota',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				19 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				21 : {1:'Výmena tesnenia',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'}, #CTR LT
				22 : {1:'Nastavenie stroja',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				23 : {1:'Zalepená zváracia špička',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				24 : {1:'Iná porucha',				2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				25 : {1:'Porucha snímača',			2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				26 : {1:'Nastavenie kamery',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				27 : {1:'Preventívna údržba',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				28 : {1:'Porucha INKJET tlačiarne',	2: 'V prevádzke',	3:'2. Obmedzenie výroby'},
				29 : {1:'Núdzové zastavenie',		2: 'V prevádzke',	3:'2. Obmedzenie výroby'}				
				}		
}

debugProface = { 
	"SCR": {
		"SCR_02_A": "10.210.200.191" 
		}
}


def getDebugLevel():
	if (len(sys.argv) > 1) :
		debugLevel = sys.argv[1]
		if debugLevel == '-d':
			return 1
			
		if debugLevel == '-dd':
			return 2
		
		if debugLevel == '-ddd':
			return 3	
	
	return 0

def get_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
def print_list(table_list):
	for x,y in table_list:
		print (x+' '+y+'END')
	print()

def get_proface_reset_word(status):
	#reset BITS in Proface													
	#nc.send(b'B\x00\x00\x00\x00\x00\x00\x08\x1bW\x00\x14\x00\x01\x00\x03')
	#													^
	#												MEM20
	
	reset_command = bytearray(b'B\x00\x00\x00\x00\x00\x00\x08\x1bW\x00\x14\x00\x01\x00\x03')
	rc = list(reset_command)
	
	loop = 0
	for	word in status:
		if (word == 7):
			reset_word = 20+loop
			rc[11] = reset_word
			reset_command = bytearray(rc)
			return reset_command
		loop = loop +1

def getMP_kod_poruchy():
	try:
		mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
		mycursor = mp_database.cursor()
		mycursor.execute("SELECT IDERCD,FSERNM FROM TDERCD_VIEW where FBDELE=0 GROUP BY FSERNM")
		myresult = mycursor.fetchall()
		
	except:
		#mp_database.close()
		return 'ERROR CONNECT'
		
	if (getDebugLevel() == 3):
		print_list(myresult)
		
	mp_database.close()
	return myresult
	
def getMP_stav_zariadenia():
	try:
		mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
		mycursor = mp_database.cursor()
		mycursor.execute("SELECT IDTMOV,FSTMOV FROM TSTMOV_VIEW  where FBDELE=0")
		myresult = mycursor.fetchall()
		
	except:
		#mp_database.close()
		return 'ERROR CONNECT'
		
	if (getDebugLevel() == 3):
		print_list(myresult)
		
	mp_database.close()
	return myresult
	
def getMP_priorita():
	try:
		mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
		mycursor = mp_database.cursor()
		mycursor.execute("SELECT IDSAPR, FSSAPR FROM TSSAPR_VIEW where FBDELE=0")
		myresult = mycursor.fetchall()
		
	except:
		#mp_database.close()
		return 'ERROR CONNECT'
		
	if (getDebugLevel() == 3):
		print_list(myresult)
		
	mp_database.close()
	return myresult

def getMP_ID(table,dopyt):
	for id,nazov in table:
		if nazov == dopyt:
			return id
	return 'NAZOV dopytu SA NENASIEL'


def send_MP_rquest(sql_connection_object,table1,table2,table3,machine,requestList,status,proface_connection_object):
	uniqeINCREMENT = get_time()
	mycursor = sql_connection_object.cursor()
	sql = "INSERT INTO TISERV(IDSERV,IDERCD,IDTMOV,IDSAPR,FSECRN)VALUES(%s,%s,%s,%s,%s)"
	val = (uniqeINCREMENT+"s0",getMP_ID(table1,requestList[0]),getMP_ID(table2,requestList[1]),getMP_ID(table3,requestList[2]),machine)
	#test_val = (uniqeINCREMENT+"s0","CAA1C481A5494650BAEC7F47B8C36F90", "4120FE1BE64B42118FA092E9926E3942","A27963D92537418E896001DF713D3B4G",machine)
								
	mycursor.execute(sql,val)
	sql_connection_object.commit()
	proface_connection_object.send(get_proface_reset_word(status))
	
def getRequestList(parameter,poruchaNum):
	typ = parameter
	rr=(requestPoziadavka.get(typ).get(poruchaNum))	#{1: 'Výmena tesnenia', 2: 'V prevádzke', 3: '2. Obmedzenie výroby'}	---dict
	rl=list(rr.values())							#['Výmena tesnenia', 'V prevádzke', '2. Obmedzenie výroby']				---list
	return rl

def magic():
	list_kody_poruch = getMP_kod_poruchy()
	list_stavy = getMP_stav_zariadenia()
	list_priorit = getMP_priorita()
	
	
	for machine,parameter in proface.items():
		try:
			memlink = [] # clear viariable
			#nc = nclib.Netcat(('10.210.200.191', 1024), udp=True, verbose=False)
			# ""proface['SCR'][machine]"" 	read all IP adresses from dictionary
			# ""machine"" 					read all machine names from dictionary
			
			nc = nclib.Netcat((parameter['IP'], 1024), udp=True, verbose=False)	#pass IP form dictionary
			#nc = nclib.Netcat((debugProface['SCR'][machine], 1024), udp=True, verbose=False) #DEBUG !!! Proface
			
			nc.settimeout(0.2)
			nc.echo_hex =False 
			nc.send(b'B\x00\x00\x00\x00\x00\x00\x06\x1bR\x00\x13\x00\x1f') # 0a - 10 stavov UPDATE: #1f - 31 stavov
			
			#read outout from Proface
			memlink = bytearray(nc.recv())
			
			#read actual time
			tim = get_time()
			
			#setup status varible as LIST
			status =list()
			
			#if Proface is Offline write to log file
		finally:
			if not memlink:
				if (getDebugLevel() == 1):
					myfile = open("/home/tom/Projects/proface/log.txt",'a')
					myfile.write(tim+' '+bcolors.RED+machine+'\t'+' Offline !!!'+bcolors.ENDC+'\n')
					myfile.close()
				nc.close()
				
			#if Proface is ONLINE fill status of PORUCHA and try to connect MaintPlan Database
			else:
				#create range from 29 to 13 in sequence -2 (29,27,25...)
				# fill status of monitoring memory (memlink 20.00 - 29.00) to get status of memlink 20.00 -> status[0]
				for x in range(71,12,-2):
					y=0
					status.insert(y, memlink[x])
					y=y+1
				try:
					mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
					if mp_database.is_connected():
						mycursor = mp_database.cursor()
						db_Info = mp_database.get_server_info()
						#check the status before after
						for st in range (0,30):
							#print(st)
							if not(st == 9 or st == 10 or st == 20):
								if (status[st] == 7): #'st' PORUCHA is set
									poruchaNum = st							
									requestList = getRequestList(parameter['type'],poruchaNum)	#ziskaj podla statusu (poziadavka) (stav) a (priorita)
									# vynimky 3 obrazovky KAPPA
									if machine == 'KAPPA_WCC' and st >= 11 and st <= 19:
										machine = 'KAPPA_WCC_03'
									if machine == 'KAPPA_WCC' and st >= 21 and st <= 29:
										machine = 'KAPPA_WCC_06'
									# vynimky MAIN
									if machine == 'QL_MAIN_03' and st >= 11 and st <= 19:
										machine = 'QL_MAIN_05'
										
									# vynimky 3 obrazovky CTR
									if machine == 'QL_CTR' and st >= 11 and st <= 19:
										machine = 'QL_CTR_BLT'
									if machine == 'QL_CTR' and st >= 21 and st <= 29:
										machine = 'QL_CTR_LT'									
										
									send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,requestList,status,nc)

						nc.close()						
						mp_database.close()
						
				#except :
				#	db_Info = "Error connecting MaintPlan Database"
					
				finally:
					#convert status LIST to string for file write
					if not status:
						status = 'NULL'
					else:
						status = ''.join(map(str,status))
					
					if mp_database.is_connected():
						mp_database.close()
						
					if (getDebugLevel() == 1):
						myfile = open("/home/tom/Projects/proface/log.txt",'a')
						myfile.write(tim+' '+bcolors.OKGREEN+machine+'\t'+' ONline'+bcolors.ENDC+'\t\t'+' MP: '+db_Info+' '+status+'\n')
						myfile.close()
					nc.close()

def main():
	
	while(True):
		time.sleep(1)	# DEBUG !!
		magic()
if __name__ == '__main__':
	main()