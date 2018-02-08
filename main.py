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
    if not settings[2]:
        print('ERROR: User has not read and agreed to risks with using this software. Please run settings.py')
        sys.exit(1)
    ftp_settings, os_settings = settings[0], settings[1]
    ftp_fs = initialize_ftp(ftp_settings[0], ftp_settings[1], ftp_settings[2], ftp_settings[3])
    os_fs = initialize_os(os_settings)
    return (ftp_fs, os_fs)


#Initialize FTP File System
def initialize_ftp(username, password, host, port):
    ftp_fs = FTPFS(host, user=username, passwd=password, port=port)
    return ftp_fs

#Initialize OS File System
def initialize_os(directory):
    os_fs = OSFS(directory)
    return os_fs

def close_sessions(sessions):
    for session in sessions:
        session.close()

#Moves Current World To Backup

#Closes File Systems
#ftp_fs.close()

if __name__ == '__main__':
    session_data = initialize_data()
    print(session_data[0].listdir('/'))
    print(session_data[1].listdir('/'))
    close_sessions(session_data)