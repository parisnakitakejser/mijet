import shutil, os, sys
from stat import *

class File:
    debug = "on"

    """
    Debug messegt will be printet to terminal if debugLevel is on
    """
    def __debug(self,msg):
        if ( self.debug.lower() == "on" ):
            print msg

    """
    Remove all files insite of this current folder.
    """
    def remove_all_files_in_folder(self,folder_name):
        
        for file in os.listdir( folder_name ):
            pathname = os.path.join(folder_name, file)
            
            mode = os.stat(pathname)[ST_MODE]
            
            if S_ISDIR(mode):
                self.__debug("Skip this is a folder: %s" % file )
            elif S_ISREG(mode):
                try:
                    os.remove(folder_name + file )
                    self.__debug("Remove file: %s" % folder_name + file )
                except OSError:
                    pass
            else:
                self.__debug("Its not a file or a folder - skipping: %s" % file )

        self.__debug("Alle files in {%s} folder are removed" % folder_name)


    