# chat-encrypted-unencrypted

A small chat application used to compare **unencrypted WebSocket communication (WS)** with **encrypted WebSocket communication (WSS/TLS)**.

## Project structure

```text
chat-encrypted-unencrypted/
├── backend/              # Unencrypted WebSocket server
├── backend_encrypted/    # Encrypted WSS/TLS server
├── frontend/             # Web client
└── docs/                 # Wireshark test
```

- `backend/` runs on `ws://127.0.0.1:8080`.
- `backend_encrypted/` runs on `wss://127.0.0.1:8443`.
- `frontend/` lets the user switch between both communication modes.

## Cryptographic approach

The encrypted mode uses **TLS**.

TLS combines asymmetric and symmetric cryptography. Asymmetric cryptography is used during the secure connection setup and server authentication. After the session is established, symmetric cryptography protects the application data.

The project does not implement a cryptographic algorithm from scratch. Encryption is provided by TLS.

## Requirements

- Python 3.11 or newer
- `pip`
- OpenSSL
- A modern web browser
- Wireshark
- Npcap on Windows for loopback traffic capture

## Install dependencies

From the project root:

```bash
python -m pip install -r backend/requirements.txt
python -m pip install -r backend_encrypted/requirements.txt
```

## Generate the TLS certificate

The encrypted server uses a local self-signed certificate.

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File backend_encrypted\generate_dev_certificate.ps1
```

### Git Bash / Linux / macOS

```bash
bash backend_encrypted/generate_dev_certificate.sh
```

The certificate and private key are generated inside:

```text
backend_encrypted/certificates/
```

These files are used only for local development and are ignored by Git.

## Run the project

Open two terminals from the project root.

### Terminal 1 — unencrypted server

```bash
python backend/server.py
```

### Terminal 2 — encrypted server

```bash
python backend_encrypted/server.py
```

Then open the frontend.

### Windows

```powershell
start frontend\index.html
```

### Linux

```bash
xdg-open frontend/index.html
```

### macOS

```bash
open frontend/index.html
```

For a basic test, open the frontend in two windows, use different names such as `Alice` and `Bob`, and send messages in both `UNENCRYPTED (WS)` and `ENCRYPTED (WSS/TLS)` modes.

## Project resources

- [Wireshark test](docs/wireshark-test.md)
- [Team video]()
