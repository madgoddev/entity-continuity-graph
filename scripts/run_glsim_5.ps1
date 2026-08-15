param(
    [int]$Port = 4014
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = (Get-Command python -ErrorAction Stop).Source
$Gltest = (Get-Command gltest -ErrorAction Stop).Source
$CompatibilityPath = Join-Path $ProjectRoot "tools\glsim_windows_sitecustomize"
$LogDirectory = Join-Path $ProjectRoot ".glsim"

New-Item -ItemType Directory -Force -Path $LogDirectory | Out-Null
$OutLog = Join-Path $LogDirectory "glsim.stdout.log"
$ErrLog = Join-Path $LogDirectory "glsim.stderr.log"

$PortProbe = [System.Net.Sockets.TcpClient]::new()
$PortOccupied = $false
try {
    $PortProbe.Connect("127.0.0.1", $Port)
    $PortOccupied = $PortProbe.Connected
}
catch [System.Net.Sockets.SocketException] {
    $PortOccupied = $false
}
finally {
    $PortProbe.Dispose()
}
if ($PortOccupied) {
    throw "Port $Port is already occupied; refusing to test against an unidentified process."
}

$PreviousPythonPath = $env:PYTHONPATH
$env:PYTHONPATH = $CompatibilityPath
$Process = Start-Process -FilePath $Python `
    -ArgumentList @("-m", "glsim", "--port", "$Port", "--validators", "5") `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog `
    -PassThru

try {
    $Ready = $false
    $Probe = '{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}'
    for ($Attempt = 0; $Attempt -lt 40; $Attempt++) {
        try {
            Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api" `
                -Method Post `
                -ContentType "application/json" `
                -Body $Probe `
                -TimeoutSec 1 | Out-Null
            $Ready = $true
            break
        }
        catch {
            Start-Sleep -Milliseconds 500
        }
    }
    if (-not $Ready) {
        throw "GLSim did not become ready. See $OutLog and $ErrLog"
    }

    & $Gltest `
        "tests\integration" `
        "-v" `
        "-s" `
        "--network" `
        "localnet" `
        "--rpc-url" `
        "http://127.0.0.1:$Port/api"
    if ($LASTEXITCODE -ne 0) {
        throw "GLSim integration tests failed with exit code $LASTEXITCODE"
    }
}
finally {
    if (-not $Process.HasExited) {
        Stop-Process -Id $Process.Id
    }
    $env:PYTHONPATH = $PreviousPythonPath
}
