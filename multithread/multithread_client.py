import socket
import threading


def handle_receive(socket: socket.socket) -> None:
    """Continuously receive messages on that socket

    Arguments:
        socket -- _description_
    """
    while True:
        try:
            data = socket.recv(1024).decode()
            if not data:
                break
            print(f"\n [Server]: {data}\n[Client]: ", end="")
        except:
            break
    print("[!] Server disconnected.")
    socket.close()


def handle_send(socket: socket.socket) -> None:
    """Continously send message on that socket

    Arguments:
        socket -- _description_
    """
    while True:
        msg = input("[Client]: ")
        socket.sendall(msg.encode())


def start_client(server_ip: str, server_port: int) -> None:
    """_summary_

    Arguments:
        server_ip -- _description_
        server_port -- _description_
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"[+] Securely connected to {server_ip}:{server_port}")

    # Start two threads: one for receiving, one for sending
    receive_thread = threading.Thread(
        target=handle_receive, args=(client_socket,), daemon=True
    )
    send_thread = threading.Thread(
        target=handle_send, args=(client_socket,), daemon=True
    )

    receive_thread.start()
    send_thread.start()

    send_thread.join()


if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    start_client(server_ip, server_port)
