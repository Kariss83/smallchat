import socket
import ssl
import threading


def handle_receive(secure_socket):
    """Continuously receives messages from the server"""
    while True:
        try:
            data = secure_socket.recv(1024).decode()
            if not data:
                break
            print(f"\n[Server]: {data}\n[Client]: ", end="")
        except:
            break
    print("[!] Server disconnected.")
    secure_socket.close()


def handle_send(secure_socket):
    """Continuously sends messages to the server"""
    while True:
        msg = input("[Client]: ")
        secure_socket.sendall(msg.encode())


def start_secure_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(client_socket, server_hostname=server_ip)

    secure_socket.connect((server_ip, server_port))
    print(f"[+] Securely connected to {server_ip}:{server_port}")

    # Start two threads: one for receiving, one for sending
    threading.Thread(target=handle_receive, args=(secure_socket,), daemon=True).start()
    threading.Thread(target=handle_send, args=(secure_socket,), daemon=True).start()


if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    start_secure_client(server_ip, server_port)
