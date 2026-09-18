import asyncio
import json
from datetime import datetime, timezone

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed


HOST = "127.0.0.1"
PORT = 8080

# Conexiones WebSocket actualmente conectadas.
connected_clients = set()


async def send_json(websocket, payload):
    """Envía un diccionario de Python como JSON."""
    await websocket.send(
        json.dumps(payload, ensure_ascii=False)
    )


async def broadcast(payload):
    """Envía un mensaje a todos los clientes conectados."""
    if not connected_clients:
        return

    message = json.dumps(payload, ensure_ascii=False)

    results = await asyncio.gather(
        *(
            client.send(message)
            for client in connected_clients
        ),
        return_exceptions=True,
    )

    # Por ahora solamente informamos errores.
    for result in results:
        if isinstance(result, Exception):
            print(f"[ERROR] Error enviando mensaje: {result}")


async def handle_client(websocket):
    """
    Maneja una conexión WebSocket.

    Cada cliente conectado ejecuta esta función
    independientemente.
    """

    connected_clients.add(websocket)

    remote_address = websocket.remote_address

    print(f"[CONNECTED] Cliente conectado: {remote_address}")
    print(f"[CLIENTS] Total: {len(connected_clients)}")

    try:
        # Mensaje inicial únicamente para este cliente.
        await send_json(
            websocket,
            {
                "type": "system",
                "mode": "UNENCRYPTED",
                "message": "Connected to unencrypted WebSocket server",
            },
        )

        # Escuchamos mensajes permanentemente.
        async for raw_message in websocket:

            # IMPORTANTE PARA EL LAB:
            # aquí estamos viendo exactamente lo recibido.
            print(f"[PLAINTEXT RECEIVED] {raw_message}")

            try:
                data = json.loads(raw_message)

            except json.JSONDecodeError:
                await send_json(
                    websocket,
                    {
                        "type": "error",
                        "message": "Message must be valid JSON",
                    },
                )
                continue

            sender = str(
                data.get("sender", "Anonymous")
            ).strip()

            message = str(
                data.get("message", "")
            ).strip()

            if not message:
                await send_json(
                    websocket,
                    {
                        "type": "error",
                        "message": "Message cannot be empty",
                    },
                )
                continue

            chat_message = {
                "type": "chat",
                "sender": sender,
                "message": message,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

            print(
                f"[CHAT] {sender}: {message}"
            )

            # Enviar el mensaje a todos.
            await broadcast(chat_message)

    except ConnectionClosed:
        pass

    finally:
        connected_clients.discard(websocket)

        print(
            f"[DISCONNECTED] Cliente desconectado: "
            f"{remote_address}"
        )
        print(
            f"[CLIENTS] Total: "
            f"{len(connected_clients)}"
        )


async def main():

    print("=" * 50)
    print("UNENCRYPTED CHAT SERVER")
    print("=" * 50)

    print(
        f"Server running at ws://{HOST}:{PORT}"
    )

    print("Mode: UNENCRYPTED")
    print("TLS: DISABLED")
    print("Compression: DISABLED")
    print("=" * 50)

    server = await serve(
        handle_client,
        HOST,
        PORT,

        # Lo desactivamos para facilitar
        # el análisis con Wireshark
        compression=None,
    )

    await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n[SERVER] Server stopped.")