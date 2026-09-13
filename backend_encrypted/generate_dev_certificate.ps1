$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$certificatesDir = Join-Path $scriptDir "certificates"

New-Item -ItemType Directory -Force -Path $certificatesDir | Out-Null

$opensslCommand = Get-Command openssl -ErrorAction SilentlyContinue
$opensslPath = $null

if ($opensslCommand) {
    $opensslPath = $opensslCommand.Source
} else {
    $gitCommand = Get-Command git -ErrorAction SilentlyContinue

    if ($gitCommand) {
        $gitCmdDir = Split-Path -Parent $gitCommand.Source
        $gitRoot = Split-Path -Parent $gitCmdDir
        $candidate = Join-Path $gitRoot "usr\bin\openssl.exe"

        if (Test-Path $candidate) {
            $opensslPath = $candidate
        }
    }
}

if (-not $opensslPath) {
    throw "No se encontró OpenSSL. Instálalo o ejecuta el script Bash desde Git Bash."
}

$keyFile = Join-Path $certificatesDir "localhost-key.pem"
$certificateFile = Join-Path $certificatesDir "localhost-cert.pem"

& $opensslPath req -x509 -newkey rsa:2048 -sha256 -nodes `
    -keyout $keyFile `
    -out $certificateFile `
    -days 30 `
    -subj "/CN=localhost" `
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

if ($LASTEXITCODE -ne 0) {
    throw "OpenSSL no pudo generar el certificado."
}

Write-Host "Certificado generado en: $certificatesDir"
Write-Host "Es autofirmado y solo debe usarse para desarrollo local."
