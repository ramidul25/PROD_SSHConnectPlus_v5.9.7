"""
************************************************************
*  SSHConnect+ - v5.9.7   (Will Expire on 31-08-2026)      *
*  Designed for: ASDA NewCo Environment                    *
*  Developed by: TCS-Network Team (Ramidul)                *
*  Copyright © 2025 TCS-Network Team. All Rights Reserved. *
*  Unauthorized distribution or modification is prohibited.*
************************************************************
"""
import subprocess
import platform
import os
from colorama import init
from termcolor import colored
import keyring
from datetime import datetime
import sys

expiry_date = datetime(2026, 8, 31)  # Set your expiry date here

if datetime.now() > expiry_date:
    print("This version has expired. Please contact the owner for the updated version.")
    sys.exit(1)

# Initialize colorama for Windows support
init(autoreset=True)

# ===================== Identification Header =====================
SCRIPT_VERSION = "5.9.7"
DEVELOPER_INFO = "Developed by: TCS - Network Team (Ramidul)"
ENVIRONMENT_INFO = "Designed for: ASDA NewCo Environment"
ENVIRONMENT_INFO1 = "Copyright © 2025 TCS-Network Team. All Rights Reserved." 
ENVIRONMENT_INFO2 = "Unauthorized distribution or modification is prohibited."

