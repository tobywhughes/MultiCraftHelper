from fs.osfs import OSFS
from fs.ftpfs import FTPFS
from settings import open_settings
import getpass
import shelve
import os.path
import sys

def config_exists():
    """Reads for all 3 extentions associated with shelve file. Returns True if the exist and False if at least one is not found"""
    extentions = ['bak', 'dat', 'dir']

    for extention in extentions:
        if not os.path.exists('settings/settings.config.' + extention):
            return False
    return True

def get_config():
    """Gets config settings from ./settings/settings.config and returns them"""
    if config_exists():
        return open_settings()
    else:
        raise FileNotFoundError

def initialize_data():
    """Initializes FTP and OS Filesystems and returns filesystem instances in tuple with ftp and os in that order"""
    try:
        settings = get_config()
    except FileNotFoundError as Error:
        print('ERROR: settings.config not found in settings folder. Please run settings.py')
        sys.exit(1)

    # Checks for required user agreement. This user agreement details security risks associated with this program,
    # so this program will not continue without confirmation that the user has read and agreed to said risks.
    if not settings[2]:
        print('ERROR: User has not read and agreed to risks with using this software. Please run settings.py')
        sys.exit(1)

    #initializes filesystems
    ftp_settings, os_settings = settings[0], settings[1]
    ftp_fs = initialize_ftp(ftp_settings[0], ftp_settings[1], ftp_settings[2], ftp_settings[3])
    os_fs = initialize_os(os_settings)

    return (ftp_fs, os_fs)


def initialize_ftp(username, password, host, port):
    """Initializes FTP filesystem and returns associated instance"""
    ftp_fs = FTPFS(host, user=username, passwd=password, port=port)
    return ftp_fs

def initialize_os(directory):
    """Initializes OS filesystem and returns associated instance"""
    os_fs = OSFS(directory)
    return os_fs

def close_sessions(sessions):
    """Closes sessions to all opened filesystems"""
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