from netmiko import ConnectHandler
import sys
import csv
import re

#Open CSV Files
print ("Opening files...")
with open ('Inventory.csv', 'r') as inf, open('UpdatedInventory.csv', 'w') as outf:
	reader = csv.DictReader(inf)

	#Add new column to updated CSV
	new_fieldnames = reader.fieldnames + ['Model']

	writer = csv.DictWriter(outf, new_fieldnames)
	writer.writeheader()
	
	#Loop through each row in the original CSV
	for row in reader:
		this_ip = row['IP Address']
		print('Connecting to:', this_ip)
		net_connect = ConnectHandler(device_type='cisco_ios', ip=this_ip, username='admin', password='nowayjose')
		model_output = net_connect.send_command("show version | i Model number")
		model_detail = re.split('[:]', model_output)
		model_info = model_detail[1].lstrip(' ')
		print(model_info)
		print("Writing row")
		writer.writerow(dict(row,Model=model_info))

