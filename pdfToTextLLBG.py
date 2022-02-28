from lib2to3.pgen2.token import EQUAL
import fitz, re, sys, os
import textmanipulation as txtmanip

# Ouverture fichiers pdf dans repertoire
files = os.listdir(sys.argv[1])
files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)

index = 0

for file in files:
    doc = fitz.open(sys.argv[1] + '/' + file)

    page = doc.load_page(0)  # Lecture de la premiere page TODO DOIT BOUCLER SUR TOUTE LES PAGES
    dl = page.get_displaylist()
    tp = dl.get_textpage()
    tp_text = tp.extractText()

    ### PARTIE TEXTE BRUT (POUR TEST) ###

    # print(tp_text)
    # print(doc.metadata)

    ### SEPARATEUR ###

    if index != 0:
        print(" ---\n")

    ### PARTIE NOM FICHIER ###

    print("Filename:")
    path = sys.argv[1]
    basename = os.path.basename(path)
    print(file + '\n')

    ### PARTIE TITRE ###

    print("Title:")
    title = doc.metadata["title"]
    patternCorrectTitle = r"/|\\"
    if title == "" or re.search(patternCorrectTitle, title) is not None:
        patternTitle = r"^\A(.*)\n"
        if re.search(patternTitle, tp_text) is not None:
            title = re.search(patternTitle, tp_text).group(0)
            title = txtmanip.spaceandreturn(title)
            print(title + '\n')
        else:
            print("Titre non trouvé !\n")
    else:
        print(title + '\n')

    ### PARTIE AUTEURS ###

    print("Author:")
    author = doc.metadata["author"]
    if author is None or author == "":
        patternAuthors = "([\w.\-]+@[\w.\-]+[.][a-zA-Z]{2,4})"

        if re.search(patternAuthors, tp_text) is not None:
            authors_email = re.findall(patternAuthors, tp_text)
            for author in authors_email:
                email_decompose = author[0:author.find('@')]

                if email_decompose.find('.') != -1:
                    nom = email_decompose[0:email_decompose.find('.')]
                    prenom = email_decompose[email_decompose.find('.') + 1:]
                    print(nom, prenom, "; ", end="")
                else:
                    print(email_decompose, "; ", end="")
            print('\n')

        else:
            patternAuthors = r"^{[\w,\s\-]+}@[\w.\-]+[.][a-zA-Z]{2,4}"
            if re.search(patternAuthors, tp_text, re.MULTILINE) is not None:
                authors_email = re.findall(patternAuthors, tp_text, re.MULTILINE)

                for author in authors_email:
                    email_decompose = author[author.find('{') + 1:author.find('}')]
                    names = re.findall("[\w]+", email_decompose)

                    for name in names:
                        print(name, "; ", end="")
                print('\n')
            else:
                print("Auteurs non trouvés \n")
    else:
        author = txtmanip.spaceandreturn(author)
        print(author,'\n')

    ### PARTIE ABSTRACT ###

    patternAbstract = r"(Abstract(-|.| |\n))\n? ?((.|\n)*)(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
    patternWithoutAbstract = r"(?<=\n)(.|\n)*(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
    print("Abstract:")

    if re.search(patternAbstract, tp_text) is not None:
        abstract = re.search(patternAbstract, tp_text).group(3)
        abstract = txtmanip.spaceandreturn(abstract)
        print(abstract,'\n')

    elif re.search(patternWithoutAbstract, tp_text) is not None :
        abstract = re.search(patternWithoutAbstract, tp_text).group(0)
        abstract = txtmanip.spaceandreturn(abstract)
        print(abstract,'\n')
        
    else:
        print("Abstract non trouvé !\n")

    index+=1