def clear_screen():
    """Clear terminal before re-printing the banner."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    border = colored("-" * 70, "white", attrs=["bold"])
    top_border = colored("*" * 70, "cyan", attrs=["bold"])
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    print("\n" + top_border)
    print(colored(f"SSHConnect+ - v{SCRIPT_VERSION}", "cyan", attrs=["bold"]))
    print(border)
    print(colored(DEVELOPER_INFO, "yellow"))
    print(colored(ENVIRONMENT_INFO, "green"))
    print(colored(ENVIRONMENT_INFO1, "green"))
    print(colored(ENVIRONMENT_INFO2, "red", attrs=["bold"]))
    print(border + "\n")
    print(colored(f"Session started: {timestamp}", "magenta"))
    print(top_border + "\n")

# ===================== Keyring-Based Credentials =====================
def get_or_prompt_credentials(service_name):
    username = os.getenv("SSH_USERNAME") or keyring.get_password(service_name, "username")
    if not username:
        username = input("Enter SSH username: ")
        keyring.set_password(service_name, "username", username)
    return username

SERVICE_NAME = "asda_ssh"
SSH_USERNAME = get_or_prompt_credentials(SERVICE_NAME)

# ===================== PuTTY Path =====================
PUTTY_PATH = "C:\\Program Files\\PuTTY\\putty.exe"

# ===================== Predefined Host Mappings =====================
UKRED_HOSTS = {
    "R1A.UKRED.asda.uk": "10.0.8.146",
    "R1B.UKRED.asda.uk": "10.0.8.147",
    "R2A.UKRED.asda.uk": "10.0.6.81",
    "R3A.UKRED.asda.uk": "10.0.6.82",
    "S1A.UKRED.asda.uk": "10.0.8.148",
    "S1B.UKRED.asda.uk": "10.0.8.149",
    "S2A.UKRED.asda.uk": "10.0.8.150",
    "S2B.UKRED.asda.uk": "10.0.8.151",
    "S3A.UKRED.asda.uk": "10.13.6.130",
    "R1A.OOB.UKRED.asda.uk": "10.0.6.0",
    "S1A.OOB.UKRED.asda.uk": "10.0.6.68"
}

UKSLO_HOSTS = {
    "R1A.UKSLO.asda.uk": "10.0.8.140",
    "R1B.UKSLO.asda.uk": "10.0.8.141",
    "R2A.UKSLO.asda.uk": "10.0.4.81",
    "R3A.UKSLO.asda.uk": "10.0.4.82",
    "S1A.UKSLO.asda.uk": "10.0.8.142",
    "S1B.UKSLO.asda.uk": "10.0.8.143",
    "S2A.UKSLO.asda.uk": "10.0.8.144",
    "S2B.UKSLO.asda.uk": "10.0.8.145",
    "S3A.UKSLO.asda.uk": "10.12.6.130",
    "R1A.OOB.UKSLO.asda.uk": "10.0.4.0",
    "S1A.OOB.UKSLO.asda.uk": "10.0.4.68"
}

# ===================== Functions =====================
def ping_host(host):
    try:
        os_type = platform.system().lower()
        args = ["ping", "-n", "1", "-w", "1000", host] if os_type == "windows" else ["ping", "-c", "1", "-W", "1", host]
        response = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return response.returncode == 0
    except FileNotFoundError:
        print(colored("[ERROR] Ping command not found. Ensure ping is installed.", "red"))
        return False
    except Exception as e:
        print(colored(f"[ERROR] Error pinging {host}: {e}", "red"))
        return False

def launch_putty(host_ip):
    if not os.path.exists(PUTTY_PATH):
        print(colored("[ERROR] PuTTY is not installed or the path is incorrect!", "red"))
        return
    try:
        subprocess.Popen([PUTTY_PATH, "-ssh", f"{SSH_USERNAME}@{host_ip}"])
        
    except Exception as e:
        print(colored(f"[ERROR] Failed to launch PuTTY: {e}", "red"))

def process_site_info(site_name):
    reachable_hosts = []

    if site_name.lower().startswith("ukred"):
        host_list = UKRED_HOSTS
        site_label = "UKRED"
    elif site_name.lower().startswith("ukslo"):
        host_list = UKSLO_HOSTS
        site_label = "UKSLO"
    else:
        host_list = None
        site_label = None

    if host_list:        
        for host, ip in host_list.items():
            if ping_host(ip):
                reachable_hosts.append((host, ip))
        if reachable_hosts:
            print(colored(f"\n✔ Site: {site_name} is available in the NewCo environment!", "yellow"))
            print(colored("\n► BELOW ARE THE NETWORK DEVICES THAT ARE REACHABLE: ", "cyan"))
            print()
            for idx, (host, _) in enumerate(reachable_hosts, start=1):
                print(colored(f"{idx}. {host}", "green"))
        else:
            print(colored(f"\n✘ Site: {site_name} is not available in the NewCo environment!", "red"))
            print()
            print(colored("Please try a different site no..", "cyan"))
    else:
        site_code = f"s0{site_name}"

        if site_name.startswith("7"):
           site_code = f"d0{site_name}"
         # For sites starting with "7", use only these hosts
           router_hosts = [
            f"ra.{site_code}.asda.uk",
            f"rb.{site_code}.asda.uk",
            f"rcorea.{site_code}.asda.uk",
            f"rcoreb.{site_code}.asda.uk"
            f"sacc1.{site_code}.asda.uk",
            f"sacc2.{site_code}.asda.uk",
            f"ssrvacc1.{site_code}.asda.uk",
            f"ssrvacc2.{site_code}.asda.uk",
            f"ssrvacc1-1.{site_code}.asda.uk",
            f"ssrvacc1-2.{site_code}.asda.uk",
            f"ssrvacca.{site_code}.asda.uk",
            f"ssrvaccb.{site_code}.asda.uk",
            f"stca01.{site_code}.asda.uk",
            f"stcb01.{site_code}.asda.uk",
            f"stcc01.{site_code}.asda.uk",
            f"stcd01.{site_code}.asda.uk",
            f"stce01.{site_code}.asda.uk",
            f"stcf01.{site_code}.asda.uk",
            f"stcg01.{site_code}.asda.uk",
            f"stch01.{site_code}.asda.uk",
            f"stci01.{site_code}.asda.uk",
            f"stcj01.{site_code}.asda.uk",
            f"stck01.{site_code}.asda.uk",
            f"stcl01.{site_code}.asda.uk",
            f"stcm01.{site_code}.asda.uk",
            f"stcn01.{site_code}.asda.uk",
            f"stco01.{site_code}.asda.uk",
            f"stcp01.{site_code}.asda.uk",
            f"stcq01.{site_code}.asda.uk",
            f"stcr01.{site_code}.asda.uk",
            f"stcs01.{site_code}.asda.uk",
            f"stct01.{site_code}.asda.uk",
            f"stcu01.{site_code}.asda.uk",
            f"stcv01.{site_code}.asda.uk",
            f"stcw01.{site_code}.asda.uk",
            f"stcx01.{site_code}.asda.uk",
            f"stcy01.{site_code}.asda.uk",
            f"stcz01.{site_code}.asda.uk"

         ]
        else:
        # Normal hosts for all other sites
          router_hosts = [
            f"ra.{site_code}.asda.uk",
            f"rb.{site_code}.asda.uk",
            f"supc1.{site_code}.asda.uk",
            f"sgrc1.{site_code}.asda.uk",
            f"sgrc2.{site_code}.asda.uk",
            f"sgm1.{site_code}.asda.uk",
            f"sgm2.{site_code}.asda.uk",
            f"shs1.{site_code}.asda.uk",
            f"shs2.{site_code}.asda.uk",
            f"shoarea1.{site_code}.asda.uk",
            f"shoarea2.{site_code}.asda.uk"
        ]

        from concurrent.futures import ThreadPoolExecutor

        reachable_hosts = []

        def ping_wrapper(host):
            return host if ping_host(host) else None

        # Run pings concurrently, max 30 at a time
        with ThreadPoolExecutor(max_workers=30) as executor:
            results = list(executor.map(ping_wrapper, router_hosts))

        # Preserve original host order
        for host, result in zip(router_hosts, results):
            if result:
                reachable_hosts.append((host, None))              

        if reachable_hosts:
            print(colored(f"\n✔ Site: {site_name} is available in the NewCo environment!", "yellow"))
            print(colored("\n► BELOW ARE THE NETWORK DEVICES THAT ARE REACHABLE : ", "cyan"))
            print()
            for idx, (host, _) in enumerate(reachable_hosts, start=1):
                print(colored(f"{idx}. {host}", "green"))
        else:
            print(colored(f"\n✘ Site: {site_name} is not available in the NewCo environment!", "red"))
            print(colored("\nPlease try a different site no..", "cyan"))
            input(colored("\nPress Enter to continue...", "yellow"))

    if reachable_hosts:
        while True:
            option = input(colored("\nEnter the option number (like 1,2,3..) to connect to a device, 'm' to go back to MAIN MENU, or 'q' to QUIT: ", "yellow")).strip()
            if not option:
                print(colored("Skipping connection.", "cyan"))
                break
            elif option.isdigit() and 1 <= int(option) <= len(reachable_hosts):
                selected_host, selected_ip = reachable_hosts[int(option) - 1]
                launch_putty(selected_ip if selected_ip else selected_host)
            elif option.lower() == 'm':
                print(colored("Returning to the main menu.", "cyan"))
                return True
            elif option.lower() == 'q':
                print(colored("Exiting program.", "cyan"))
                exit()
            else:
                print(colored("[ERROR] Invalid option. Please enter a valid number, 'm' for main menu, or 'q' to quit.", "red"))

def get_site_name():
    while True:
        site_name = input(
f"\nEnter the {colored('Site no.','green')} / {colored('UKSLO','green')} / {colored('UKRED','green')} (or '{colored('q','red')}' to quit) {colored('(case-insensitive)','yellow')}: "
).strip()
        if site_name.lower() == 'q':
            print(colored("Exiting program.", "cyan"))
            exit()
        elif site_name:
            return site_name
        print(colored("[ERROR] Please enter a valid site no.", "red"))

if __name__ == "__main__":
    while True:
        clear_screen()
        print_banner()
        site_name = get_site_name()
        process_site_info(site_name)
