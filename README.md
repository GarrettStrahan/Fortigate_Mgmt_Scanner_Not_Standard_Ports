# Fortigate_Mgmt_Scanner_Not_Standard_Ports
If you want to scan your network environment for mgmt port for example fortigate or fortimanager and include with ability to use non-standard port numbers
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
