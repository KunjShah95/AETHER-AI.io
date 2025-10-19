<#
PowerShell Docker diagnostics and basic recovery helper for Docker Desktop (Windows).

Usage:
  - Run from an elevated PowerShell (recommended):
      .\scripts\check_docker.ps1
  - Non-elevated runs will still show checks but cannot restart services.

This script performs readonly checks, attempts a safe service restart if possible,
and collects a small log excerpt to %TEMP% for sharing.
#>

param()

function Run-Cmd {
    param($cmd)
    try {
        $out = & cmd.exe /c "$cmd" 2>&1
        return $out -join "`n"
    } catch {
        return "ERROR: $_"
    }
}

Write-Host "=== AetherAI Docker Diagnostic ===" -ForegroundColor Cyan

Write-Host "(1) docker info -> check engine connection"
try {
    $dockerInfo = & docker info 2>&1
    if ($LASTEXITCODE -eq 0) { Write-Host "docker info: OK" -ForegroundColor Green }
    else { Write-Host "docker info: FAILED" -ForegroundColor Yellow }
    Write-Host $dockerInfo
} catch {
    Write-Host "docker info: command failed - client likely present but engine unreachable." -ForegroundColor Red
}

Write-Host "`n(2) Service check: com.docker.service"
try {
    $svc = Get-Service -Name com.docker.service -ErrorAction SilentlyContinue
    if ($null -ne $svc) {
        Write-Host "Service 'com.docker.service' state: $($svc.Status)"
    } else {
        Write-Host "Service 'com.docker.service' not found (Docker Desktop may not be installed as a Windows service)." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Service query error: $_"
}

Write-Host "`n(3) Check Docker Desktop named pipe: \\.\\pipe\\dockerDesktopLinuxEngine"
try {
    $pipe = Test-Path \\"\\.\\pipe\\dockerDesktopLinuxEngine\\" -PathType Leaf
    Write-Host "Pipe exists: $pipe"
} catch {
    Write-Host "Pipe test failed: $_"
}

Write-Host "`n(4) WSL distributions (wsl -l -v)"
try {
    $wsl = wsl -l -v 2>&1
    Write-Host $wsl
} catch {
    Write-Host "wsl query failed: $_" -ForegroundColor Yellow
}

Write-Host "`n(5) WSL status (wsl --status)"
try {
    $status = wsl --status 2>&1
    Write-Host $status
} catch {
    Write-Host "wsl --status failed: $_" -ForegroundColor Yellow
}

Write-Host "`n(6) Docker contexts (docker context ls)"
try {
    $ctx = docker context ls 2>&1
    Write-Host $ctx
} catch {
    Write-Host "docker context ls failed: $_" -ForegroundColor Yellow
}

# If the engine seems down, attempt a safe restart of the service (if elevated)
$needRestart = $false
if ($dockerInfo -is [array]) {
    $joined = $dockerInfo -join "`n"
} else {
    $joined = [string]$dockerInfo
}
if ($joined -match "error.*pipe|cannot find the file|dockerDesktopLinuxEngine" -or $joined -match "Is the docker daemon running") {
    $needRestart = $true
}

if ($needRestart) {
    Write-Host "`nEngine appears down. Attempting safe restart if possible..." -ForegroundColor Yellow
    $isAdmin = ([bool]([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
    if (-not $isAdmin) {
        Write-Host "Not running as Administrator. Attempting non-elevated recovery: starting Desktop executable." -ForegroundColor Yellow
        try {
            $exe = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
            if (Test-Path $exe) {
                Start-Process -FilePath $exe -WindowStyle Minimized
                Write-Host "Started Docker Desktop executable. Wait 30 seconds and re-run this script or check \`docker info\`." -ForegroundColor Green
            } else {
                Write-Host "Docker Desktop executable not found at: $exe" -ForegroundColor Red
            }
        } catch {
            Write-Host "Failed to start Docker Desktop: $_" -ForegroundColor Red
        }
    } else {
        # Elevated - attempt service restart
        try {
            if (Get-Service -Name com.docker.service -ErrorAction SilentlyContinue) {
                Write-Host "Restarting com.docker.service..." -ForegroundColor Cyan
                Restart-Service -Name com.docker.service -Force -ErrorAction Stop
                Start-Sleep -Seconds 6
                Write-Host "Restart requested. Wait a few seconds and retry docker info." -ForegroundColor Green
            } else {
                Write-Host "com.docker.service not present; starting Docker Desktop executable instead." -ForegroundColor Yellow
                $exe = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
                if (Test-Path $exe) { Start-Process -FilePath $exe -WindowStyle Minimized }
            }
        } catch {
            Write-Host "Service restart failed: $_" -ForegroundColor Red
        }
    }
}

Write-Host "`n(7) Collecting recent Docker Desktop logs to TEMP for inspection"
try {
    $outDir = Join-Path $env:TEMP "aetherai_docker_diag"
    New-Item -Path $outDir -ItemType Directory -Force | Out-Null
    $logGlob = Join-Path $env:APPDATA "Docker\log\*.log"
    $files = Get-ChildItem -Path $logGlob -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    if ($files -and $files.Count -gt 0) {
        $take = 5
        foreach ($f in $files[0..([math]::Min($take-1, $files.Count-1))]) {
            $dest = Join-Path $outDir $f.Name
            Get-Content -Path $f.FullName -Tail 500 -ErrorAction SilentlyContinue | Out-File -FilePath $dest -Encoding UTF8
        }
        Write-Host "Logs saved to: $outDir" -ForegroundColor Green
    } else {
        Write-Host "No Docker Desktop log files found under $env:APPDATA\Docker\log" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Failed to collect logs: $_" -ForegroundColor Red
}

Write-Host "`nDiagnostic complete. If issues persist, consider restarting your PC or reinstalling Docker Desktop. See scripts/DockerTroubleshoot.md for next steps." -ForegroundColor Cyan
