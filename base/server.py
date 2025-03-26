import socket


def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[*] Listening on {host}:{port}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"[+] Connection established from {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data or data.lower() == "exit":
                    print("[!] Connection closed")
                    break
                print(f"[Client]: {data}")
                response = input("[Server]: ")
                conn.sendall(response.encode())


if __name__ == "__main__":
    host = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = int(input("Enter port: "))
    start_server(host, port)
