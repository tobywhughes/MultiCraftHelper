#MANAGES FILE_SYSTEM DATA
import getpass
import shelve
import colorama
import os

def security_agreement():
    agreement_text = (colorama.Fore.YELLOW + colorama.Back.RED +
                'This program recieves backups from the MultiCraft servers over an FTP connection. FTP is UNSECURE and UNENCRPYTED. '
                'It is vulnerable to man-in-the-middle attacks and password sniffing attacks.\nAgreeing to use this software means that '
                'you are accepting this risk. DO NOT use this software if you are unwilling to put your files at risk. Do not use a '
                'password associated with any other accounts you have.\nIf you still desire to use this software despite the associated '
                'risks type YES (case-sensitive) to agree. Type NO to exit software. Otherwise, you will not be able to use this software.\n'
                + colorama.Style.RESET_ALL + 'Please enter confirmation: ')
    while True:
        agreement_string = input(agreement_text)
        if agreement_string == 'YES':
            return True
        elif agreement_string == 'NO':
            return False
        

def prompt_user_ftp():
    """Returns tuple containing username, password, host, and port in that order"""
    username = input('Please Enter FTP Username:')
    password = getpass.getpass('Please Enter FTP Password: ')
    host = input('Please Enter Host Address: ')
    port = int(input('Please Enter Port:'))
    return (username, password, host, port)

def prompt_user_os():
    while True:
        path = input('Please Enter Desired Path. Enter nothing for default location (./backups): ')
        if path == '':
            return os.path.abspath('./') + '/backups'
        else:
            if os.path.exists(path):
                return path
            else:
                print('Path not found.')
                continue
            

def save_file(ftp_settings, os_settings, agreement):
    if os_settings == os.path.abspath('./') + '/backups':
        os.makedirs('./backups', exist_ok=True)
    os.makedirs('./settings', exist_ok=True)
    shelf_file = shelve.open('settings/settings.config')
    shelf_file['ftp_settings'] = ftp_settings
    shelf_file['os_settings'] = os_settings
    shelf_file['agreement'] = agreement
    shelf_file.close()

def open_settings():
    shelf_file = shelve.open('settings/settings.config')
    ftp_settings = shelf_file['ftp_settings']
    os_settings = shelf_file['os_settings']
    agreement = shelf_file['agreement']
    shelf_file.close()
    return (ftp_settings, os_settings, agreement)

if __name__ == '__main__':
    colorama.init()
    agreement = security_agreement()
    if agreement:
        ftp_settings = prompt_user_ftp()
        os_settings = prompt_user_os()
        save_file(ftp_settings, os_settings, agreement)