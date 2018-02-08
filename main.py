from fs.osfs import OSFS
from fs.ftpfs import FTPFS
from settings import open_settings
import getpass
import shelve
import os.path
import sys

def config_exists():
    extentions = ['bak', 'dat', 'dir']
    for extention in extentions:
        if not os.path.exists('settings/settings.config.' + extention):
            return False
    return True

def get_config():
    if config_exists():
        return open_settings()
    else:
        raise FileNotFoundError

def initialize_data():
    try:
        settings = get_config()
    except FileNotFoundError as Error:
        print('ERROR: settings.config not found in settings folder. Please run settings.py')
        sys.exit(1)

if __name__ == '__main__':
    initialize_data()

#Initialize FTP File System
#ftp_fs = FTPFS(host, user=username, passwd=password, port=port)
#print(ftp_fs.listdir('/'))

#Initialize OS File System

#Moves Current World To Backup

#Closes File Systems
#ftp_fs.close()