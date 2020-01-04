import socket


sock = socket.socket()
sock.connect(("localhost", 8080))

# --------------------------------
# Register
sock.sendall("R:1234567890123456".encode())

msg, data = sock.recv(2**12).decode().split(":", 1)
print("Recv", msg, data)

sock.sendall("C:".encode())
