# -*- coding : utf-8 -*-

from dis import dis
from distutils.debug import DEBUG
import re
import difflib
import textmanipulation as txtmanip
from textmanipulation import (
    REGEX_ABSTRACT_NO_INTRO, REGEX_CONCLUSION, REGEX_DISCUSSION, REGEX_INTRODUCTION, REGEX_TITLE, REGEX_ABSTRACT,
    REGEX_TITLE, REGEX_ALL_EMAILS, REGEX_TYPE_MULTI_EMAILS,
    REGEX_POST_TITLE_PRE_ABSTRACT, REGEX_POST_TITLE_PRE_NO_ABSTRACT, REGEX_ABSTRACT,
    REGEX_NO_ABSTRACT, REGEX_REFERENCES, REGEX_TABREFERENCES)

class PdfToPlainText:
    # variables utiles pour les operations
    currentFile = ""
    manager = None
    doc = []
    emailFindingResult = True
    preCoupage = ""
    listWordForAffiliation = []

    # DEBUG
    DEBUG_TEXT = False
    DEBUG_TITLE = False
    DEBUG_AUTHOR = False
    DEBUG_EMAIL = False
    DEBUG_AFFILIATION = False
    DEBUG_ABSTRACT = False
    DEBUG_INTRODUCTION = False
    DEBUG_REFERENCE = False

    # variables a recuperer
    metadata = []
    filename = ""
    title = ""
    authors = []
    emails = []
    affiliations = []
    abstract = ""
    introduction = ""
    discussion = ""
    conclusion = ""
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

        # Creer le text permettant de faire des verifications avec difflib
        if re.search(REGEX_POST_TITLE_PRE_ABSTRACT, text) is not None:
            preCoupage = re.search(REGEX_POST_TITLE_PRE_ABSTRACT, text).group(0)
        else:
            if re.search(REGEX_POST_TITLE_PRE_NO_ABSTRACT, text) is not None:
                preCoupage = re.search(REGEX_POST_TITLE_PRE_NO_ABSTRACT, text).group(0)
            else:
                preCoupage = "N/A"

        self.preCoupage = txtmanip.allClean(preCoupage)
        self.listWordForAffiliation = re.split("\n| ", preCoupage)

        # Recupere tous les attributs souhaites
        self.__setFilename()
        self.__setTitle(self.metadata, text)
        self.__setEmails(text)
        self.__setAuthors()
        self.__setAffiliations(text)
        self.__setAbstract()
        self.__setIntroduction()
        self.__setDiscussion()
        self.__setConclusion()
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

    def getTextAllPage(self):
        nbPage = self.getNbPages()
        text = ""

        for page in range(0, nbPage - 1, 1):
            text += self.getTextAnyPage(page)
        
        return text
        

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
        self.filename = self.manager.getFileName(self.currentFile + ".pdf")

    # Defini le titre de l'article
    def __setTitle(self, metadatas, text):
        metas_title = metadatas["title"]

        if not metas_title or metas_title == "" or not re.search(REGEX_TITLE, metas_title):
            if re.search(REGEX_TITLE, text) is not None:
                self.title = re.search(REGEX_TITLE, text).group(0)
            else:
                self.title = "N/A"
        else:
            self.title = metas_title

        if self.DEBUG_TITLE:
            print(self.title + "\n\n")

    # Trouve les emails
    def __setEmails(self, text):   
        if re.search(REGEX_ALL_EMAILS, text) is not None:
            # Recupere les adresses emails dans le text
            emails = re.findall(REGEX_ALL_EMAILS, text, re.MULTILINE)
            
            # Ajout des emails et verification des formats peu frequents
            for email in emails:
                email = re.sub('Q', '@', email)
                if re.search(REGEX_TYPE_MULTI_EMAILS, email) is not None: # multi email
                    # recuperation de l'email
                    email = txtmanip.cleanEmail(email)

                    # recuperation des noms dans l'adresse
                    names_pre_adresse = email[0:email.find('@')]
                    adresse_post_name = email[email.find('@'):]
                    names = re.findall(r"[\w.-]+", names_pre_adresse)
                    for name in names:
                        email = name + adresse_post_name
                        self.emails.append(email)
                else:
                    email = txtmanip.cleanEmail(email)
                    self.emails.append(email)

            self.emailFindingResult = False # email trouvee

        else:
            self.emails.append("N/A")
            self.emailFindingResult = True # pas d'email

        if self.DEBUG_EMAIL:
            for email in self.emails:
                print(email + "; ")
            print("\n")

    # Defini les auteurs
    def __setAuthors(self):
        if self.emailFindingResult: # pas d'email
            self.authors.append("N/A")
        
        else: # email
            self.getAuthorsFromEmails()
        
        if self.DEBUG_AUTHOR:
            for author in self.authors:
                print(author + "; ")
            print("\n")

    # Recupere la partie Auteurs de la partie email
    def getAuthorsFromEmails(self):
        for email in self.emails:
            email_decompose = email[0:email.find('@')]
            tab_email_decompose = email_decompose.split('.')
            result_author = ''
            for i in range(len(tab_email_decompose)):
                textName = difflib.get_close_matches(tab_email_decompose[i],self.listWordForAffiliation)
                if i == 0:
                    if textName != []:
                        result_author += textName[0]
                    else:
                        result_author += tab_email_decompose[i]
                else:
                    if textName != []:
                        result_author += " " + textName[0]
                    else:
                        result_author += " " + tab_email_decompose[i]
            
            result_author = txtmanip.authorClean(result_author)
            self.authors.append(result_author)

    # Defini la partie Affiliation de l'article
    def __setAffiliations(self, text):
        if self.emailFindingResult: # si pas d'email et d'auteur
            for i in range(len(self.authors)-1):
                self.affiliations.append("N/A")
            return None # Saute toute l'execution qui suit

        # Verification de la proximité entre deux mots et utiliser le mot trouvé pour faire la borne du regex avec l'email
        for i in range(len(self.authors)):
            wordCloseToAuthor = ""

            # Recupere le nom de l'auteur
            splitedAuthors = self.authors[i].split(sep=" ")
            if len(splitedAuthors) < 1:
                authorLastName = self.authors[i]
            else:
                authorLastName = splitedAuthors[len(splitedAuthors)-1]
            
            # Trouve le mot le plus proche du nom de l'auteur dans le texte
            wordsCloseToAuthor = difflib.get_close_matches(authorLastName,self.listWordForAffiliation)

            if len(wordsCloseToAuthor) < 1: # Si aucun mot ne correspond au nom de l'auteur donne
                wordCloseToAuthor = ""
            else:
                wordCloseToAuthor = wordsCloseToAuthor[len(wordsCloseToAuthor)-1]

            # Recupere l'email associee
            emailToUse = self.emails[i]
            emailTruePart = emailToUse[0:emailToUse.find('@')]

            wordsCloseToEmail = difflib.get_close_matches(emailTruePart,self.listWordForAffiliation)
            wordCloseToEmail = ""
            for word in wordsCloseToEmail:
                wordCloseToEmail += word

            '''
            print('\n' + self.emails[i] + " #")
            print(emailTruePart + " ##")
            print(wordsCloseToAuthor, " ###")
            print(wordCloseToAuthor + " ####")
            print(wordsCloseToEmail, " #####")
            print(wordCloseToEmail + " ######")
            '''

            regex_affiliation = r"(?<=" + wordCloseToAuthor + ")(.|\n)+(?=(" + self.emails[i] + "))"
            if re.search(regex_affiliation, self.preCoupage) is not None:
                resultAffiliation = re.search(regex_affiliation, self.preCoupage).group(0)
                self.affiliations.append(resultAffiliation)
            else:
                self.affiliations.append("N/A")
        
        if self.DEBUG_AFFILIATION:
            for affiliation in self.affiliations:
                print(affiliation + "; ")
            print("\n")

    # Defini la partie Abstract de l'article
    def __setAbstract(self):
        text = self.getTextAnyPage(0) + self.getTextAnyPage(1)  
        print(self.getTextAnyPage(0))

        try:
            abstract = re.search(REGEX_ABSTRACT, text, re.IGNORECASE).group(3)
        except:
            try:
                abstract = re.search(REGEX_NO_ABSTRACT, text).group(0)
            except:
                try:
                  abstract = re.search(REGEX_ABSTRACT_NO_INTRO, text, re.IGNORECASE).group(3)  
                except:
                    abstract = "N/A"
            
        self.abstract = txtmanip.pasCleanText(abstract)

        if self.DEBUG_ABSTRACT:
           print(self.abstract + "\n\n")

    # Definit la partie introduction
    def __setIntroduction(self):
        text = self.getTextAnyPage(0) + self.getTextAnyPage(1) + self.getTextAnyPage(2)
        introduction = ""
        if re.search(REGEX_INTRODUCTION, text) is not None:
            introduction = re.search(REGEX_INTRODUCTION, text).group(2)
        if self.DEBUG_INTRODUCTION:
            print(introduction + "\n\n")
        self.introduction = txtmanip.pasCleanText(introduction)


    # Definit la partie discussion
    def __setDiscussion(self):
        text = ""
        discussion = ""
        page = 0

        # On recupere la partie discussion
        for page in range(self.getNbPages()-1, 0, -1):
            text = self.getTextAnyPage(page)

            # Si on trouve le mot discussion
            if re.search("discussion", text, re.IGNORECASE):
                if page <= self.getNbPages() - 3:
                    text += self.getTextAnyPage(page + 1)
                    text += self.getTextAnyPage(page + 2)
        
                if re.search(REGEX_DISCUSSION, text, re.IGNORECASE):
                    discussion = re.search(REGEX_DISCUSSION, text, re.IGNORECASE).group(0)
    
        self.discussion = txtmanip.pasCleanText(discussion)

    # Definit la partie conclusion
    def __setConclusion(self):
        
        text = ""
        conclusion = "N/A"
        page = 0

        # On recupere la partie conclusion
        for page in range(self.getNbPages()-1, 0, -1):
            text = self.getTextAnyPage(page)

            # Si on trouve le mot conclusion
            if re.search("Conclusion", text, re.IGNORECASE):
                if page <= self.getNbPages() - 3:
                    text += self.getTextAnyPage(page + 1)
                    text += self.getTextAnyPage(page + 2)
                break
        
        if re.search(REGEX_CONCLUSION, text, re.IGNORECASE):
            conclusion = re.search(REGEX_CONCLUSION, text, re.IGNORECASE).group(0)
    
        self.conclusion = txtmanip.pasCleanText(conclusion)

    # Definit les references de l'article
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
                    self.references.append("N/A")
                
                break # on stop le parcours de pages

            else: # Enregistrement de la page precendente si le mot "Référence" n'est pas trouve
                text = textTest + ' ' + text + ' '
