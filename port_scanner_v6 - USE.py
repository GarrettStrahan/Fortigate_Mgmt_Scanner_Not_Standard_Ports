#Programmed by Garrett Strahan, using python 3.12
#Version 1 proved it did indeed work and outputted ALL the closed and open ports.
#Version 2 add multiple core processing.
#Version 3 add time elapse calualations and creates spreadsheets
#version 4 Instead of one line per port and lines for the same IPv4 addresses it is now 1 line per each IPv4 and many ports open/closed status.
#Version 5 This version will have support for .xslx spreadsheet files and using the API Pandas, NOT IMPLEMENTED AS OF YET!
#Version 5.2 This version re-introduces multi-core / multi-threading processing
#Version 6 Same as above but this version will have support for automation for sending the files with an email to my email account


#:
# This python program which takes in a text document called allips.txt with each line having a different IP address and put that text document into a list called all_fgt_ips. It to scans these IPs with the list all_fgt_ips for open TCP ssh ports for 22, 422, 822, and 922, if the TCP port is open create a text document called open_ssh_ports.txt and append all IP address and which SSH TCP ports are open. If the SSH TCP ports are closed append all the IP addresses and which SSH TCP are closed into the text document called closed_ssh_ports.txt
# It then searchs again with the all_fgt_ips list to search all the open fortigate mgmt open TCP ports and search for for these TCP port numbers of 80, 443, 4443, 8443, 9443, 10443. If the fortigate mgmt open TCP ports are opened then create a document called fgt_mgmt_opened_ports.txt and append with the IP addresses and the fortigate mgmt ports that are open. **If the fortigate mgmt TCP ports are open create a text file is called for fgt_mgmt_closed_ports.txt and append all IP addresses and the TCP ports that are closed.
# Search for port 541 which is for Fortigate to fortimanager management. It will append all the results for the closed ports for port 541. 
# The program creates the following spreadsheet files:
# open_ssh_ports.xlsx
# closed_ssh_ports.xlsx
# fgt_mgmt_opened_ports.xlsx
# fgt_mgmt_closed_ports.xlsx
# fgm_mgmt_open_ports.xlsx
# fgm_mgmt_closed_ports.xlsx
#
# It will also use the python program to use the  Pandas API to give spreadsheet files and spreadsheet data.
# The spreadsheet files to have, First column with "IPv4", the second column with "TCP Port #s"
#
# The spreadsheet data about the open SSH ports involving port numbers 22, 422, 822, 922 to put in file: open_ssh_ports.xlsx
# The spreadsheet data  about the closed SSH ports involving port numbers 22, 422, 822, 922 to put in file: closed_ssh_ports.xlsx
# The spreadsheet data about the open fortigate management ports involving port numbers 80, 443, 4443, 8443, 9443, 10443 to put in file: fgt_mgmt_opened_ports.xlsx
# The spreadsheet data about the closed fortigate managementclosed_ports involving port numbers 80, 443, 4443, 8443, 9443, 10443 to put in file: fgt_mgmt_closed_ports.xlsx
# The spreadsheet data about the open fortimanager ports involving port numbers 541 to put in file: fgm_mgmt_open_ports.xlsx
# The spreadsheet data about the closed fortimanager ports involving port numbers 541 to put in file: fgm_mgmt_closed_ports.xlsx
#

#Requirements:
# You’ll need pandas and openpyxl installed (pip install pandas openpyxl) to write Excel files. I removed the unused import openpyxl from your code since Pandas handles it internally via to_excel.
#
# How to Use:
# Ensure allips.txt is in the same directory with one IP per line.
# Run the script. It will:
# Scan ports and write to text files (one line per IP with multiple ports).
# Generate six Excel files with "IPv4" and "TCP Port #s" columns.
# Print start and end timestamps.


import socket
import os
import datetime as dt
import pytz
import pandas as pd
from datetime import datetime
import pytz
import time
from concurrent.futures import ThreadPoolExecutor

#new below
def main():
    print('function main() is being run now')
    #all_fgt_ips = read_ip_list("allips.txt") #This needs to be removed
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(scan_ports())
#end of new above

def make_est_timestamp() -> str:
    """
    Generates a friendly string for the start date and end date of the program
    in EST time zone.
    :return: Date/Time string.
    """
    est_tz = pytz.timezone("America/New_York")  # EST/EDT timezone
    current_time = dt.datetime.now(est_tz)  # Get current time in EST
    return f"TZID=America/New_York:{current_time.strftime('Date %m-%d-%Y Military Time %H:%M:%S / 12H %I:%M:%S %p EST')}"


