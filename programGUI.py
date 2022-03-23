from tkinter import *
from tkinter.filedialog import askdirectory

root = Tk()
root.title("PDF Parser")
root.resizable(width=True, height=True)

    ## Actions des bouttons de l'interface ##
# Lance le parser selon les parametres definis par l'utilisateur
def launch():
    # TODO launch
    print("")

def askDirectoryToParse():
    parseFolder = askdirectory()
    butOpenFolder.destroy()
    # TODO creer l'affichage des fichiers pdf du dossier selectionne
    print(parseFolder)

def resetGUIPreset():
    # Parse preset
    checkFilename.select()
    checkTitle.select()
    checkAuthor.select()
    checkAbstract.select()
    checkIntroduction.select()
    checkCorps.select()
    checkConclusion.select()
    checkDiscussion.select()
    checkBiblio.select()

    # Output preset
    valueCheckXmlOrTxt.set(0)


    ## Menu avec choix de langue et de dossier ##
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Folder...", accelerator='ctrl+o', command=askDirectoryToParse)
filemenu.add_command(label="Set Default Preset", command=resetGUIPreset)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="Window", menu=filemenu)

langmenu = Menu(menubar, tearoff=0)
langmenu.add_command(label="Français", command=launch)
langmenu.add_command(label="English", command=resetGUIPreset)

menubar.add_cascade(label="Language", menu=langmenu)

    ## Frame constituee des fichiers pdf ##
fileFrame = LabelFrame(root, text="Files selection", padx=3, pady=3)
fileFrame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

butSelectAll = Button(fileFrame, text="Select all")
butSelectAll.grid(row=0, column=0, padx=3, pady=5)

butUnselectAll = Button(fileFrame, text="Unselect all")
butUnselectAll.grid(row=0, column=1, padx=3, pady=5)

space = Label(fileFrame, text="")
space.grid(row=1, column=2, padx=3, pady=5)

butOpenFolder = Button(fileFrame, text="Open Folder...", command=askDirectoryToParse, bg="#FFF4E5", activebackground='green', activeforeground='white', font=1, borderwidth=2, relief="groove")
butOpenFolder.grid(row=2, column=1, padx=3, pady=5)

    ## Frame constituee des presets pour le parser ##
presetFrame = LabelFrame(root, text="Presets selection", padx=5, pady=5)
presetFrame.grid(row=0, column=1, padx=10, pady=10, sticky=NE)

valueCheckFilemane = IntVar()
checkFilename = Checkbutton(presetFrame, text="Nom du fichier", variable=valueCheckFilemane)
checkFilename.select()
checkFilename.grid(row=0, sticky=W)

valueCheckTitle = IntVar()
checkTitle = Checkbutton(presetFrame, text="Titre de l'article", variable=valueCheckTitle)
checkTitle.select()
checkTitle.grid(row=1, sticky=W)

valueCheckAuthor = IntVar()
checkAuthor = Checkbutton(presetFrame, text="Auteur", variable=valueCheckAuthor)
checkAuthor.select()
checkAuthor.grid(row=2, sticky=W)

valueCheckAbstract = IntVar()
checkAbstract = Checkbutton(presetFrame, text="Abstract", variable=valueCheckAbstract)
checkAbstract.select()
checkAbstract.grid(row=3, sticky=W)

valueCheckIntroduction = IntVar()
checkIntroduction = Checkbutton(presetFrame, text="Introduction", variable=valueCheckIntroduction)
checkIntroduction.select()
checkIntroduction.grid(row=4, sticky=W)

valueCheckCorps = IntVar()
checkCorps = Checkbutton(presetFrame, text="Corps", variable=valueCheckCorps)
checkCorps.select()
checkCorps.grid(row=5, sticky=W)

valueCheckConclusion = IntVar()
checkConclusion = Checkbutton(presetFrame, text="Conclusion", variable=valueCheckConclusion)
checkConclusion.select()
checkConclusion.grid(row=6, sticky=W)

valueCheckDiscussion = IntVar()
checkDiscussion = Checkbutton(presetFrame, text="Discussion", variable=valueCheckDiscussion)
checkDiscussion.select()
checkDiscussion.grid(row=7, sticky=W)

valueCheckBiblio = IntVar()
checkBiblio = Checkbutton(presetFrame, text="Bibliographie", variable=valueCheckBiblio)
checkBiblio.select()
checkBiblio.grid(row=8, sticky=W)


    ## Lancement du programme ##
launchFrame = Frame(root, padx=2, pady=2)
launchFrame.grid(row=1, column=0, sticky=SW)

valueCheckXmlOrTxt = IntVar()

Radiobutton(launchFrame, text="Format XML", variable=valueCheckXmlOrTxt, value=0).grid(row=0, column=0)
Radiobutton(launchFrame, text="Format TXT", variable=valueCheckXmlOrTxt, value=1).grid(row=0, column=1)

butLaunch = Button(launchFrame, text="Start parsing", command=launch)
butLaunch.grid(row=0, column=2)


    ## Zone de retour, message d'erreur ##
labError = Label(root, text="")
labError.grid(row=1, column=1, sticky=SE)


root.config(menu=menubar)
root.mainloop()