import fitz
import os,sys

class fileManager:
    folder = ""
    resFolder = ""
    files = []

    def __init__(self, folder):
        self.folder = folder
        self.resFolder = folder + "/result"
        files = os.listdir(self.folder)
        files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
        self.files = list(files)

    def writeTxt(self, txt_basename, filename_display, title_display , author_display, abstract_display):
        # Creation repertoire resultat
        if not os.path.isdir(self.resFolder):
            os.mkdir(self.resFolder)

        # Creation et ouverture du fichier .txt
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".txt", "w+")

        # Ecriture du nom du fichier, du titre, des auteurs et de l'abstract
        txtFileToFill.write(filename_display)
        txtFileToFill.write(title_display)
        txtFileToFill.write(author_display)
        txtFileToFill.write(abstract_display)

        # Fermeture du fichier
        txtFileToFill.close()

    def getTextFirstPage(self):
        texts = []

        for file in self.files:

            # Ouverture du fichier .pdf
            doc = fitz.open(sys.argv[1] + '/' + file)
            page = doc.load_page(0)
            dl = page.get_displaylist()
            tp = dl.get_textpage()
            texts.append(tp.extractText())
        
        return texts
    
    def getMetadatas(self):
        metadatas = []
        index = 0
        for file in self.files:
            doc = fitz.open(sys.argv[1] + '/' + file)
            metadatas.append(doc.metadata)
            index += 1

        return metadatas

    def getFiles(self):
        return self.files