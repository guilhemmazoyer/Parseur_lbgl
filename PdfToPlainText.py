import re
import textmanipulation as txtmanip
from textmanipulation import (
    REGEX_TITLE, REGEX_CORRECT_TITLE, REGEX_AUTHORS,
    REGEX_MULTI_AUTHORS, REGEX_ABSTRACT, REGEX_NO_ABSTRACT)

class PdfToPlainText:
    # variables utiles pour les operations
    currentFile = ""
    manager = None
    doc = []

    # variables a recuperer
    filename = ""
    title = ""
    authors = []
    emails = []
    abstract = ""
    references = []

    # Initialise le manager passe en parametre
    def __init__(self, manager):
        self.manager = manager
    
    # Processus majeur, determine tous les attributs a partir d'un fichier
    def fileProcessing(self, file):
        self.currentFile = file
        self.doc = self.manager.openFile(self.manager, self.currentFile)

        # Recupere la premiere page et les metadonnees
        text = self.getTextFirstPage(self)
        metadata = self.getMetadata(self)

        self.__setFilename(self)
        self.__setTitle(self, metadata, text)
        self.__setAuthorsAndemails(self, metadata, text)
        self.__setAbstract(self, text)

        fullText = self.getTextAllPages(self)
        self.__setReferences(self, fullText)

    # Recupere la page de garde de l'article
    def getTextFirstPage(self):
        # Ouverture de la premiere page du fichier .pdf
        page = self.doc.load_page(0)
        dl = page.get_displaylist()
        tp = dl.get_textpage()
        rawText = tp.extractText()

        return txtmanip.cleanText(rawText)
    
    # Recupere toutes les pages du documents
    def getTextAllPages(self):
        # Ouverture de toutes les pages du fichier .pdf
        # TODO

        # Ouverture de la premiere page du fichier .pdf
        # A enlever apres la realisation de la partie au dessus
        page = self.doc.load_page(0)
        dl = page.get_displaylist()
        tp = dl.get_textpage()
        rawText = tp.extractText()

        return txtmanip.cleanText(rawText)

    # Recupere les metadonnees du fichier courant
    def getMetadata(self):
        return self.doc.metadata

    # Definit le nom du fichier
    def __setFilename(self):
        self.filename = self.manager.getFileName(self.manager, self.currentFile)

    # Definit le titre de l'article
    def __setTitle(self, metadatas, text):
        title = metadatas["title"]

        # Si les metadata sont incoherentes
        if re.search(REGEX_CORRECT_TITLE, title) is not None:
            
            # On recupere le titre avec regex (premiere ligne)
            if re.search(REGEX_TITLE, text) is not None:
                title = re.search(REGEX_TITLE, text).group(0)
                title = txtmanip.cleanText(title)
                
        else:
            title = "Titre non trouvé !"

        self.title = title



    # Definit les auteurs et leurs emails
    def __setAuthorsAndemails(self, metadatas, text):
        authorDisplay = ""
        author = metadatas["author"]

        if author is None or author == "":
            if re.search(REGEX_AUTHORS, text) is not None:
                authorsEmail = re.findall(REGEX_AUTHORS, text)
                for author in authorsEmail:
                    email_decompose = author[0:author.find('@')]

                    if email_decompose.find('.') != -1:
                        nom = email_decompose[0:email_decompose.find('.')]
                        prenom = email_decompose[email_decompose.find('.') + 1:]
                        authorDisplay += nom + prenom + "; "
                    else:
                        authorDisplay += email_decompose + "; "

            else:
                if re.search(REGEX_MULTI_AUTHORS, text, re.MULTILINE) is not None:
                    authorsEmail = re.findall(REGEX_MULTI_AUTHORS, text, re.MULTILINE)

                    for author in authorsEmail:
                        email_decompose = author[author.find('{') + 1:author.find('}')]
                        names = re.findall("[\w]+", email_decompose)

                        for name in names:
                            authorDisplay += name + "; "
                else:
                    authorDisplay += "Auteurs non trouvés"
        else:
            self.__getEmails(self, text)
            author = txtmanip.cleanText(author)
            authorDisplay = author

        return authorDisplay

    def __getEmails(self, text):
        

    # Definit la partie Abstract de l'article
    def __setAbstract(self, text):
        patternAbstract = REGEX_ABSTRACT
        patternWithoutAbstract = REGEX_NO_ABSTRACT

        if re.search(patternAbstract, text) is not None:
            abstract = re.search(patternAbstract, text).group(3)
            abstractDisplay = txtmanip.cleanText(abstract)

        elif re.search(patternWithoutAbstract, text) is not None :
            abstract = re.search(patternWithoutAbstract, text).group(0)
            abstractDisplay = txtmanip.cleanText(abstract)
            
        else:
            abstractDisplay = "Abstract non trouvé !"

        return abstractDisplay

    # Definit les references de l'article
    def __setReferences(self, fullText):
        # TODO
        print()