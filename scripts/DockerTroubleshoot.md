# Docker Desktop (Windows) Troubleshooting — AetherAI helper

This short guide lists common steps to resolve the pipe/engine errors on Windows
when Docker client reports: "open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.".

1) Ensure Docker Desktop is running
   - Open Docker Desktop from Start Menu and confirm it says "Docker is running".
   - If it shows an error, click Troubleshoot in the UI and follow suggestions.

2) Use the provided diagnostic script
   - Run `scripts\check_docker.bat` from the repository root (double-click or run from cmd.exe).
   - The script will attempt to collect logs to `%TEMP%\aetherai_docker_diag` and will attempt a safe restart when run elevated.

3) Verify WSL 2 is available and default
   - In an elevated PowerShell:

     ```powershell
     wsl --status
     wsl -l -v
     wsl --set-default-version 2
     ```

   - If WSL isn't enabled, enable VirtualMachinePlatform and WSL via DISM (then reboot):

     ```powershell
     dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
     dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
     ```

4) Restart Docker Desktop (Try GUI -> Quit Docker Desktop, then relaunch) or restart the service:
   - Elevated PowerShell:

     ```powershell
     Restart-Service -Name com.docker.service -Force
     ```

5) Reset to factory defaults (last resort)
   - Docker Desktop -> Troubleshoot -> Reset to factory defaults. This removes images/containers/settings — only use if acceptable.

6) Reinstall Docker Desktop
   - Download the latest installer from the Docker website and install using the WSL2 backend: [https://www.docker.com/get-started](https://www.docker.com/get-started)

7) If all else fails
   - Attach the diagnostics bundle created by the GUI Troubleshoot to an issue, or paste the content of `%TEMP%\aetherai_docker_diag` into the issue.
- You can also use the GitHub Actions CI that builds the Docker image on each push — this avoids needing a local Docker engine for validation.
