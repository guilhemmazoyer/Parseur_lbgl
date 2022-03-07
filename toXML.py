import re, sys, os
import textmanipulation as txtmanip
from fileManager import FileManager as fM
from PdfToPlainText import PdfToPlainText
from textmanipulation import REGEX_ABSTRACT, REGEX_AUTHORS, REGEX_NO_ABSTRACT, REGEX_TITLE

class ToXML:
    folder = ""
    files = []
    manager = None
    pdfTPT = None

    def __init__(self,folder):
        # Variable instanciee a partir des parametres
        self.folder = folder

        # Initialisations de FileManager et PdfToPlainText
        self.manager = fM.__init__(self,folder)
        self.pdfTPT = PdfToPlainText.__init__()

        # Recuperation des fichiers
        files = os.listdir(self.folder)
        files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
        self.files = list(files)

    def allPDF(self):

        for file in self.files:
            self.pdfTPT.fileProcessing(file)
            result = txtmanip.arrangeXML(self.pdfTPT)
            self.manager.writeXML(result)