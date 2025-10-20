# 🔧 Docker Troubleshooting Guide for Windows

## Common Issues and Solutions

### Issue 1: Docker Desktop Not Running

**Error Message:**
```
error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

**Cause:** Docker Desktop is not running or not installed.

**Solution:**

#### A. Install Docker Desktop (if not installed)
1. Download from: https://www.docker.com/products/docker-desktop/
2. Run the installer
3. Restart your computer
4. Enable WSL 2 if prompted

#### B. Start Docker Desktop
1. Press `Win + S` and search for "Docker Desktop"
2. Click to open Docker Desktop
3. Wait for the whale icon to appear in system tray (bottom right)
4. Wait until status shows "Docker Desktop is running"
5. This may take 1-2 minutes on first start

#### C. Verify Docker is Running
Run the verification script:
```cmd
docker-verify.bat
```

Or manually check:
```cmd
docker --version
docker info
docker ps
```

---

### Issue 2: WSL 2 Not Installed

**Error Message:**
```
Docker Desktop requires Windows Subsystem for Linux (WSL) 2
```

**Solution:**

#### Enable WSL 2 (Administrator PowerShell)
```powershell
# Run PowerShell as Administrator

# Enable WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
shutdown /r /t 0

# After restart, set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu (optional but recommended)
wsl --install -d Ubuntu
```

---

### Issue 3: Version Warning in docker-compose.yml

**Warning Message:**
```
the attribute `version` is obsolete, it will be ignored
```

**Solution:** Already fixed! The `version` field has been removed from `docker-compose.yml`.

---

### Issue 4: Hyper-V Conflicts

**Error Message:**
```
Hardware assisted virtualization and data execution protection must be enabled in the BIOS
```

**Solution:**

#### Enable Virtualization in BIOS
1. Restart computer
2. Press BIOS key during boot (usually F2, F10, DEL, or ESC)
3. Find "Virtualization Technology" (Intel VT-x or AMD-V)
4. Enable it
5. Save and exit BIOS
6. Restart computer

#### Enable Hyper-V (Windows Pro/Enterprise)
```powershell
# Run as Administrator
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

---

### Issue 5: Docker Build Fails with Permission Errors

**Solution:**
```cmd
# Run Docker Desktop as Administrator
# Right-click Docker Desktop → Run as administrator
```

---

### Issue 6: Port Already in Use

**Error Message:**
```
Bind for 0.0.0.0:8080 failed: port is already allocated
```

**Solution:**

#### Option A: Change the port in docker-compose.yml
```yaml
ports:
  - "9090:8080"  # Use different host port
```

#### Option B: Find and stop the process using port 8080
```cmd
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

### Issue 7: Build Context Too Large

**Error Message:**
```
Sending build context to Docker daemon... (very large)
```

**Solution:** Already fixed! `.dockerignore` file excludes unnecessary files.

To verify:
```cmd
type .dockerignore
```

---

### Issue 8: Docker Daemon Not Responding

**Solution:**

#### Reset Docker Desktop
1. Right-click Docker Desktop icon in system tray
2. Select "Troubleshoot"
3. Click "Reset to factory defaults"
4. Restart Docker Desktop

---

## Step-by-Step: First Time Docker Setup on Windows

### 1. System Requirements
- ✅ Windows 10 64-bit: Pro, Enterprise, or Education (Build 16299 or later)
- ✅ Windows 11 64-bit
- ✅ 4GB RAM minimum (8GB recommended)
- ✅ BIOS virtualization enabled

### 2. Install WSL 2
```powershell
# Run as Administrator
wsl --install
```

Restart computer after installation.

### 3. Install Docker Desktop
1. Download: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
2. Run installer
3. Select "Use WSL 2 instead of Hyper-V"
4. Restart computer

### 4. Start Docker Desktop
1. Launch Docker Desktop from Start Menu
2. Accept terms if prompted
3. Wait for "Docker Desktop is running"

### 5. Verify Installation
```cmd
cd C:\NEXUS-AI.io
docker-verify.bat
```

### 6. Build AetherAI
```cmd
cd C:\NEXUS-AI.io
docker-compose build
```

---

## Quick Commands Reference

### Check Docker Status
```cmd
# Check if Docker is running
docker info

# Check Docker version
docker --version

# Check running containers
docker ps

# Check all containers
docker ps -a
```

### Docker Compose Commands
```cmd
# Build images
docker-compose build

# Start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Clean everything
docker-compose down -v --rmi all
```

### Docker Desktop Management
```cmd
# Check Docker Desktop service
sc query com.docker.service

# Restart Docker Desktop (from system tray)
# Right-click whale icon → Restart
```

---

## AetherAI Specific Commands

### Build and Run
```cmd
# Navigate to project
cd C:\NEXUS-AI.io

# Verify Docker is running
docker info

# Build the image
docker-compose build

# Start container
docker-compose up -d

# Access the application
docker exec -it aetherai_terminal python terminal/main.py
```

### Using the Management Script
```cmd
# Build
docker-manage.bat build

# Start
docker-manage.bat up

# Run application
docker-manage.bat run

# View logs
docker-manage.bat logs

# Stop
docker-manage.bat down
```

---

## Still Having Issues?

### 1. Check Docker Desktop Logs
```
%LOCALAPPDATA%\Docker\log.txt
```

### 2. Check System Requirements
```cmd
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
```

### 3. Run Docker Desktop Diagnostics
1. Right-click Docker Desktop icon
2. Select "Troubleshoot"
3. Click "Get support"
4. Review diagnostics

### 4. Restart Everything
```cmd
# Stop Docker Desktop
# Close from system tray

# Restart Docker service
net stop com.docker.service
net start com.docker.service

# Start Docker Desktop again
```

### 5. Complete Reinstall
1. Uninstall Docker Desktop
2. Delete `%APPDATA%\Docker`
3. Delete `%LOCALAPPDATA%\Docker`
4. Restart computer
5. Reinstall Docker Desktop

---

## Contact Support

If issues persist:
1. Check Docker Desktop documentation: https://docs.docker.com/desktop/windows/
2. Docker Community: https://forums.docker.com/
3. Project Issues: https://github.com/KunjShah95/NEXUS-AI.io/issues

---

**Last Updated:** October 20, 2025
