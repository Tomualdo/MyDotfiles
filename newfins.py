from __future__ import print_function
import sys
import nclib

def main():
	mrc=src=mem=mem_s1=mem_s2=mem_s3=mem_e1=mem_e2=debug=dat_len=""
	print (len(sys.argv))
	script = sys.argv[0]
	if len(sys.argv)>=2:
		mrc = sys.argv[1]
	if len(sys.argv)>=3:
		src = sys.argv[2]
	if len(sys.argv)>=4:
		mem = sys.argv[3]
	if len(sys.argv)>=5:
		mem_s1 = sys.argv[4]
	if len(sys.argv)>=6:
		mem_s2 = sys.argv[5]
	if len(sys.argv)>=7:
		mem_s3 = sys.argv[6]
	if len(sys.argv)>=8:
		mem_e1 = sys.argv[7]
	if len(sys.argv)>=9:
		mem_e2 = sys.argv[8]
	if len(sys.argv)>=10:
		debug = sys.argv[9]
	if len(sys.argv)>=11:
		dat_len = sys.argv[10]
	
#	assert mrc in ['01'], 'memory area parameter only 01 you inserted >' + mrc
#	assert src in ['01'], 'memory area parameter from 01 to 05 you inserted >' + src

	if debug=='-d':
		debug=True
	else:
		debug=False

	process(mrc,src,mem,mem_s1,mem_s2,mem_s3,mem_e1,mem_e2,debug=True)	

def process(mrc,src,mem,mem_s1,mem_s2,mem_s3,mem_e1,mem_e2,debug):
	nc = nclib.Netcat(('10.210.200.189', 500), udp=False, verbose=debug)
	nc.echo_hex = debug
	nc.echo_headers = debug
	nc.echo_perline = debug #controls whether the data should be split on newlines for logging
	nc.echo_sending = debug #controls whether to log data on send
	nc.echo_recving = debug #controls whether to log data on recv
	nc.send(b'FINS\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
	response = bytearray(nc.recv())
	cli = (response[19])
	srv = (response[23])

	finsCommand = list(b'FINS\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x00')
#						 \length		 \command		 \errcode		 \
	
	finsCommandFrame = list(b'\x80\x00\x02\x00\x01\x00\x00\x00\x00\x00')
	#finsCommandFrame = list(b'\x80\x00\x02\x00\x01\x00\x00\x00\x00\x01\x00\x00\x82\x00\x00\x00\x0F\xff'\t\o\t\o\)
	#							0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17
	#																	MRC	SRC	MEM	M_S			M_E		
	#																	MRC	SRC	MEM	M_S			M_E	\18\19\20\21\22\23\24		
	finsCommandFrame[7]=chr(cli)
	finsCommandFrame[4]=chr(srv)
	
	dat_len = len(sys.argv)+17	#int(dat_len,16)
	
	print (dat_len)
	finsCommand[7]=chr(dat_len)	#data length
	
	if dat_len >=19:
		mrc = int(mrc,16)	#convert str to int
		finsCommandFrame.append(chr(mrc))
		#finsCommandFrame[10]=chr(mrc)
	if dat_len >=20:
		src = int(src,16)
		finsCommandFrame.append(chr(src))
		#finsCommandFrame[11]=chr(src)
	if dat_len >=21:
		mem = int(mem,16)	#convert str to hex ("82" > "0x82" = 130 )
		finsCommandFrame.append(chr(mem))
		#finsCommandFrame[12]=chr(mem)
	if dat_len >=22:
		mem_s1 = int(mem_s1,16)
		finsCommandFrame.append(chr(mem_s1))
		#finsCommandFrame[13]=chr(mem_s1)
	if dat_len >=23:
		mem_s2 = int(mem_s2,16)
		finsCommandFrame.append(chr(mem_s2))
		#finsCommandFrame[14]=chr(mem_s2)
	if dat_len >=24:
		mem_s3 = int(mem_s3,16)
		finsCommandFrame.append(chr(mem_s3))
		#finsCommandFrame[15]=chr(mem_s3)
	if dat_len >=25:
		mem_e1 = int(mem_e1,16)
		finsCommandFrame.append(chr(mem_e1))
		#finsCommandFrame[16]=chr(mem_e1)
	if dat_len >=26:
		mem_e2 = int(mem_e2,16)
		finsCommandFrame.append(chr(mem_e2))
		#finsCommandFrame[17]=chr(mem_e2)

#	test = ('TOMA')
#	test = list(test)
#	finsCommandFrame.extend(test)
	

#*****************************************************************************************************	
	finsCommandFrame = "".join(finsCommandFrame)
	finsCommand = "".join(finsCommand)

	nc.send(finsCommand)
	nc.send(finsCommandFrame)
	nc.recv()
	nc.close()
#	rec =list(nc.recv())
#	for i in range(30,30+((mem_e1+mem_e2)*2)):print (rec[i],sep=' ', end='')
#	print ()

if __name__ == '__main__':
   main()
