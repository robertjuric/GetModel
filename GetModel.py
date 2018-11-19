from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
import sys
import csv
import re

#Open CSV Files
print ("Opening files...")
with open ('Inventory.csv', 'r') as inf, open('UpdatedInventory.csv', 'w') as outf:
	reader = csv.DictReader(inf)

	#Add new column to end of updated CSV
	new_fieldnames = reader.fieldnames + ['Model'] + ['LiveVersion']

	writer = csv.DictWriter(outf, new_fieldnames)
	writer.writeheader()
	
	#Loop through each row in the original CSV
	for row in reader:
		#Create variable for data in the column with header 'IP Address'
		this_ip = row['IP Address']
		print('Connecting to:', this_ip)
		#Try to connect to device, catch errors
		try:
			net_connect = ConnectHandler(device_type='cisco_ios', ip=this_ip, username='admin', password='pw')
		except SSHException:
			print('SSH error')
			continue
		#Works but returns empty on IOS-XE
		#model_output = net_connect.send_command("show version | i Model number")
		#Works better across multiple platforms, but is still missing:
		#show version | i Model Number appears to work on IOS-XE
		#"show version | i bytes of" to get similar out, some devices say 'bytes of physical memory'
		model_output = net_connect.send_command("show version | i bytes of")
		model_detail = re.split(' ', model_output)
		if model_output:
			#print(model_detail[1])
			model_info = model_detail[1]
			#strip leading space when splitting "show version | i Model number"
			#model_info = model_detail[1].lstrip(' ')
		else:
			model_info = "empty"
		"""
		version_output = net_connect.send_command("show version | i Software")	
		version_detail = re.split(',', version_output)
		
		if version_output:
			print(version_detail[2])
			version_info = version_detail[2].lstrip(' ')
		else:
			version_info = "empty"
		"""
		net_connect.disconnect()
		print("Writing row")
		writer.writerow(dict(row,Model=model_info))
		# If using the version_output:
		#writer.writerow(dict(row,Model=model_info, LiveVersion=version_info))

