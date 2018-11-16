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
		net_connect = ConnectHandler(device_type='cisco_ios', ip=this_ip, username='admin', password='pw')
		#Works but returns empty on IOS-XE
		#model_output = net_connect.send_command("show version | i Model number")
		#Works better across multiple platforms, but is still missing:
		#show version | i Model Number appears to work on IOS-XE
		#"show version | i bytes of" to get similar out, some devices say 'bytes of physical memory'
		model_output = net_connect.send_command("show version | i bytes of memory")
		model_detail = re.split(' ', model_output)
		if model_output:
			print(model_detail[1])
			model_info = model_detail[1]
			#strip leading space when splitting "show version | i Model number"
			#model_info = model_detail[1].lstrip(' ')
		else:
			model_info = "empty"
		print("Writing row")
		writer.writerow(dict(row,Model=model_info))

