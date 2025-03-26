import asyncio
import ssl


async def start_secure_client(server_ip, server_port):
    ssl_context = ssl.create_default_context()
    reader, writer = await asyncio.open_connection(
        server_ip, server_port, ssl=ssl_context
    )

    print(f"[+] Securely connected to {server_ip}:{server_port}")

    async def receive():
        while True:
            try:
                data = await reader.read(1024)  # Non-blocking receive
                if not data:
                    break
                print(f"\n[Server]: {data.decode()}\n[Client]: ", end="")
            except:
                break
        print("[!] Server disconnected.")
        writer.close()
        await writer.wait_closed()

    async def send():
        while True:
            msg = await asyncio.to_thread(input, "[Client]: ")  # Non-blocking input
            writer.write(msg.encode())
            await writer.drain()

    # Run both tasks concurrently
    await asyncio.gather(receive(), send())


if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    asyncio.run(start_secure_client(server_ip, server_port))
