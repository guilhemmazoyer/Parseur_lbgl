# -*- coding : utf-8 -*-

import re
import xml.etree.cElementTree as ET
import xml.dom.minidom

m_encoding = 'UTF-8'

REGEX_TITLE = r"^([A-Z].*)+"
REGEX_ALL_EMAILS = r"{?\(?\b[\w][\w, .-]*[a-z\d]\)?}?\n?[@|Q][\w\-_.]+"
REGEX_TYPE_MULTI_EMAILS = r"({|\()?([\w.\- ]+,[\w.\- ]+)+(\)|})?\n?@[\w\-_.]+"
REGEX_POST_TITLE_PRE_ABSTRACT = r"(?<=\n)(.|\n)+(?=(Abstract))"
REGEX_POST_TITLE_PRE_NO_ABSTRACT = r"(?<=\n)(.|\n)+(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_ABSTRACT = r"(Abstract(-|.| |\n)|a b s t r a c t)\n? ?((.|\n)*)(?=((1|I)(\n| |( \n)|. *\n*)Introduction))"
REGEX_NO_ABSTRACT = r"(?<=\n)(.|\n)*(?=(1(\n| |( \n)|. *\n*)Introduction)|(I. INTRODUCTION))"
REGEX_ABSTRACT_NO_INTRO = r"(Abstract(-|.| |\n)|a b s t r a c t)\n? ?((.|\n)*)(?=1|II)"
REGEX_INTRODUCTION = r"(INTRODUCTION|Introduction)\n* *((.|\n)*)(?=\nII\.|[^-]\n2\.?( |\n))"
REGEX_CONCLUSION = r"((\. |\d\.? ?\n)Conclusions?.*)\n?((.|\n)*)(?=\n(References|acknowledgments?|Follow-Up Work|Appendix))"
REGEX_DISCUSSION = r".*discussion.*(.|\n)*(?=appendix|conclusions?|Acknowledgments|\d)"
#r"(\d Discussion.*)(.|\n)*(?=appendix|conclusions?Acknowledgments|\n\d)"
REGEX_REFERENCES = r"(((?<=References|REFERENCES)|(?<=Bibliographie|BIBLIOGRAPHIE))+((.|\n)*))"
REGEX_TABREFERENCES = r"\[[0-9|, ]+\]"
REGEX_AFFILIATIONS = r"(?<=@)([^\.]*)\."

# Retire les caracteres indesirables d'un String
def preCleanText(text):
    # 2 espaces -> 1    
    text = text.replace("  ", ' ')
    # á UTF-8
    text = text.replace("´a", 'á')
    # à UTF-8
    text = text.replace("`a", 'à')
    # À UTF-8
    text = text.replace("`A", 'À')
    # è UTF-8
    text = text.replace("`e", 'è')
    # é UTF-8
    text = text.replace("´e", 'é')
    # É UTF-8
    text = text.replace("´E", 'É')
    # ç UTF-8
    text = text.replace("c¸",'ç')
    # î UTF-8
    text = text.replace("ˆı",'î')
    # mot coupe
    text = text.replace("- ", '')
    # retour à la ligne mot coupe
    text = text.replace("- \n", '')
    # caractères spéciaux
    text = text.replace("♮", '')
    text = text.replace("♭", '')
    
    return text

def pasCleanText(text):
    # Pour que le texte soit sur une seule ligne
    text = text.replace('\n', ' ')
    text = text.replace('\n\n', '\n')

    return text

def allClean(text):
    text = preCleanText(text)
    text = pasCleanText(text)

    return text

# Passe la premiere lettre du nom et prenom des auteurs en majuscule
def authorFormat(authors):
    newAuthors = []
    for author in authors:
        newAuthors.append(author.title())

    return newAuthors

def authorClean(name):
    name = name.replace('*', '')
    name = name.replace(',', '')
    name = name.replace('{', '')
    name = name.replace('}', '')
    name = name.title()
    
    return name

def cleanEmail(email):
    email = email.replace('{', '')
    email = email.replace('}', '')
    email = email.replace('(', '')
    email = email.replace(')', '')
    email = email.replace('\n', '')
    return email

def cleanAllEmails(emails):
    newEmails = []
    for email in emails:
        email = email.replace('{', '')
        email = email.replace('}', '')
        email = email.replace('(', '')
        email = email.replace(')', '')
        email = email.replace('\n', '')
        newEmails.append(email)

    return newEmails

def cleanToXMLFormat(text):
    text = text.replace('&',' &amp ')
    text = text.replace('>',' &gt ')
    text = text.replace('<',' &lt ')

    return text

# Arrange le texte ecris dans le fichier .xml a partir des attributs de pdfTPT
def arrangeTXT(pdfTPT):

    mergeAll = pdfTPT.filename + '\n' + pdfTPT.title + '\n'
    for author in pdfTPT.authors:
        mergeAll += author + '; '
    mergeAll += '\n'

    for email in pdfTPT.emails:
        mergeAll += email + '; '
    mergeAll += '\n'

    for affiliation in pdfTPT.affiliations:
        mergeAll += affiliation + '; '
    mergeAll += '\n'

    mergeAll += pdfTPT.abstract + '\n'
    mergeAll += pdfTPT.introduction + '\n'
    mergeAll += pdfTPT.discussion + '\n'
    mergeAll += pdfTPT.conclusion + '\n'
    for reference in pdfTPT.references:
        mergeAll += reference + ";\n"

    return mergeAll

def arrangeXML(pdfTPT):

    root = ET.Element("article")

    ET.SubElement(root, "preamble").text = pdfTPT.currentFile
    ET.SubElement(root, "titre").text = pdfTPT.title

    auteurs = ET.SubElement(root, "auteurs")
    maxIndex = max(max(len(pdfTPT.authors), len(pdfTPT.emails)), len(pdfTPT.affiliations))

    for i in range(maxIndex):
        auteur = ET.SubElement(auteurs, "auteur")
        ET.SubElement(auteur, "name").text = pdfTPT.authors[i]
        try:
            ET.SubElement(auteur, "mail").text = pdfTPT.emails[i]
        except:
            ET.SubElement(auteur, "mail").text = ""
        try:
            ET.SubElement(auteur, "affiliation").text = pdfTPT.affiliations[i]
        except:
            ET.SubElement(auteur, "affiliation").text = ""

    ET.SubElement(root, "abstract").text = pdfTPT.abstract
    ET.SubElement(root, "introduction").text = pdfTPT.introduction
    ET.SubElement(root, "discussion").text = pdfTPT.discussion
    ET.SubElement(root, "conclusion").text = pdfTPT.conclusion

    biblioText = ""
    for reference in pdfTPT.references:
        if reference != "":
            biblioText += reference

    ET.SubElement(root, "biblio").text = biblioText

    dom = xml.dom.minidom.parseString(ET.tostring(root))
    xml_string = dom.toprettyxml()

    return xml_string
