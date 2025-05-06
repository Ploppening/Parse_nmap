import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from termcolor import colored
from datetime import datetime

def run_nmap(args):
    """Runs an Nmap scan and saves results."""
    ip = args[-1]
    result_dir = Path("nmap_results")
    result_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M")
    output_base = result_dir / f"{ip}_{timestamp}"

    if ping_check(ip) == True:
        command = ["nmap"] + args + ["-oA", str(output_base)]
        print(colored(f"[+] Running sudo nmap {" ".join(args)}", "white"))
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_base, ip, " ".join(command)
    else:
        print(colored("[-] Host may be down or is unreachable.", "red"))
        sys.exit(1)

def ping_check(ip):
    """Check if the target is up before running Nmap."""
    command = ["ping", "-c", "1", "-W", "1", ip]
    # print(colored(f"[+] Running {' '.join(command)}", "white"))
    print(colored("[+] Ping to check connection to host...", "white"))
    try:
        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
    except FileNotFoundError:
        print(colored("[-] Ping command not found. Please ensure it is installed.", "red"))
    except Exception as e:
        print(colored(f"[-] Ping check failed with error: {e}", "red"))
    return False


def parse_nmap_xml(xml_file, ip):
    """Parses an existing Nmap XML file and formats output."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        host = root.find("host")
        if host is None or host.find("status").attrib["state"] != "up":
            print(colored("[-] Host is down or unreachable.", "red"))
            return

        # Extract OS and hostname details
        hostname = host.find("hostnames/hostname")
        hostname_text = hostname.attrib["name"] if hostname is not None else ip

        os_match = host.find("os/osmatch")
        os_text = os_match.attrib["name"] if os_match is not None else "Unknown OS"

        print(colored(f"\n[+] Results for {hostname_text} running {os_text}", "green"))

        ports = host.find("ports")
        if ports is None:
            print(colored("[-] No open ports found.", "red"))
            return
        
        # Headings
        print(f"{colored(f'\n{"PORT":>10}', 'magenta')} | {colored("STATE", 'green'):>14} | {colored("SERVICE", 'yellow'):<20} | {colored("VERSION", 'yellow')}")
        
        for port in ports.findall("port"):
            port_id = port.attrib["portid"]
            state = port.find("state").attrib["state"]
    
            # Extract service information
            service = port.find("service")
            if service is not None:
                service_name = service.attrib.get("name", "unknown")
                service_product = service.attrib.get("product", "N/A")
                service_version = service.attrib.get("version", "N/A")
                
                # Combine service product and version if available
                if service_product and service_version != "N/A":
                    version = f"{service_product} {service_version}"
                else:
                    version = service_product or service_name  # Fallback to service name if product is not available
            else:
                version = "unknown N/A"

            state_text = colored(state.upper(), "white") if state == "open" else colored(state.upper(), "red")
            print(f"{colored(f'\nPort {port_id:>5}', 'magenta')} | {state_text:>14} | {colored(service_name, 'yellow'):<20} | {colored(version, 'yellow')}")

            for script in port.findall("script"):
                print(colored(f"  └── {script.attrib['id']}: {script.attrib['output']}", "blue"))
        
        # Parse additional scripts (e.g., OS details, other host scripts)
        print(colored(f"\n[+] Host script results", "white"))
        for script in host.findall("hostscript/script"):
            hostid = f"\n  └── {script.attrib['id']}:"
            hostbody = colored(f" {script.attrib['output']}", "blue")
            print(f"{hostid}{hostbody}")
                       
    except ET.ParseError:
        print(colored("[-] Error parsing XML file!", "red"))

def display_nmap_output(nmap_file):
    """Displays the original Nmap output file."""
    print(colored(f"\n[+] Original Nmap Output: {nmap_file}", "white"))
    # try:
    #     with open(nmap_file, "r") as f:
    #         print(f.read())
    # except FileNotFoundError:
    #     print(colored("[-] Nmap output file not found!", "red"))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_nmap.py <nmap_args> <IP> OR python3 parse_nmap.py <nmap_file.xml>")
        sys.exit(1)

    if sys.argv[1].endswith(".xml"):
        xml_file = sys.argv[1]
        ip = os.path.basename(xml_file).replace(".xml", "").split("/")[-1]
        nmap_file = xml_file.replace(".xml", ".nmap")
    else:
        output_base, ip, _ = run_nmap(sys.argv[1:])
        xml_file = f"{output_base}.xml"
        nmap_file = f"{output_base}.nmap"

    if os.path.exists(xml_file):
        parse_nmap_xml(xml_file, ip)
    else:
        print(colored("[-] XML output not found!", "red"))

    # Call the function to display the original Nmap output
    if os.path.exists(nmap_file):
        display_nmap_output(nmap_file)

if __name__ == "__main__":
    main()
