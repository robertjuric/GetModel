from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
import sys
import csv
import re

#Open CSV Files
print ("Opening files...")
with open ('shortinventory.csv', 'r') as inf, open('UpdatedInventory.csv', 'w') as outf:
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
			model_info = "SSH error"
			continue
		model_output = net_connect.send_command("show version | i bytes of")
		model_detail = re.split(' ', model_output)
		if model_output:
			model_info = model_detail[1]
			print(model_info)
			#If needed, strip leading space
			#model_info = model_detail[1].lstrip(' ')
			if len(model_info) == 0:
				#print("blank")
				#test Nexus 9k:
				nexus_output = net_connect.send_command("show hardware | i Model")
				if nexus_output:
					nexus_detail = re.split(' ', nexus_output)
					model_info = nexus_detail[5].rstrip('\n')
					print(model_info)
		else:
			print("oops")
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

