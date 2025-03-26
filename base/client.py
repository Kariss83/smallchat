import socket


def start_client(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        print(f"[+] Connected to {server_ip}:{server_port}")

        while True:
            msg = input("[Client]: ")
            client_socket.sendall(msg.encode())
            if msg.lower() == "exit":
                print("[!] Disconnecting...")
                break
            response = client_socket.recv(1024).decode()
            print(f"[Server]: {response}")


if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    start_client(server_ip, server_port)
