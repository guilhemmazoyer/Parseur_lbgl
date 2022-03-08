REGEX_TITLE = r"^\A(.*)\n"
REGEX_CORRECT_TITLE = r"/|\\"
REGEX_AUTHORS = r"([\w.\-]+@[\w.\-]+[.][a-zA-Z]{2,4})"
REGEX_MULTI_AUTHORS = r"^{[\w,\s\-]+}@[\w.\-]+[.][a-zA-Z]{2,4}"
REGEX_ABSTRACT = r"(Abstract(-|.| |\n))\n? ?((.|\n)*)(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
REGEX_NO_ABSTRACT = r"(?<=\n)(.|\n)*(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"

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

def arrangeTXT(pdfTTP):
    # TODO
    print("")

def arrangeXML(pdfTTP):
    # TODO
    print("")