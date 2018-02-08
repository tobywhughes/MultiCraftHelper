#MANAGES FILE_SYSTEM DATA
import getpass
import shelve

def prompt_user_ftp():
    """Returns tuple containing username, password, host, and port in that order"""
    username = input('Please Enter FTP Username:')
    password = getpass.getpass('Please Enter FTP Password: ')
    host = input('Please Enter Host Address: ')
    port = int(input('Please Enter Port:'))
    return (username, password, host, port)

def prompt_user_os():
    pass

def save_file(ftp_settings):
    shelf_file = shelve.open('settings.config')
    shelf_file['ftp_settings'] = ftp_settings
    shelf_file.close()

def open_settings():
    shelf_file = shelve.open('settings.config')
    ftp_settings = shelf_file['ftp_settings']
    shelf_file.close()
    return (ftp_settings)

if __name__ == '__main__':
    ftp_settings = prompt_user_ftp()
    save_file(ftp_settings)
    settings = open_settings()
    print(settings)