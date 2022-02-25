import fitz,re,sys,os

doc = fitz.open(sys.argv[1])

page = doc.load_page(0) # Lecture de la premiere page TODO DOIT BOUCLER SUR TOUTE LES PAGES
dl = page.get_displaylist()
tp = dl.get_textpage()
tp_text = tp.extractText()

### PARTIE TEXTE BRUT ###

print(tp_text)
#print(doc.metadata)

### PARTIE NOM FICHIER ###

print("Filename:")
path = sys.argv[1]
basename = os.path.basename(path)
print(basename+"\n")

### PARTIE TITRE (torres moreno)###

print("Title:")
title = doc.metadata["title"]
#if title == "":
    #patternTitle = "^\A(.*)$"
    #title = re.search(patternTitle, tp_text).group(1)
print(title)

### PARTIE AUTEURS ###

print("Author:")
print(doc.metadata["author"]+"\n")

### PARTIE ABSTRACT ###

patternAbstract = "Abstract\n((.|\n)*)(?=1\nIntroduction)"

print("Abstract:")
result = re.search(patternAbstract, tp_text).group(1)
print(result+"\n")
