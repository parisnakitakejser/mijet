import mijet.file.directory

directory = mijet.file.directory.moveTo()
directory.directory = "./tmp/"
directory.directoryExtract = "./tmp/unzip/"
directory.run()