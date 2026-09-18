#!/usr/bin/env bash

# Genero un certificado autofirmado solo para las pruebas locales del laboratorio.
# Incluyo localhost y 127.0.0.1 para que el navegador reconozca ambas direcciones.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
certificates_dir="$script_dir/certificates"

mkdir -p "$certificates_dir"

openssl req -x509 -newkey rsa:2048 -sha256 -nodes \
  -keyout "$certificates_dir/localhost-key.pem" \
  -out "$certificates_dir/localhost-cert.pem" \
  -days 30 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo "Certificado generado en: $certificates_dir"
echo "Es autofirmado y solo debe usarse para desarrollo local."
