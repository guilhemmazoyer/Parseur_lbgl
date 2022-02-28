from lib2to3.pgen2.token import EQUAL
import fitz, re, sys, os
import textmanipulation as txtmanip
import shutil

# Ouverture fichiers pdf dans repertoire
files = os.listdir(sys.argv[1])
files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)

# Creation du sous-dossier ou deposer les fichiers textes
res_folder_path = sys.argv[1] + "\\result"
if os.path.isdir(res_folder_path):
    shutil.rmtree(res_folder_path)
os.mkdir(res_folder_path)

for file in files:
    # ouverture du fichier .pdf
    doc = fitz.open(sys.argv[1] + '/' + file)

    page = doc.load_page(0)  # Lecture de la premiere page TODO DOIT BOUCLER SUR TOUTE LES PAGES
    dl = page.get_displaylist()
    tp = dl.get_textpage()
    tp_text = tp.extractText()

    ### PARTIE TEXTE BRUT (POUR TEST) ###

    # print(tp_text)
    # print(doc.metadata)

    ### PARTIE NOM FICHIER ###

    # recuperation du nom du fichier pdf
    filename_display = "Filename:\n"
    file_basename = os.path.basename(sys.argv[1] + '\\' + file)
    filename_display += file_basename + '\n' + '\n'

    # transformation du nom pour le futur fichier texte
    txt_basename = file_basename[0:file_basename.find('.')]

    ### PARTIE TITRE ###

    title_display = "Title:\n"
    title = doc.metadata["title"]
    patternCorrectTitle = r"/|\\"
    if title == "" or re.search(patternCorrectTitle, title) is not None:
        patternTitle = r"^\A(.*)\n"
        if re.search(patternTitle, tp_text) is not None:
            title = re.search(patternTitle, tp_text).group(0)
            title = txtmanip.spaceandreturn(title)
            title_display += title + '\n' + '\n'
        else:
            title_display += "Titre non trouvé !\n\n"
    else:
        title_display += title + '\n' + '\n'

    ### PARTIE AUTEURS ###

    author_display = "Author:\n"
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
                    author_display += nom + prenom + "; "
                else:
                    author_display += email_decompose + "; "

        else:
            patternAuthors = r"^{[\w,\s\-]+}@[\w.\-]+[.][a-zA-Z]{2,4}"
            if re.search(patternAuthors, tp_text, re.MULTILINE) is not None:
                authors_email = re.findall(patternAuthors, tp_text, re.MULTILINE)

                for author in authors_email:
                    email_decompose = author[author.find('{') + 1:author.find('}')]
                    names = re.findall("[\w]+", email_decompose)

                    for name in names:
                        author_display += name + "; "
            else:
                author_display += "Auteurs non trouvés"
    else:
        author = txtmanip.spaceandreturn(author)
        author_display += author
    author_display += "\n\n"

    ### PARTIE ABSTRACT ###

    patternAbstract = r"(Abstract(-|.| |\n))\n? ?((.|\n)*)(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
    patternWithoutAbstract = r"(?<=\n)(.|\n)*(?=(1(\n| |( \n)|. )Introduction)|(I. INTRODUCTION))"
    abstract_display = "Abstract:\n"

    if re.search(patternAbstract, tp_text) is not None:
        abstract = re.search(patternAbstract, tp_text).group(3)
        abstract = txtmanip.spaceandreturn(abstract)
        abstract_display += abstract

    elif re.search(patternWithoutAbstract, tp_text) is not None :
        abstract = re.search(patternWithoutAbstract, tp_text).group(0)
        abstract = txtmanip.spaceandreturn(abstract)
        abstract_display += abstract
        
    else:
        abstract_display += "Abstract non trouvé !"

    # creation et ouverture du fichier .txt
    txtFileToFill = open(res_folder_path + '\\' + txt_basename + ".txt", "w+")

    # ecriture du nom du fichier, du titre, des auteurs et de l'abstract
    txtFileToFill.write(filename_display)
    txtFileToFill.write(title_display)
    txtFileToFill.write(author_display)
    txtFileToFill.write(abstract_display)

    # fermeture du fichier
    txtFileToFill.close()
