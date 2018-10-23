import socket



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	m = raw_input()
	sock.sendto(m, ('192.168.4.1', 3001))