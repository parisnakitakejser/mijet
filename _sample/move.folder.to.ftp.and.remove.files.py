import mijet.server.ftp
import mijet.system.file
import datetime

current_date_format = datetime.date.today().strftime("%Y/%m/%d")
xml_invoice_path = 'tmp/'

ftp_host = '{host}'
ftp_username = '{username}'
ftp_password = '{password}'

ftp = mijet.server.ftp.FTP(ftp_host,ftp_username,ftp_password)
ftp.passiv_mode = True
ftp.folder_root = '/test-folder/'

ftp.connect()
ftp.create_folder(current_date_format)
ftp.upload_all_files_from_folder(xml_invoice_path,current_date_format)
ftp.close()

file = mijet.system.file.File()
file.remove_all_files_in_folder(xml_invoice_path)