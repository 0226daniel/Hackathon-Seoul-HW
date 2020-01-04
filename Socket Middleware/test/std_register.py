import socket


sock = socket.socket()
sock.connect(("localhost", 8080))

# --------------------------------
# Register Hostname
sock.sendall("R:1234567890123456".encode())
msg, data = sock.recv(2**12).decode().split(":", 1)
print("Recv", msg, data)

input("Enter to publish GPS")

# Register GPS
sock.sendall("G:1234567890123456:37.490762,126.8844066".encode())
msg, data = sock.recv(2**12).decode().split(":", 1)
print("Recv", msg, data)
