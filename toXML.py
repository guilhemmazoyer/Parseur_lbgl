# -*- coding : utf-8 -*-

import os
import textmanipulation as txtmanip
from fileManager import FileManager as fM
from PdfToPlainText import PdfToPlainText

class ToXML:
    folder = ""
    files = []
    manager = None
    pdfTPT = None

    def __init__(self,folder):
        # Variable instanciee a partir des parametres
        self.folder = folder

        # Initialisations de FileManager et PdfToPlainText
        self.manager = fM(self.folder)
        self.pdfTPT = PdfToPlainText(self.manager)

        # Creer le dossier resultat
        self.manager.createResultFolder()

        # Recuperation des fichiers
        files = os.listdir(self.folder)
        files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
        self.files = list(files)

    def allPDF(self, numberFiles, i, progressBar):
        progressBar.progress(i)
        for file in range(i, i+numberFiles): # index du début du thread jusqu'au nombre de fichier max du thread
            self.pdfTPT.fileProcessing(self.files[file])
            result = txtmanip.arrangeXML(self.pdfTPT)
            self.manager.writeXML(self.pdfTPT, result)
