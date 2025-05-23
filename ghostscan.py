# ghostscan.py - Juanita Zero: GhostLayer Vault Scanner (Lite Edition)
import os
import socket
import platform
import hashlib
import time

def system_fingerprint():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    osys = platform.system()
    arch = platform.machine()
    return f"{host}-{ip}-{osys}-{arch}"

def scan_artifacts():
    sus_files = []
    targets = ["/tmp", "/var", os.getenv("APPDATA") or "", os.path.expanduser("~")]
    flags = [".ghost", ".sig", ".tmp", "._", ".zero"]
    for t in targets:
        if os.path.exists(t):
            for root, _, files in os.walk(t):
                for f in files:
                    for flag in flags:
                        if flag in f:
                            sus_files.append(os.path.join(root, f))
    return sus_files

def report(fingerprint, artifacts):
    hash_fp = hashlib.sha256(fingerprint.encode()).hexdigest()
    log = f"[JUANITA-ZERO SCAN REPORT]\n\nID: {hash_fp}\nSystem: {fingerprint}\n\nArtifacts:\n"
    log += "\n".join(artifacts) if artifacts else "None Detected"
    with open("ghostscan_report.txt", "w") as f:
        f.write(log)
    print("Scan complete. Report saved to ghostscan_report.txt")

def self_destruct():
    time.sleep(10)
    os.remove(__file__)

if __name__ == "__main__":
    fp = system_fingerprint()
    results = scan_artifacts()
    report(fp, results)
    self_destruct()
