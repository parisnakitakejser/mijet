import ftplib
import os

class FTP:
    
    debug = "on"
    passiv_mode = False
    create_folder_if_not_exists = False
    folder_root = '/'
    
    __filelist = []
    
    """
    Debug messegt will be printet to terminal if debugLevel is on
    """
    def __debug(self,msg):
        if ( self.debug.lower() == "on" ):
            print msg

    """
    Return right folder name into filelist array
    """
    def __parse(self,line):
        if line[0] == 'd':
            self.__filelist.append( line.rpartition(' ')[2] )
    
    """
    Setup FTP settings before its connect to FTP server
    """
    def __init__(self,host,username,password):
        self.__host = host
        self.__username = username
        self.__password = password
        
        self.__debug("# FTP-Settings:")
        self.__debug("Username: %s" % self.__username )
        self.__debug("Password: %s" % self.__password )
        self.__debug("Trying to connect to: %s" % self.__host )

    """
    Connect to FTP server
    """
    def connect(self):
        try:
            self.__ftp = ftplib.FTP(self.__host)
            self.__debug( self.__ftp.login(self.__username,self.__password) )
            
            self.__debug("")
            self.__ftp.set_pasv(self.passiv_mode)
            
            self.__debug( "Passiv mode: %s " % self.passiv_mode )
            self.__debug("## FTP Settings complated ##")
            self.__debug("")
        
            self.go_to_folder( self.folder_root)
                
        except IOError:
            print ftplib.error_reply
    
    """
    Close connection to FTP server
    """
    def close(self):
        self.__debug( self.__ftp.quit() )
    
    """
    Change FTP folder
    """
    def go_to_folder(self, go_to_folder):
        self.__debug( self.__ftp.cwd( go_to_folder ) )

    """
    Upload all files from a folder to what path you need to uploaded to.
    """
    def upload_all_files_from_folder(self, from_folder_path, to_folder_path ):
        
        self.go_to_folder( self.folder_root + to_folder_path )
        self.__debug( "# Go to folder before uploading: %s" % self.folder_root + to_folder_path )
        for root, dirs, files in os.walk(from_folder_path):
            
            for fname in files:
                
                full_fname = os.path.join(root, fname)
                self.__ftp.storbinary('STOR '+ fname, open(full_fname, 'rb'))
                self.__debug("# - Upload filename: %s" % fname )

    """
    Create new folder on FTP server
    """
    def create_folder(self, folder_name, num = 0):
        
        folders = folder_name.split('/')
        folder_count = len( folders )
        
        current_folder = folders[num]

        filelist = []

        self.__ftp.dir(self.__parse)
        folder_found = 0
        
        self.__debug("Folders found: %s" % self.__filelist )

        for f in self.__filelist:
            if current_folder in f:
                self.__debug("Folder {%s} can not be created becures its exists already" % current_folder )
                folder_found=1

        if folder_found == 0:
            self.__debug( self.__ftp.mkd( current_folder ) )
    
        self.go_to_folder(current_folder)

        folder_number = (int(num) + 1 )
        
        self.__filelist = []
        self.__debug("Clearn folder list: %s" % self.__filelist )

        if ( folder_number != folder_count ):
            self.create_folder(folder_name, folder_number )