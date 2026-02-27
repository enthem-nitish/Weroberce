import requests
import socket
import subprocess
import sys
from urllib.parse import urlparse

class VulnerabilityScanner:
    def __init__(self):
        self.results = []
        
    def scan_target(self, target):
        print(f"\n\033[1;36m[*] Starting scan on: {target}\033[0m")
        
        # Determine if target is URL or IP
        if self.is_url(target):
            print("[*] Target identified as URL")
            self.scan_url(target)
        else:
            print("[*] Target identified as IP address")
            self.scan_ip(target)
            
        self.generate_report(target)
    
    def is_url(self, target):
        try:
            result = urlparse(target)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def scan_url(self, url):
        print("\n[*] Testing for XSS vulnerabilities...")
        self.test_xss(url)
        
        print("[*] Testing for SQL injection vulnerabilities...")
        self.test_sqli(url)
        
        print("[*] Testing for LFI vulnerabilities...")
        self.test_lfi(url)
        
        print("[*] Testing for open ports...")
        self.scan_ports(urlparse(url).hostname)
    
    def scan_ip(self, ip):
        print("[*] Scanning for open ports...")
        self.scan_ports(ip)
        
        # Try to detect web services
        print("[*] Testing for web services...")
        for port in [80, 443, 8080, 8888]:
            try:
                scheme = "https" if port == 443 else "http"
                url = f"{scheme}://{ip}:{port}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] Web server found on port {port}")
                    print("[*] Testing for web vulnerabilities...")
                    self.test_xss(url)
                    self.test_sqli(url)
                    self.test_lfi(url)
                    break
            except:
                continue
    
    def test_xss(self, url):
        payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            'javascript:alert("XSS")'
        ]
        
        vulnerable = False
        for payload in payloads:
            try:
                test_url = f"{url}?q={payload}" if "?" in url else f"{url}/?q={payload}"
                response = requests.get(test_url, timeout=5)
                if payload in response.text:
                    print(f"[!] Potential XSS vulnerability found with payload: {payload}")
                    self.results.append(f"XSS Vulnerability: {payload}")
                    vulnerable = True
            except:
                continue
        
        if not vulnerable:
            print("[-] No XSS vulnerabilities found")
    
    def test_sqli(self, url):
        payloads = [
            "'",
            "''",
            "`",
            "``",
            "' OR '1'='1",
            "' OR 1=1-- -"
        ]
        
        vulnerable = False
        for payload in payloads:
            try:
                test_url = f"{url}?id={payload}" if "?" in url else f"{url}/?id={payload}"
                response = requests.get(test_url, timeout=5)
                content = response.text.lower()
                if "error" in content or "syntax" in content or "mysql" in content or "ora-" in content:
                    print(f"[!] Potential SQL injection vulnerability found with payload: {payload}")
                    self.results.append(f"SQL Injection Vulnerability: {payload}")
                    vulnerable = True
            except:
                continue
        
        if not vulnerable:
            print("[-] No SQL injection vulnerabilities found")
    
    def test_lfi(self, url):
        payloads = [
            "../../../../etc/passwd",
            "....//....//....//....//etc/passwd",
            "..\\..\\..\\..\\..\\..\\etc\\passwd"
        ]
        
        vulnerable = False
        for payload in payloads:
            try:
                test_url = f"{url}?file={payload}" if "?" in url else f"{url}/?file={payload}"
                response = requests.get(test_url, timeout=5)
                if "root:" in response.text or "daemon:" in response.text:
                    print(f"[!] Potential LFI vulnerability found with payload: {payload}")
                    self.results.append(f"LFI Vulnerability: {payload}")
                    vulnerable = True
            except:
                continue
        
        if not vulnerable:
            print("[-] No LFI vulnerabilities found")
    
    def scan_ports(self, host):
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        open_ports = []
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    print(f"[+] Port {port} is OPEN")
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        if open_ports:
            self.results.append(f"Open Ports: {', '.join(map(str, open_ports))}")
        else:
            print("[-] No common open ports found")
    
    def generate_report(self, target):
        print("\n\033[1;36m[*] Generating report...\033[0m")
        
        # Create report filename from target
        filename = target.replace("://", "_").replace("/", "_").replace(":", "_") + "_scan_report.txt"
        
        with open(filename, 'w') as f:
            f.write("WebSeeker Vulnerability Scan Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Target: {target}\n")
            f.write(f"Scan Date: {self.get_timestamp()}\n")
            f.write("\nFindings:\n")
            f.write("-" * 20 + "\n")
            
            if self.results:
                for finding in self.results:
                    f.write(f"- {finding}\n")
            else:
                f.write("- No vulnerabilities found\n")
                
            f.write("\nReport generated by WebSeeker\n")
            f.write("Developed by Nitish Sharma\n")
        
        print(f"[+] Report saved to: {filename}")
        
        # Show summary
        if self.results:
            print("\n\033[1;31m[!] Vulnerabilities found:\033[0m")
            for finding in self.results:
                print(f"  - {finding}")
        else:
            print("\n\033[1;32m[+] No vulnerabilities found\033[0m")
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
