from fs.osfs import OSFS
from fs.ftpfs import FTPFS
import getpass

#Temporary CLI Input
username = input('Username:')
password = getpass.getpass('Password: ')
port = int(input('Port:'))
host = input('Host: ')

#Initialize FTP File System
ftp_fs = FTPFS(host, user=username, passwd=password, port=port)
print(ftp_fs.listdir('/'))

#Initialize OS File System

#Moves Current World To Backup

#Closes File Systems
ftp_fs.close()
