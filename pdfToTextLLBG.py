import fitz,re,sys,os

# Ouverture fichiers pdf dans repertoire
files = os.listdir(sys.argv[1])
files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)

for file in files:
    doc = fitz.open(sys.argv[1]+ '/'+file)

    page = doc.load_page(0) # Lecture de la premiere page TODO DOIT BOUCLER SUR TOUTE LES PAGES
    dl = page.get_displaylist()
    tp = dl.get_textpage()
    tp_text = tp.extractText()

    ### PARTIE TEXTE BRUT (POUR TEST) ###

    #print(tp_text)
    #print(doc.metadata)

    ### PARTIE NOM FICHIER ###

    print("Filename:")
    path = sys.argv[1]
    basename = os.path.basename(path)
    print(file+'\n')

    ### PARTIE TITRE ###

    print("Title:")
    title = doc.metadata["title"]
    if title == "":
        patternTitle = "^\A(.*)$"
        title = re.search(patternTitle, tp_text)
    print(title)

    ### PARTIE AUTEURS ###

    print("Author:")
    print(doc.metadata["author"] + '\n')

    ### PARTIE ABSTRACT ###

    patternAbstract = "(Abstract(-|.|\n))((.|\n)*)(?=(1(\n| )Introduction)|(I. INTRODUCTION))"

    print("Abstract:")
    if re.search(patternAbstract, tp_text) != None:
        abstract = re.search(patternAbstract, tp_text).group(3)
        print(abstract)
        print('\n')
    else:
        print("Abstract non trouvé !\n\n")