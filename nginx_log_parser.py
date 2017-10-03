import os
import re 

code_500 = []
nginx_log_list = []

def load_log_file(filepath):
	if not os.path.exists(filepath):
		return None
	else:
		with open(filepath,'r') as log_file:
			for line in log_file:
				nginx_log_list.append(line)	
		return nginx_log_list		

def log_parser_code_500(nginx_log):
	for line in nginx_log:
		if (line.find(" 500 ")!=-1):
			code_500.append(line)
	return code_500

def write_new_log(log_list):
	with open("log_code_500.txt",'w', encoding='utf-8') as log_500:
		for line in log_list:
			log_500.write(line)

def count_request(log_list):
	count_req = 0
	for line in log_list:
		if (line.find(" 200 ")!=-1 and (line.find("GET"))):
			count_req+=1
	return count_req

def count_ip(log_list):
	for line in log_list:
		#print (line)
		ip = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})',line)
		#ip = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

		#ip_count = line.count(ip)
	return ip

nginx_log = load_log_file("nginx.log")
log_code_500 = log_parser_code_500(nginx_log)
print (log_code_500)
write_new_log(log_code_500)

print (count_request(nginx_log))
print (count_ip(nginx_log))
