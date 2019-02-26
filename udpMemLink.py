import sys
import nclib
import time
while True:
	nc = nclib.Netcat(('10.210.200.191', 1024), udp=True, verbose=False)
	nc.echo_hex = True
	nc.send(b'B\x00\x00\x00\x00\x00\x00\x06\x1bR\x00\x00\x00\x01')
	response = list(nc.recv())
	if response[11]==1:
		sys.stdout.write("\ron ")
	else: sys.stdout.write("\roff")
	sys.stdout.flush()
	nc.close()
	#time.sleep(1)
