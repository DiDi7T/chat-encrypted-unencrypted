# chat-encrypted-unencrypted

A chat application that will allow for a practical comparison between **unencrypted** and **encrypted** communication.

## Project Structure

The project is divided into three main components:

- `backend/`: Contains the unencrypted WebSocket server (WS) running on port 8080.
- `backend_encrypted/`: Contains the encrypted WebSocket server (WSS) running on port 8443, along with the scripts to generate local TLS certificates.
- `frontend/`: Contains the unified HTML/JS client to interact with both servers simultaneously.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8+
- Wireshark (for network traffic analysis)
- A modern web browser (Chrome, Firefox, Edge)

## Setup and Execution Guide

### Step 1: Install Dependencies

Navigate to both backend folders and install the required Python packages (mainly the `websockets` library):

```bash
pip install -r backend/requirements.txt
pip install -r backend_encrypted/requirements.txt
```

### Step 2: Generate Certificates (First Time Only)

If you haven't generated certificates yet, you need to do this in the `backend_encrypted/` directory. Run the generation script:

```bash
cd backend_encrypted
bash generate_dev_certificates.sh
cd ..
```

This will create `cert.pem` (private key) and `key.pem` (public key) files in the same directory.

> **Security Warning**: These are **self-signed certificates**. When you open the frontend, your browser will show a security warning. This is expected for this educational exercise.

### Step 3: Start the Servers

Open **two terminals**.

Terminal 1 (Unencrypted Server):

```bash
cd backend
python server.py
```

Terminal 2 (Encrypted Server):

```bash
cd backend_encrypted
python server.py
```

In the second terminal, you should see output indicating the server is running on `ws://localhost:8080`.

### Step 4: Start the Encrypted Server (WSS)

In a **new terminal**, navigate to the `backend_encrypted/` directory and run:

```bash
python server.py
```

You should see output indicating the server is running on `wss://localhost:8443`.

### Step 5: Open the Chat Client

Open the `frontend/index.html` (drag and drop it into your browser) file in your web browser.

## Practical Exercises

Once the application is running, perform the following tests to demonstrate the difference between WS and WSS:

### Exercise 1: Plain Text Observation (WS)

1. In the "Chat Texto Plano" window, send a message.
2. Open Wireshark on the "Ethernet" or "Local Area Connection" interface.
3. In Wireshark, filter by protocol: `websocket`.
4. Observe the network packets. You will see the exact text message (e.g., "Hello") in plain text within the WebSocket frames.
5. Try to identify the destination IP address and port (should be [IP_ADDRESS]).

### Exercise 2: Encrypted Traffic Observation (WSS)

1. In the "Chat Cifrado" window, send a message.
2. Look at your Wireshark capture (you may need to stop and restart the capture to see new packets).
3. Filter by protocol: `websocket`.
4. You will see WebSocket frames, but the **payload (the actual message data) will be encrypted**. You will NOT be able to read the plain text.
5. Observe the TLS Handshake traffic (look for `Client Hello`, `Server Hello`) to confirm the secure connection is established.

### Exercise 3: Comparison

Write a brief report comparing:

- The ease of implementation (WS is simpler).
- The security implications (WSS protects against eavesdropping).
- What information is visible in a packet analyzer for each protocol.
