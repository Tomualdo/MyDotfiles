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
		"SCR_02_A": 	{'IP' :	"10.210.202.60", "type" : "WD"},
		"SCR_02_B": 	{'IP' :	"10.210.202.61", "type" : "WD"},
		"SCR_03_A": 	{'IP' :	"10.210.202.62", "type" : "LT"},
		"SCR_03_B": 	{'IP' :	"10.210.202.63", "type" : "LT"},
		"SCR_04_CMB": 	{'IP' :	"10.210.202.64", "type" : "WD"},
		"SCR_05_LEAK": 	{'IP' :	"10.210.202.65", "type" : "LT"}
			
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
		mycursor.execute("SELECT IDERCD,FSERNM FROM TDERCD_VIEW where FBDELE=0")
		myresult = mycursor.fetchall()
		
	except:
		#mp_database.close()
		return 'ERROR CONNECT'
		
	if (getDebugLevel()==3):
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
		
	if (getDebugLevel()==3):
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
		
	if (getDebugLevel()==3):
		print_list(myresult)
		
	mp_database.close()
	return myresult

def getMP_ID(table,dopyt):
	for id,nazov in table:
		if nazov == dopyt:
			return id
	return 'NAZOV dopytu SA NENASIEL'


def send_MP_rquest(sql_connection_object,table1,table2,table3,machine,poziadavka,stav,priorita,status,proface_connection_object):
	uniqeINCREMENT = get_time()
	mycursor = sql_connection_object.cursor()
	sql = "INSERT INTO TISERV(IDSERV,IDERCD,IDTMOV,IDSAPR,FSECRN)VALUES(%s,%s,%s,%s,%s)"
	val = (uniqeINCREMENT+"s0",getMP_ID(table1,poziadavka),getMP_ID(table2,stav),getMP_ID(table3,priorita),machine)
	#test_val = (uniqeINCREMENT+"s0","CAA1C481A5494650BAEC7F47B8C36F90", "4120FE1BE64B42118FA092E9926E3942","A27963D92537418E896001DF713D3B4G",machine)
								
	mycursor.execute(sql,val)
	sql_connection_object.commit()
	proface_connection_object.send(get_proface_reset_word(status))

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
			nc.send(b'B\x00\x00\x00\x00\x00\x00\x06\x1bR\x00\x13\x00\x0a')
			
			#read outout from Proface
			memlink = bytearray(nc.recv())
			
			#read actual time
			tim = get_time()
			
			#setup status varible as LIST
			status =list()
			
			#if Proface is Offline write to log file
		finally:
			if not memlink:
				myfile = open("/home/tom/Projects/proface/log.txt",'a')
				myfile.write(tim+' '+bcolors.RED+machine+'\t'+' Offline !!!'+bcolors.ENDC+'\n')
				myfile.close()
				nc.close()
				
			#if Proface is ONLINE fill status of PORUCHA and try to connect MaintPlan Database
			else:
				#create range from 29 to 13 in sequence -2 (29,27,25...)
				# fill status of monitoring memory (memlink 20.00 - 29.00) to get status of memlink 20.00 -> status[0]
				for x in range(29,12,-2):
					y=0
					status.insert(y, memlink[x])
					y=y+1
				try:
					mp_database = mysql.connector.connect (host="10.210.200.41",user="sejong_cli",passwd="s3j0ng!",database="mp3_sejong")
					if mp_database.is_connected():
						mycursor = mp_database.cursor()
						db_Info = mp_database.get_server_info()
						#check the status before after
						
						if (status[0] == 7): #1 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Nastavenie dráhy zvaru'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Výmena tesnenia'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
															
							
						if (status[1] == 7): #2 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Nastavenie stroja'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Nastavenie stroja'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)



						if (status[2] == 7): #3 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Zalepená zváracia špička'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Porucha lasera'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)


						if (status[3] == 7): #4 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Iná porucha'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Iná porucha'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)


						if (status[4] == 7): #5 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Porucha snímača'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Porucha snímača'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)


						if (status[5] == 7): #6 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Nastavenie kamery'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Nastavenie kamery'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)


						if (status[6] == 7): #7 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Preventívna údržba'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Preventívna údržba'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)


						if (status[7] == 7): #8 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Porucha robota'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Porucha INKJET tlačiarne'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)


						if (status[8] == 7): #9 PORUCHA is set
						
							if(parameter['type']=='WD'):
								poziadavka = 	'Núdzové zastavenie'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)
							
							if(parameter['type']=='LT'):
								poziadavka = 	'Núdzové zastavenie'
								stav = 			'V prevádzke'
								priorita = 		'2. Obmedzenie výroby'
								send_MP_rquest(mp_database,list_kody_poruch,list_stavy,list_priorit,machine,poziadavka,stav,priorita,status,nc)

						

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