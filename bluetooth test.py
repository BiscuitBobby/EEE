import socket

bd_addr = "B0:A7:32:F2:C2:22"  # itade address
port = 1

sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((bd_addr, port))

print("Connected")

sock.settimeout(1.0)
sock.send(b'*')
sock.send(b'hello')  # Send data as bytes
sock.send(b'|')
sock.send(b"I'm under the water")  # Send data as bytes

sock.close()
