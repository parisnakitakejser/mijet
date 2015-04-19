import sys
import imaplib
import email
import os
import imghdr

class build:
    mailFolder = "INBOX"
    mailFolderCopyTo = "INOBX/Parsed"
    localPath = "./tmp"
    mailFrom = ""
    
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
            print self.mailbox.select(self.mailFolder)
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
    def __getAllLoop(self):
        
        rv, data = self.mailbox.search(None, 'ALL', '(HEADER FROM "'+ self.mailFrom +'")')
        
        if rv != 'OK':
            print("No messages found!")
        
        mailCount = data[0].split()
        print "Mail back to handle: "+ str( len(mailCount) )
        
        if ( len(mailCount) > 0):
            num = mailCount[0]
            
            print "Mail listID: "+ num
            rv, data = self.mailbox.fetch(num, '(RFC822)')
            print(rv)
            
            email_body = data[0][1]
            mail = email.message_from_string(email_body)
            
            print "["+ str(mail["From"]) +"] :" + str(mail["Subject"])
            
            self.__saveAttachedFiles(mail)
            self.__moveMailToParsedFolder(num)
            self.__getAllLoop()
    
    """
    Get all mailbox messegt 
    """
    def run(self):
        
        self.__login()
        self.__getAllLoop()
        self.__close()

    """
    Save all attached files from mails
    """
    def __saveAttachedFiles(self,mail):
        
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
        
            if part.get('Content-Disposition') is None:
                continue
    
            filename = part.get_filename()
            counter = 1

            if filename:
                att_path = os.path.join(self.localPath, str(mail['Message-ID']) +"_"+ filename )

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    """
    Move mail messegt to parsed folder after its handle
    """
    def __moveMailToParsedFolder(self,num):
        
        mail_uid = num
        
        apply_lbl_msg = self.mailbox.copy(mail_uid, self.mailFolderCopyTo)
        print apply_lbl_msg
        
        if apply_lbl_msg[0] == 'OK':
            self.mailbox.store(mail_uid, '+FLAGS', '\\Deleted')
            self.mailbox.expunge()