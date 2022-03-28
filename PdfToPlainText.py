# -*- coding : utf-8 -*-

import re
import difflib
import textmanipulation as txtmanip
from textmanipulation import (
    REGEX_TITLE, REGEX_MULTI_EMAILS, REGEX_POST_TITLE_PRE_ABSTRACT, 
    REGEX_ABSTRACT, REGEX_NO_ABSTRACT, REGEX_REFERENCES,
    REGEX_TABREFERENCES)

class PdfToPlainText:
    # variables utiles pour les operations
    currentFile = ""
    manager = None
    doc = []
    emailFindingResult = True

    # DEBUG
    DEBUG_TEXT = False
    DEBUG_TITLE = False
    DEBUG_AUTHOR = False
    DEBUG_EMAIL = False
    DEBUG_AFFILIATION = False
    DEBUG_ABSTRACT = False
    DEBUG_REFERENCE = False

    # variables a recuperer
    metadata = []
    filename = ""
    title = ""
    authors = []
    emails = []
    affiliations = []
    abstract = ""
    references = []

    # Initialise le manager passe en parametre
    def __init__(self, manager):
        self.manager = manager
    
    # Processus majeur, determine tous les attributs a partir d'un fichier
    def fileProcessing(self, file):

        self.resetCoreVariables()

        self.currentFile = file
        self.doc = self.manager.openFile(self.currentFile)

        # Recupere la premiere page et les metadonnees
        text = self.getTextFirstPage()
        if self.DEBUG_TEXT:
            print(text + "\n\n")

        self.metadata = self.getMetadata()

        # Recupere tous les attributs souhaites
        self.__setFilename()
        self.__setTitle(self.metadata, text)
        self.__setEmails(text)
        self.__setAuthors()
        self.__setAffiliations(text)
        self.__setAbstract(text)
        self.__setReferences()

    # Reinitialise certaines variables
    def resetCoreVariables(self):
        self.doc = []
        self.authors = []
        self.emails = []
        self.affiliations = []
        self.references = []

    # Recupere la page de garde de l'article
    def getTextFirstPage(self):
        # Ouverture de la premiere page du fichier .pdf
        page = self.doc.load_page(0)
        dl = page.get_displaylist()
        tp = dl.get_textpage()
        rawText = tp.extractText()

        return txtmanip.preCleanText(rawText)

    # Recupere la derniere page de l'article
    def getTextLastPage(self):
        # Ouverture de la premiere page du fichier .pdf
        page = self.doc.load_page(self.getNbPages()-1)
        dl = page.get_displaylist()
        tp = dl.get_textpage()
        rawText = tp.extractText()

        return txtmanip.preCleanText(rawText)

    # Recupere la page desiree de l'article
    def getTextAnyPage(self, nb):
        # Ouverture de la nb page du fichier .pdf
        try:
            page = self.doc.load_page(nb)
            dl = page.get_displaylist()
            tp = dl.get_textpage()
            rawText = tp.extractText()

            return txtmanip.preCleanText(rawText)
        except IndexError:
            print("erreur de numéro de page")

    # Retourne le nombre de page dans le document
    def getNbPages(self):
        return self.doc.page_count

    # Recupere les metadonnees du fichier courant
    def getMetadata(self):
        return self.doc.metadata

    # Defini le nom du fichier
    def __setFilename(self):
        self.filename = self.manager.getFileName(self.currentFile)

    # Defini le titre de l'article
    def __setTitle(self, metadatas, text):
        metas_title = metadatas["title"]

        if not metas_title or metas_title == "" or not re.search(REGEX_TITLE, metas_title):
            if re.search(REGEX_TITLE, text) is not None:
                self.title = re.search(REGEX_TITLE, text).group(0)
            else:
                self.title = "Titre non trouvé"
        else:
            self.title = metas_title

        if self.DEBUG_TITLE:
            print(self.title + "\n\n")

    # Trouve les emails
    def __setEmails(self, text):   
        if re.findall(REGEX_MULTI_EMAILS, text, re.MULTILINE) != []:
            # Recupere les adresses emails dans le text
            emails = re.findall(REGEX_MULTI_EMAILS, text, re.MULTILINE)
            
            # Ajout des emails
            for email in emails:
                email = re.sub('Q', '@', email)
                self.emails.append(email)
            self.emailFindingResult = False # email trouvee

        else:
            self.emails.append("Email non trouvé")
            self.emailFindingResult = True # pas d'email

        if self.DEBUG_EMAIL:
            for email in self.emails:
                print(email + "; ")
            print("\n")

    # Defini les auteurs
    def __setAuthors(self):
        if self.emailFindingResult: # pas d'email
            self.authors.append("Auteur non trouvé")
        
        else: # email
            self.getAuthorsFromEmails()
            self.authors = txtmanip.authorFormat(self.authors)
        
        if self.DEBUG_AUTHOR:
            for author in self.authors:
                print(author + "; ")
            print("\n")

    # Recupere la partie Auteurs de la partie email
    def getAuthorsFromEmails(self):
        for email in self.emails:
            email_decompose = email[0:email.find('@')]
            self.emails = txtmanip.cleanEmails(self.emails)
            names = re.findall(r"[\w-]+", email_decompose)

            newName = ""
            for name in names:
                newName += name + " "
            newName = newName[0:len(newName)-1]
            self.authors.append(newName)

    # Defini la partie Affiliation de l'article
    def __setAffiliations(self, text):
        if self.emailFindingResult: # si pas d'email et d'auteur
            return

        preCoupage = re.search(REGEX_POST_TITLE_PRE_ABSTRACT, text).group(0)
        preCoupage = txtmanip.allClean(preCoupage)

        listWordForAffiliation = []
        listWordForAffiliation = preCoupage.split(sep=" ")

        # Verification de la proximité entre deux mots et utiliser le mot trouvé pour faire la borne du regex avec l'email
        for i in range(len(self.authors)):
            wordCloseToAuthor = difflib.get_close_matches(self.authors[i],listWordForAffiliation)
            regex_affiliation = r"(?<=" + wordCloseToAuthor + ")(.|\n)+(?=(" + self.emails[i] + "))"
            resultAffiliation = re.search(regex_affiliation, preCoupage).group(0)
            self.affiliations.append(resultAffiliation)

        if self.DEBUG_AFFILIATION:
            for affiliation in self.affiliations:
                print(affiliation + "; ")
            print("\n")

    # Defini la partie Abstract de l'article
    def __setAbstract(self, text):
        if re.search(REGEX_ABSTRACT, text) is not None:
            abstract = re.search(REGEX_ABSTRACT, text).group(3)

        # Dans le cas où le mot abstract n'est pas present
        elif re.search(REGEX_NO_ABSTRACT, text) is not None :
            abstract = re.search(REGEX_NO_ABSTRACT, text).group(0)
            
        else:
            abstract = "Abstract non trouvé"

        self.abstract = txtmanip.pasCleanText(abstract)

        if self.DEBUG_ABSTRACT:
           print(self.abstract + "\n\n")
        
    # Defini les references de l'article
    def __setReferences(self):
        text = ""
        textTest = ""

        # On part de la derniere page
        for pages in range(self.getNbPages()-1, 0, -1):
            textTest = self.getTextAnyPage(pages)

            if re.search(REGEX_REFERENCES, textTest) is not None: # trouve le mot references
                text = re.search(REGEX_REFERENCES, textTest).group(1) + ' ' + text + ' ' # on ajoute au début a partir du mot references
                text = txtmanip.preCleanText(text)
                if self.DEBUG_REFERENCE:
                    print("REFERENCES:\n" + text + "\n\n")

                if re.search(REGEX_TABREFERENCES, text) is not None: # verification de crochets
                    # on peut nettoyaer completement et supprimer les \n en surplus
                    text = txtmanip.pasCleanText(text)
                    tab_ref = re.split(REGEX_TABREFERENCES, text)

                    if len(tab_ref[0]) <= 5:
                        del tab_ref[0]
                    self.references = tab_ref
                    

                elif re.search(REGEX_TITLE, text, re.MULTILINE) is not None:
                    for reference in re.split(REGEX_TITLE, text):
                        self.references.append(txtmanip.pasCleanText(reference))

                else: # ajout d'une simple chaine de caractere
                    self.references.append("Référence non trouvée")
                
                break # on stop le parcours de pages

            else: # Enregistrement de la page precendente si le mot "Référence" n'est pas trouve
                text = textTest + ' ' + text + ' '
