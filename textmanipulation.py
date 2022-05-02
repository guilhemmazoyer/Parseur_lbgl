# -*- coding : utf-8 -*-

import re

REGEX_TITLE = r"^([A-Z].*)+"
REGEX_ALL_EMAILS = r"{?\(?\b[\w][\w, .-]*[a-z\d]\)?}?\n?[@|Q][\w\-_.]+"
REGEX_TYPE_MULTI_EMAILS = r"({|\()?([\w.\- ]+,[\w.\- ]+)+(\)|})?\n?@[\w\-_.]+"
REGEX_POST_TITLE_PRE_ABSTRACT = r"(?<=\n)(.|\n)+(?=(Abstract))"
REGEX_POST_TITLE_PRE_NO_ABSTRACT = r"(?<=\n)(.|\n)+(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_ABSTRACT = r"(Abstract(-|.| |\n))\n? ?((.|\n)*)(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_NO_ABSTRACT = r"(?<=\n)(.|\n)*(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_INTRODUCTION = r"(INTRODUCTION|Introduction)\n* *((.|\n)*)(?=(\n2.? ?\n?|\nII.? ))"
REGEX_CORPS = r"\n(2|II)\.? ?.*\n((.|\n)*)(?=conclusion|discussion)"
REGEX_CONCLUSION = r"(.*Conclusions?.*)(.|\n)*(?=References|acknowledgments?|Follow-Up Work|Appendix)"
REGEX_DISCUSSION = r".*discussion.*(.|\n)*(?=appendix|conclusions?|\n\d)"
REGEX_REFERENCES = r"(((?<=References|REFERENCES)|(?<=Bibliographie|BIBLIOGRAPHIE))+((.|\n)*))"
REGEX_TABREFERENCES = r"\[[0-9|, ]+\]"

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
    text = text.replace('&','&amp')
    text = text.replace('>','&gt')
    text = text.replace('<','&lt')

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
    mergeAll += pdfTPT.corps + '\n'
    mergeAll += pdfTPT.discussion + '\n'
    mergeAll += pdfTPT.conclusion + '\n'
    for reference in pdfTPT.references:
        mergeAll += reference + ";\n"

    return mergeAll

def arrangeXML(pdfTPT):

    pdfTPT.abstract = cleanToXMLFormat(pdfTPT.abstract)
    pdfTPT.affiliations = cleanToXMLFormat(pdfTPT.affiliations)
    pdfTPT.conclusion = cleanToXMLFormat(pdfTPT.conclusion)
    pdfTPT.corps = cleanToXMLFormat(pdfTPT.corps)
    pdfTPT.discussion = cleanToXMLFormat(pdfTPT.discussion)

    mergeAll = "<article>\n"
    mergeAll += "\t<preambule>" + pdfTPT.filename + "</preambule>\n"
    mergeAll += "\t<titre>" + pdfTPT.title + "</titre>\n"
    mergeAll += "\t<auteurs>\n"

    maxIndex = max(max(len(pdfTPT.authors), len(pdfTPT.emails)), len(pdfTPT.affiliations))

    for i in range(maxIndex):
        mergeAll += "\t\t<auteur>\n"

        try:
            mergeAll += "\t\t\t<nom>" + pdfTPT.authors[i] +"</nom>\n"
        except:
            mergeAll += "\t\t\t<nom></nom>\n"
            
        try:
            mergeAll += "\t\t\t<email>" + pdfTPT.emails[i] + "</email>\n"
        except:
            mergeAll += "\t\t\t<email></email>\n"

        try:
            mergeAll += "\t\t\t<affiliation>" + pdfTPT.affiliations[i] + "</affiliation>\n"
        except:
            mergeAll += "\t\t\t<affiliation></affiliation>\n"

        mergeAll += "\t\t</auteur>\n"

    mergeAll += "\t</auteurs>\n"
    mergeAll += "\t<abstract>" + pdfTPT.abstract + "</abstract>\n"
    mergeAll += "\t<introduction>" + pdfTPT.introduction + "</introduction>\n"
    mergeAll += "\t<corps>" + pdfTPT.corps + "</corps>\n"
    mergeAll += "\t<discussion>" + pdfTPT.discussion + "</discussion>\n"
    mergeAll += "\t<conclusion>" + pdfTPT.conclusion + "</conclusion>\n"
    mergeAll += "\t<biblios>\n"

    for reference in pdfTPT.references:
        if reference != "":
            mergeAll += "\t\t<biblio>" + reference + "</biblio>\n"

    mergeAll += "\t</biblios>\n"
    mergeAll += "</article>"

    return mergeAll
