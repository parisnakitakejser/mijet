import mijet.file.directory

directory = mijet.file.directory.MoveTo()
directory.directory = "./tmp/"
directory.directoryExtract = "./tmp/unzip/"
directory.run()