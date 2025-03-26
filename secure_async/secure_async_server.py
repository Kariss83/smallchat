import asyncio
import ssl


async def handle_client(reader, writer):
    """Handles incoming messages from a client and allows sending messages"""
    addr = writer.get_extra_info("peername")
    print(f"[+] Secure connection established with {addr}")

    async def receive():
        while True:
            try:
                data = await reader.read(1024)  # Non-blocking receive
                if not data:
                    break
                print(f"\n[Client]: {data.decode()}\n[Server]: ", end="")
            except:
                break
        print("[!] Client disconnected.")
        writer.close()
        await writer.wait_closed()

    async def send():
        while True:
            msg = await asyncio.to_thread(input, "[Server]: ")  # Non-blocking input
            writer.write(msg.encode())
            await writer.drain()

    # Run receive and send tasks concurrently
    await asyncio.gather(receive(), send())


async def start_secure_server(host, port):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    server = await asyncio.start_server(handle_client, host, port, ssl=ssl_context)
    addr = server.sockets[0].getsockname()
    print(f"[*] Secure server listening on {addr}...")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    host = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = int(input("Enter port: "))
    asyncio.run(start_secure_server(host, port))
