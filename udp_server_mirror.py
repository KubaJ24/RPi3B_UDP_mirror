# UDP Server
# Mirrors messages sent

import socket

print("# --UDP Server mirror--")
print("# Ctrl+C or 'shutdown' to exit program")

localPort = 8888
serverAddress = "192.168.5.136"
bufferSize = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_ip_address():
	ip_addr = ''
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip_addr = s.getsockname()[0]
	s.close()
	return ip_addr

def udp_init():
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.bind(('', localPort))
	print("UDP Server: {}:{}".format(get_ip_address(), localPort))

def main():
	while True:
		data, addr = sock.recvfrom(bufferSize)
		decoded_data = data.decode('utf-8')
		print("Received message: '{}' from {}".format(decoded_data, addr))
		sock.sendto("Message received OK".encode(), addr)

		if decoded_data == 'info':
			message = "Raspberry PI 3, server address: {}, port: {}".format(serverAddress, localPort)
			sock.sendto(message.encode(), addr)

		if decoded_data == 'shutdown':
			sock.sendto("Shutting down the server...".encode(), addr)
			print("User: {} shut the server down".format(addr))
			break

if __name__ == '__main__':
	udp_init()
	main()
