from fs.osfs import OSFS
from fs.ftpfs import FTPFS
from fs.copy import copy_file_if_newer
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
    """Initializes FTP and OS Filesystems and returns filesystem instances in tuple along with the world name"""
    try:
        settings = get_config()
    except FileNotFoundError:
        print('ERROR: settings.config not found in settings folder. Please run settings.py')
        sys.exit(1)

    # Checks for required user agreement. This user agreement details security risks associated with this program,
    # so this program will not continue without confirmation that the user has read and agreed to said risks.
    if not settings[2]:
        print('ERROR: User has not read and agreed to risks with using this software. Please run settings.py')
        sys.exit(1)

    #initializes filesystems
    ftp_settings, os_settings = settings[0], settings[1]
    world_name = ftp_settings[4]
    ftp_fs = initialize_ftp(ftp_settings[0], ftp_settings[1], ftp_settings[2], ftp_settings[3])
    os_fs = initialize_os(os_settings)

    return (ftp_fs, os_fs, world_name)


def initialize_ftp(username, password, host, port):
    """Initializes FTP filesystem and returns associated instance"""
    ftp_fs = FTPFS(host, user=username, passwd=password, port=port)
    return ftp_fs

def initialize_os(directory):
    """Initializes OS filesystem and returns associated instance"""
    os_fs = OSFS(directory)
    return os_fs

def copy_world(ftp_fs, os_fs, world_name):
    """Copies backup from FTP server onto OS"""
    world_name = world_name + '.zip'

    if world_name in ftp_fs.listdir('/'):
        try:
            new_copy = copy_file_if_newer(ftp_fs, world_name, os_fs, world_name)
        except:
            print('ERROR: File exists but there was an error when copying file to OS')
            close_sessions([ftp_fs, os_fs])
            sys.exit(1)

        if new_copy:
            print('Copied', world_name, 'from FTP server to OS.')
        else:
            print('Already have latest file. Nothing copied.')     
    else:
        print('ERROR: File not found.', world_name, 'must exist in your FTP directory.')
        close_sessions([ftp_fs, os_fs])
        sys.exit(1)

def close_sessions(sessions):
    """Closes sessions to all opened filesystems"""
    for session in sessions:
        session.close()

if __name__ == '__main__':
    session_data = initialize_data()
    copy_world(session_data[0], session_data[1], session_data[2])
    close_sessions(session_data[:-1])