now = datetime.now()

time_info = now.strftime("%B %d,%I:%M%p")
print(f"Port Scanner program v6 has started at {now}, using now")
print(f"Port Scanner program v6 has started at {make_est_timestamp()}")
start_time = datetime.now()

# Read IP addresses from allips.txt into a list
def read_ip_list(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []


# Function to check if a port is open
def check_port(ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0  # Returns True if port is open
    except:
        sock.close()
        return False


# Main scanning function
def scan_ports():
    # List of IPs from file
    all_fgt_ips = read_ip_list('allips.txt')
    if not all_fgt_ips:
        return

    # Define port lists
    ssh_ports = [22, 422, 822, 922]
    fgt_mgmt_ports = [80, 443, 4443, 8443, 9443, 10443]
    fgm_port = [541]  # FortiManager port as a list

    # Clear previous text files if they exist
    files_to_clear = [
        'open_ssh_ports.txt', 'closed_ssh_ports.txt',
        'fgt_mgmt_opened_ports.txt', 'fgt_mgmt_closed_ports.txt',
        'fgm_mgmt_open_ports.txt', 'fgm_mgmt_closed_ports.txt'
    ]
    for file in files_to_clear:
        if os.path.exists(file):
            os.remove(file)

    # Dictionaries to store results per IP
    ssh_open = {}
    ssh_closed = {}
    mgmt_open = {}
    mgmt_closed = {}
    fgm_open = {}
    fgm_closed = {}

    # Lists to store data for Excel files
    ssh_open_data = []
    ssh_closed_data = []
    mgmt_open_data = []
    mgmt_closed_data = []
    fgm_open_data = []
    fgm_closed_data = []

    # Scan each IP
    for ip in all_fgt_ips:
        print(f"Scanning IP: {ip}")

        # Initialize lists for this IP
        ssh_open[ip] = []
        ssh_closed[ip] = []
        mgmt_open[ip] = []
        mgmt_closed[ip] = []
        fgm_open[ip] = []
        fgm_closed[ip] = []

        # Scan SSH ports
        for port in ssh_ports:
            if check_port(ip, port):
                ssh_open[ip].append(port)
            else:
                ssh_closed[ip].append(port)

        # Scan FortiGate management ports
        for port in fgt_mgmt_ports:
            if check_port(ip, port):
                mgmt_open[ip].append(port)
            else:
                mgmt_closed[ip].append(port)

        # Scan FortiManager port
        for port in fgm_port:
            if check_port(ip, port):
                fgm_open[ip].append(port)
            else:
                fgm_closed[ip].append(port)

    # Write results to text files and prepare Excel data (one line per IP)
    for ip in all_fgt_ips:
        # SSH open ports
        if ssh_open[ip]:
            with open('open_ssh_ports.txt', 'a') as f:
                ports_str = ', '.join(map(str, ssh_open[ip]))
                f.write(f"IP: {ip} - Open SSH Ports: {ports_str}\n")
            ssh_open_data.append({"IPv4": ip, "TCP Port #s": ports_str})

        # SSH closed ports
        if ssh_closed[ip]:
            with open('closed_ssh_ports.txt', 'a') as f:
                ports_str = ', '.join(map(str, ssh_closed[ip]))
                f.write(f"IP: {ip} - Closed SSH Ports: {ports_str}\n")
            ssh_closed_data.append({"IPv4": ip, "TCP Port #s": ports_str})

        # FortiGate management open ports
        if mgmt_open[ip]:
            with open('fgt_mgmt_opened_ports.txt', 'a') as f:
                ports_str = ', '.join(map(str, mgmt_open[ip]))
                f.write(f"IP: {ip} - Open Mgmt Ports: {ports_str}\n")
            mgmt_open_data.append({"IPv4": ip, "TCP Port #s": ports_str})

        # FortiGate management closed ports
        if mgmt_closed[ip]:
            with open('fgt_mgmt_closed_ports.txt', 'a') as f:
                ports_str = ', '.join(map(str, mgmt_closed[ip]))
                f.write(f"IP: {ip} - Closed Mgmt Ports: {ports_str}\n")
            mgmt_closed_data.append({"IPv4": ip, "TCP Port #s": ports_str})

        # FortiManager open ports
        if fgm_open[ip]:
            with open('fgm_mgmt_open_ports.txt', 'a') as f:
                ports_str = ', '.join(map(str, fgm_open[ip]))
                f.write(f"IP: {ip} - Open FGM Port: {ports_str}\n")
            fgm_open_data.append({"IPv4": ip, "TCP Port #s": ports_str})

        # FortiManager closed ports
        if fgm_closed[ip]:
            with open('fgm_mgmt_closed_ports.txt', 'a') as f:
                ports_str = ', '.join(map(str, fgm_closed[ip]))
                f.write(f"IP: {ip} - Closed FGM Port: {ports_str}\n")
            fgm_closed_data.append({"IPv4": ip, "TCP Port #s": ports_str})

    # Create Excel files using Pandas
    pd.DataFrame(ssh_open_data).to_excel('open_ssh_ports.xlsx', index=False)
    pd.DataFrame(ssh_closed_data).to_excel('closed_ssh_ports.xlsx', index=False)
    pd.DataFrame(mgmt_open_data).to_excel('fgt_mgmt_opened_ports.xlsx', index=False)
    pd.DataFrame(mgmt_closed_data).to_excel('fgt_mgmt_closed_ports.xlsx', index=False)
    pd.DataFrame(fgm_open_data).to_excel('fgm_mgmt_open_ports.xlsx', index=False)
    pd.DataFrame(fgm_closed_data).to_excel('fgm_mgmt_closed_ports.xlsx', index=False)

    print("Scanning complete. Results written to text and Excel files.")


# Run the program
# if __name__ == "__main__":
#     scan_ports()

#NEW BELOW
if __name__ == "__main__":
    print("if __name__ == main is being run?")
    main()
#    scan_ports()
#END OF NEW ABOVE

print("Spreadsheet/TEXT file generation has been completed! Moving to emailing these files to the proper place.")

print("The Automation emailer section is starting") #lines of code here and below are for emailing the generated files as attached files.
import smtplib
import os
from email.message import EmailMessage

# Step 1: Generate the email.txt file
filename = ["closed_ssh_ports.txt", "closed_ssh_ports.xlsx", "fgm_mgmt_closed_ports.txt", "fgm_mgmt_closed_ports.xlsx", "fgm_mgmt_open_ports.txt", "fgm_mgmt_open_ports.xlsx", "fgt_mgmt_closed_ports.txt", "fgt_mgmt_closed_ports.xlsx", "fgt_mgmt_opened_ports.txt", "fgt_mgmt_opened_ports.xlsx", "open_ssh_ports.txt", "open_ssh_ports.xlsx"]
# with open(filename, "w") as file:
#     file.write("Generated from Python, to be emailed.")

# Step 2: Email credentials and recipient
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "EMAIL@gmail.com"  # Replace with your Gmail address
EMAIL_PASSWORD = "przm utbd prih ekbg" #Not real API password but example
TO_EMAIL = "EMAIL@HOTMAIL.com" #Replace with the email you want to email the files to
SUBJECT = "Automated Email with Attachment"

# Step 3: Create email message
msg = EmailMessage()
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg["Subject"] = SUBJECT
msg.set_content("Please find the attached file.")

# Step 4: Attach the file
#ORIGINAL FOR A STRING
# with open(filename, "rb") as f:
#     file_data = f.read()
#     msg.add_attachment(file_data, maintype="text", subtype="plain", filename=filename)

#NEW FOR A LIST
# for fname in filename:
#     with open(fname, "rb") as f:
#         file_data = f.read()
#         msg.add_attachment(file_data, maintype="text", subtype="plain", filename=fname)

for fname in filename:
    try:
        with open(fname, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="text", subtype="plain", filename=fname)
    except FileNotFoundError:
        print(f"Warning: {fname} not found. Skipping...")
#END NEW FOR A LIST



# Step 5: Send the email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
print("Sending files section has been completed.")
#END OF EMAILING SECTION OF CODE




end_time = datetime.now()

# Calculate the duration
elapsed_time = end_time - start_time

# Format and display results
print("Start Time:", start_time.strftime("%I:%M:%S %p"))
print("End Time:", end_time.strftime("%I:%M:%S %p"))
print("Elapsed Time:", elapsed_time)

make_est_timestamp()
print(f"Time_info = {time_info}")
print(f"Port Scanner program v6 has ended at {make_est_timestamp()}")