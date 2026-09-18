import asyncio
import json
import os
import ssl
from datetime import datetime, timezone
from pathlib import Path

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed


# Uso una dirección local y un puerto fijo para que esta versión sea fácil de
# comparar con el servidor no cifrado.
HOST = "127.0.0.1"
PORT = 8443
CERTIFICATES_DIR = Path(__file__).parent / "certificates"
CERTIFICATE_FILE = CERTIFICATES_DIR / "localhost-cert.pem"
PRIVATE_KEY_FILE = CERTIFICATES_DIR / "localhost-key.pem"

# Mantengo aquí solamente las conexiones del modo cifrado.
connected_clients = set()


async def send_json(websocket, payload):
    """Convierto un diccionario de Python a JSON y lo envío al cliente."""
    await websocket.send(json.dumps(payload, ensure_ascii=False))


async def broadcast(payload):
    """Reenvío un mensaje únicamente a los clientes WSS conectados."""
    if not connected_clients:
        return

    message = json.dumps(payload, ensure_ascii=False)
    results = await asyncio.gather(
        *(client.send(message) for client in tuple(connected_clients)),
        return_exceptions=True,
    )

    for result in results:
        if isinstance(result, Exception):
            print(f"[ERROR] Error enviando mensaje: {result}")


async def handle_client(websocket):
    """Manejo una conexión WebSocket segura (WSS)."""
    connected_clients.add(websocket)
    remote_address = websocket.remote_address

    print(f"[CONNECTED] Cliente cifrado conectado: {remote_address}")
    print(f"[CLIENTS] Total (ENCRYPTED): {len(connected_clients)}")

    try:
        await send_json(
            websocket,
            {
                "type": "system",
                "mode": "ENCRYPTED",
                "message": "Connected to encrypted WebSocket server",
            },
        )

        async for raw_message in websocket:
            # En este punto TLS ya descifró el mensaje dentro del servidor.
            # Mientras viajaba por la red, el texto no iba en texto plano.
            print(f"[DECRYPTED RECEIVED] {raw_message}")

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

            sender = str(data.get("sender", "Anonymous")).strip()
            message = str(data.get("message", "")).strip()

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
                "mode": "ENCRYPTED",
                "sender": sender,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            print(f"[CHAT ENCRYPTED] {sender}: {message}")
            await broadcast(chat_message)

    except ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"[DISCONNECTED] Cliente cifrado desconectado: {remote_address}")
        print(f"[CLIENTS] Total (ENCRYPTED): {len(connected_clients)}")


def create_ssl_context():
    """Cargo el certificado TLS que necesito para ofrecer conexiones WSS."""
    if not CERTIFICATE_FILE.exists() or not PRIVATE_KEY_FILE.exists():
        raise FileNotFoundError(
            "No se encontraron los certificados TLS. Ejecuta primero: "
            "bash backend_encrypted/generate_dev_certificate.sh"
        )

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(CERTIFICATE_FILE, PRIVATE_KEY_FILE)
    return context


async def main():
    ssl_context = create_ssl_context()

    print("=" * 50)
    print("ENCRYPTED CHAT SERVER")
    print("=" * 50)
    print(f"Server running at wss://{HOST}:{PORT}")
    print("Mode: ENCRYPTED")
    print("TLS: ENABLED")
    print("Compression: DISABLED")
    print("=" * 50)

    server = await serve(
        handle_client,
        HOST,
        PORT,
        ssl=ssl_context,
        # También desactivo compresión para centrar la comparación en TLS.
        compression=None,
    )
    await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Server stopped.")
