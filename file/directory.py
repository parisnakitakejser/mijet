import os
import zipfile

class MoveTo:
    directory = ""
    directoryExtract = ""
    debug = "on"
    removeZipAfterExtract = 1
    
    """
    Debug messegt will be printet to terminal if debugLevel is on
    """
    def __debug(self,msg):
        if ( self.debug.lower() == "on" ):
            print msg
    
    """
    Remove file from system
    """
    def __remove_file(self, filePath):
        
        if ( os.path.isfile(filePath) ):
            os.remove(filePath)
            self.__debug("## - File is removed: "+ filePath)
        else:
            self.__debug("## Error: file found, but not ready to be removed.")

    """
    Look up about its a zipfile, if its match as a zipfile, its will extract all to extract directory.
    """
    def __unzip_file(self, filePath):

        if ( zipfile.is_zipfile(filePath) == True ):
            self.__debug("## - This is a zipfile, and will try to unzip it.")

            with zipfile.ZipFile(filePath, "r") as z:
                z.extractall(self.directoryExtract)
                
                if ( self.removeZipAfterExtract == 1 ):
                    os.remove(filePath)
    
        else:
            self.__debug("## - This are not a zipfile, and will not be unzip.")

    """
    Scan directory target
    """
    def run(self):
        
        files = os.listdir(self.directory)
        
        for filename in files:
            self.__debug("# File move start: "+ filename)
            
            filePath = self.directory + filename
            
            # Remove .DS_Store file
            if ( filename.lower() == '.ds_store'):
                self.__debug("## This is .DS_Store file is a OS X index file, and will be removed.")
                self.__remove_file(filePath)
        
            # Skip if its a directory
            if ( os.path.isdir(filePath) == True ):
                self.__debug("## Skip this, becures its a directory")
            
            # Handle the process for the file
            else:
                self.__unzip_file(filePath)
            
            self.__debug("# FileMove done for this file #")
            self.__debug(" ")