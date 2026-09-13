# chat-encrypted-unencrypted

A small chat application designed to compare **unencrypted WebSocket communication (WS)** with **encrypted WebSocket communication (WSS/TLS)** and analyze both cases with Wireshark.

## Project structure

```text
chat-encrypted-unencrypted/
├── backend/                  # Unencrypted WebSocket server
├── backend_encrypted/        # WSS/TLS WebSocket server
├── frontend/                 # Web client
└── docs/                     # Wireshark test, evidence and comparison
```

- `backend/` runs the unencrypted server on `ws://127.0.0.1:8080`.
- `backend_encrypted/` runs the encrypted server on `wss://127.0.0.1:8443`.
- `frontend/` contains the client used to switch between both communication modes.
- `docs/` contains the Wireshark procedure, evidence checklist, comparison and video outline.

## Cryptographic approach

The encrypted mode uses **TLS**, which follows a hybrid cryptographic model:

- **Asymmetric cryptography** is used during the secure connection establishment and server authentication.
- **Symmetric cryptography** protects the application data after the TLS session is established.
- **Hybrid cryptography** combines both mechanisms to provide secure and efficient communication.

The project does not implement a cryptographic algorithm from scratch. The encrypted transport is provided by TLS.

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

## Generate the local TLS certificate

The encrypted server requires a local self-signed certificate for development.

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File backend_encrypted\generate_dev_certificate.ps1
```

### Git Bash / Linux / macOS

```bash
bash backend_encrypted/generate_dev_certificate.sh
```

The generated files are stored in:

```text
backend_encrypted/certificates/localhost-cert.pem
backend_encrypted/certificates/localhost-key.pem
```

These files are local development credentials and are intentionally ignored by Git.

## Run the project

Open two terminals from the project root.

### Terminal 1 — unencrypted server

```bash
python backend/server.py
```

Expected endpoint:

```text
ws://127.0.0.1:8080
```

### Terminal 2 — encrypted server

```bash
python backend_encrypted/server.py
```

Expected endpoint:

```text
wss://127.0.0.1:8443
```

## Open the frontend

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

The browser must show both connection states as **Connected** before testing both modes.

Because the WSS server uses a self-signed certificate, some browsers may require you to trust or import `localhost-cert.pem` locally before the encrypted connection is accepted.

## Basic test

1. Open the frontend in two browser windows.
2. Enter different names, for example `Alice` and `Bob`.
3. Select `UNENCRYPTED (WS)` in both windows and exchange messages.
4. Select `ENCRYPTED (WSS/TLS)` in both windows and repeat the test.
5. Confirm that both clients receive the messages in both modes.

## Wireshark and evidence

The complete capture procedure, expected observations, comparison table and video outline are documented in:

```text
docs/wireshark-test.md
```

Use only fictitious messages and capture traffic only in an authorized environment.
