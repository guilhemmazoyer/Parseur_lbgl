REGEX_TITLE = r"^\A(.*)\n"
REGEX_INCORRECT_TITLE = r"/|\\"
REGEX_EMAILS = r"([\w.\-]+@[\w.\-]+[.][a-zA-Z]{2,4})"
REGEX_MULTI_EMAILS = r"^{[\w,\s\-]+}@[\w.\-]+[.][a-zA-Z]{2,4}"
REGEX_ABSTRACT = r"(Abstract(-|.| |\n))\n? ?((.|\n)*)(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_NO_ABSTRACT = r"(?<=\n)(.|\n)*(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_REFERENCES = ""

def cleanText(text):
    # Pour que le texte soit sur une seule ligne
    text = text.replace('\n', ' ')
    # 2 espaces -> 1
    text = text.replace("  ", ' ')
    # retour à la ligne mot coupe
    text = text.replace("- ", '')
    # è UTF-8
    text = text.replace("`e", 'è')
    # é UTF-8
    text = text.replace("´e", 'é')
    
    return text

def authorFormat(authors):
    newAuthors = []
    for author in authors:
        newAuthors.append(author.title())
    return newAuthors

def arrangeTXT(pdfTTP):
    mergeAll = pdfTTP.filename + '\n' + pdfTTP.title + '\n'

    for author in pdfTTP.authors:
        mergeAll += author + '; '
    mergeAll += '\n'

    for email in pdfTTP.emails:
        mergeAll += email + '; '
    mergeAll += '\n'

    mergeAll += pdfTTP.abstract + '\n'

    for reference in pdfTTP.references:
        mergeAll += reference + "; "

    return mergeAll

def arrangeXML(pdfTTP):
    mergeAll = "<article>\n"
    mergeAll += "\t<preamble> " + pdfTTP.filename + " </preamble>\n"
    mergeAll += "\t<titre> " + pdfTTP.title + " </title>\n"
    mergeAll += "\t<auteurs>\n"
    
    '''
    i = 0
    for author in pdfTTP.authors:
        mergeAll = "\t\t<auteur>\n"
        mergeAll = "\t\t\t<name>\n " + author + " </name>\n"
        mergeAll = "\t\t\t<mail> " + pdfTTP.emails[i] + " </mail>\n"
        mergeAll = "\t\t</auteur>\n"

        i+=1
    '''
    
    mergeAll += "\t</auteurs>\n"
    mergeAll += "\t<abstract> " + pdfTTP.abstract + " </abstract>\n"
    mergeAll += "\t<biblios>\n"
    for reference in pdfTTP.references:
        mergeAll += "\t\t<biblio> " + reference + " </biblio>\n"
    mergeAll += "\t</biblios>\n"
    mergeAll += "</article>"

    return mergeAll
