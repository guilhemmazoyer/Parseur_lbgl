import fitz
import os, sys, shutil, platform

class FileManager:
    OS_NAME = False
    folder = ""
    resFolder = ""
    option = ""
    index = 0
    files = []

    def __init__(self, folder, option):
        self.folder = folder
        self.option = option
        
        # Recuperation du systeme d'exploitation, True si "Windows", False sinon
        self.OS_NAME = (platform.system() == "Windows")

    # Creer un dossier "result" dans le dossier source
    def createResultFolder(self):
        if os.path.exist(self.resFolder):
            shutil.rmtree(self.resFolder)
        os.mkdir(self.resFolder)

    #
    def openFile(self, file):
        if self.OS_NAME:
            return fitz.open(self.folder + "\\" + file)
        else:
            return fitz.open(self.folder + "/" + file)

    def getFileName(self, file):
        if self.OS_NAME:
            file_basename = os.path.basename(self.folder + "\\" + file)
        else:
            file_basename = os.path.basename(self.folder + "/" + file)
        
        return file_basename[0:file_basename.find('.')]

    # 
    def createResultFileTXT(self):
        # TODO
        print("")
    
    #
    def createResultFileXML(self):
        # TODO
        print("")

    #
    def writeTxt(self, txt_basename, filename_display, title_display , author_display, abstract_display):
        # Creation et ouverture du fichier .txt
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".txt", "w+")

        # Ecriture du nom du fichier, du titre, des auteurs et de l'abstract
        txtFileToFill.write(filename_display)
        txtFileToFill.write(title_display)
        txtFileToFill.write(author_display)
        txtFileToFill.write(abstract_display)

        # Fermeture du fichier
        txtFileToFill.close()

    #
    def writeXML(self, txt_basename, filename_display, title_display , author_display, abstract_display):
        # Creation et ouverture du fichier .xml
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".xml", "w+")

        # TODO

        # Fermeture du fichier
        txtFileToFill.close()
    
    def pdfFilesProcessing(self):
        # Créer le dossier result
        self.resFolder = self.folder + "/result"
        self.createResultFolder(self)

        # TODO

    def pdfFilesProcessingWindows(self):
         # Créer le dossier result
        self.resFolder = self.folder + "\result"
        self.createResultFolder(self)

        # TODO