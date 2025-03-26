import socket
import threading


def handle_receive(conn) -> None:
    """Continuously receive messages on that socket

    Arguments:
        socket -- _description_
    """
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"\n [Client]: {data}\n[Server]: ", end="")
        except:
            break
    print("[!] Server disconnected.")
    conn.close()


def handle_send(conn) -> None:
    """Continously send message on that socket

    Arguments:
        socket -- _description_
    """
    while True:
        msg = input("[Server]: ")
        conn.sendall(msg.encode())


def start_server(host: str, port: int) -> None:
    """_summary_

    Arguments:
        host -- _description_
        port -- _description_
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[*] Server listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"[+] Connection established with {addr}")

    # Start two threads: one for receiving, one for sending
    receive_thread = threading.Thread(target=handle_receive, args=(conn,), daemon=True)
    send_thread = threading.Thread(target=handle_send, args=(conn,), daemon=True)

    receive_thread.start()
    send_thread.start()

    # Prevent the main thread from exiting
    send_thread.join()  # Blocks until send_thread exits (which it won't unless connection is closed)


if __name__ == "__main__":
    host = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = int(input("Enter port: "))
    start_server(host, port)
