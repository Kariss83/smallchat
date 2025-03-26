import socket
import ssl
import threading


def handle_receive(conn):
    """Continuously receives messages from the client"""
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"\n[Client]: {data}\n[Server]: ", end="")
        except:
            break
    print("[!] Client disconnected.")
    conn.close()


def handle_send(conn):
    """Continuously sends messages to the client"""
    while True:
        msg = input("[Server]: ")
        conn.sendall(msg.encode())


def start_secure_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    secure_socket = context.wrap_socket(server_socket, server_side=True)

    secure_socket.bind((host, port))
    secure_socket.listen()
    print(f"[*] Secure server listening on {host}:{port}...")

    conn, addr = secure_socket.accept()
    print(f"[+] Secure connection established with {addr}")

    # Start two threads: one for receiving, one for sending
    threading.Thread(target=handle_receive, args=(conn,), daemon=True).start()
    threading.Thread(target=handle_send, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    host = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = int(input("Enter port: "))
    start_secure_server(host, port)
