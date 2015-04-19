import sys
import imaplib
import email
import os
import imghdr

class Build:
    mail_folder = "INBOX"
    mail_folder_copy_to = "INOBX/Parsed"
    local_path = "./tmp"
    mail_from = ""
    
    """
    Defined server, username and password 
    """
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
    
    """
    Connect to your IMAP mailbox 
    """
    def __login(self):
        try:
            self.mailbox = imaplib.IMAP4(self.server)
            self.mailbox.login(self.username, self.password)
            print self.mailbox.select(self.mail_folder)
            print "-"
        
        except imaplib.IMAP4.error:
            print "LOGIN FAILED!!! "
    
    """ 
    Close connection to your IMAP mailbox 
    """
    def __close(self):
        self.mailbox.close()
        self.mailbox.logout()
    
    """ 
    Get all mailbox loop and handle every mails there are back
    """
    def __get_all_loop(self):
        
        rv, data = self.mailbox.search(None, 'ALL', '(HEADER FROM "%s")' % self.mail_from )
        
        if rv != 'OK':
            print("No messages found!")
        
        mail_count = data[0].split()
        print "Mail back to handle: "+ str( len(mail_count) )
        
        if ( len(mail_count) > 0):
            num = mail_count[0]
            
            print "Mail listID: "+ num
            rv, data = self.mailbox.fetch(num, '(RFC822)')
            print(rv)
            
            email_body = data[0][1]
            mail = email.message_from_string(email_body)
            
            print "["+ str(mail["From"]) +"] :" + str(mail["Subject"])
            
            self.__save_attached_files(mail)
            self.__move_mail_to_parsed_folder(num)
            self.__get_all_loop()
    
    """
    Get all mailbox messegt 
    """
    def run(self):
        
        self.__login()
        self.__get_all_loop()
        self.__close()

    """
    Save all attached files from mails
    """
    def __save_attached_files(self,mail):
        
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
        
            if part.get('Content-Disposition') is None:
                continue
    
            filename = part.get_filename()
            counter = 1

            if filename:
                att_path = os.path.join(self.local_path, str(mail['Message-ID']) +"_"+ filename )

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    """
    Move mail messegt to parsed folder after its handle
    """
    def __move_mail_to_parsed_folder(self,num):
        
        mail_uid = num
        
        apply_lbl_msg = self.mailbox.copy(mail_uid, self.mail_folder_copy_to)
        print apply_lbl_msg
        
        if apply_lbl_msg[0] == 'OK':
            self.mailbox.store(mail_uid, '+FLAGS', '\\Deleted')
            self.mailbox.expunge()