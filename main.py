#!/usr/bin/env python3
import os
import sys
from banner import display_banner
from scanner import VulnerabilityScanner
from ddos_attacks import DDoSAttacker

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def main_menu():
    clear_screen()
    display_banner()
    
    print("\n\033[1;36m[+] Main Menu:\033[0m")
    print("  1. Vulnerability Scanner")
    print("  2. DDoS Attack Tools")
    print("  3. Exit")
    
    choice = input("\n\033[1;33m[?] Select an option (1-3): \033[0m")
    return choice

def scan_menu():
    clear_screen()
    display_banner()
    
    print("\n\033[1;36m[+] Vulnerability Scanner:\033[0m")
    print("  1. Scan a URL")
    print("  2. Scan an IP Address")
    print("  3. Return to Main Menu")
    
    choice = input("\n\033[1;33m[?] Select an option (1-3): \033[0m")
    
    if choice == "1":
        target = input("\n[?] Enter target URL (e.g., http://example.com): ")
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        scanner = VulnerabilityScanner()
        scanner.scan_target(target)
        
    elif choice == "2":
        target = input("\n[?] Enter target IP address: ")
        scanner = VulnerabilityScanner()
        scanner.scan_target(target)
        
    elif choice == "3":
        return
        
    input("\n[Press Enter to continue...]")

def ddos_menu():
    clear_screen()
    display_banner()
    
    print("\n\033[1;36m[+] DDoS Attack Tools:\033[0m")
    print("  1. SYN Flood Attack")
    print("  2. HTTP/HTTPS Flood Attack")
    print("  3. UDP Flood Attack")
    print("  4. Return to Main Menu")
    
    choice = input("\n\033[1;33m[?] Select an option (1-4): \033[0m")
    
    if choice in ["1", "2", "3"]:
        target = input("\n[?] Enter target IP address: ")
        port = input("[?] Enter target port (default 80): ") or "80"
        duration = input("[?] Enter attack duration in seconds (default 30): ") or "30"
        
        attacker = DDoSAttacker()
        
        if choice == "1":
            attacker.syn_flood(target, int(port), int(duration))
        elif choice == "2":
            attacker.http_flood(target, int(port), int(duration))
        elif choice == "3":
            attacker.udp_flood(target, int(port), int(duration))
    
    input("\n[Press Enter to continue...]")

def main():
    while True:
        try:
            choice = main_menu()
            
            if choice == "1":
                scan_menu()
            elif choice == "2":
                ddos_menu()
            elif choice == "3":
                print("\n\033[1;32m[+] Thank you for using WebSeeker!\033[0m")
                sys.exit(0)
            else:
                print("\n\033[1;31m[!] Invalid option. Please try again.\033[0m")
                input("[Press Enter to continue...]")
                
        except KeyboardInterrupt:
            print("\n\033[1;31m[!] Operation cancelled by user.\033[0m")
            sys.exit(1)
        except Exception as e:
            print(f"\n\033[1;31m[!] An error occurred: {str(e)}\033[0m")
            input("[Press Enter to continue...]")

if __name__ == "__main__":
    main()
