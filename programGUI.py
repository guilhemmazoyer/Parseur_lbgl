from faulthandler import disable
from tkinter import *
from tkinter.filedialog import askdirectory
from language.lang import lang
from language.lang import *

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
    if parseFolder != "":
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

def updateLanguageDisplay():
    ## Menus
    menubar.entryconfig(index=1, label=MENU_FILES_TITLE[lang.LANG])
    filemenu.entryconfig(index=0, label=MENU_FILES_OPEN_FOLDER[lang.LANG])
    filemenu.entryconfig(index=1, label=MENU_FILES_SET_DEFAULT_PRESEST[lang.LANG])
    filemenu.entryconfig(index=3, label=MENU_FILES_EXIT[lang.LANG])
    menubar.entryconfig(index=2, label=MENU_LANGUAGE_TITLE[lang.LANG])

    ## File Selection
    fileFrame.config(text=LABELFRAME_FILE_SELECTION[lang.LANG])
    butSelectAll.config(text=BUTTON_SELECT_ALL[lang.LANG])
    butUnselectAll.config(text=BUTTON_UNSELECT_ALL[lang.LANG])
    butOpenFolder.config(text=MENU_FILES_OPEN_FOLDER[lang.LANG])

    ## Presets
    presetFrame.config(text=LABELFRAME_PRESETS_SELECTION[lang.LANG])
    checkFilename.config(text=CHECK_FILENAME[lang.LANG])
    checkTitle.config(text=CHECK_TITLE[lang.LANG])
    checkAuthor.config(text=CHECK_AUTHOR[lang.LANG])
    checkAbstract.config(text=CHECK_ABSTRACT[lang.LANG])
    checkIntroduction.config(text=CHECK_INTRODUCTION[lang.LANG])
    checkCorps.config(text=CHECK_CORPS[lang.LANG])
    checkConclusion.config(text=CHECK_CONCLUSION[lang.LANG])
    checkDiscussion.config(text=CHECK_DISCUSSION[lang.LANG])
    checkBiblio.config(text=CHECK_REFERENCES[lang.LANG])

    ## Others UI Elements
    radXMLFormat.config(text=RADIO_XML_FORMAT[lang.LANG])
    radTXTFormat.config(text=RADIO_TXT_FORMAT[lang.LANG])
    butLaunch.config(text=BUTTON_LAUNCH_PARSING[lang.LANG])

def changeToEnglish():
    lang.LANG = 0
    updateLanguageDisplay()

def changeToFrench():
    lang.LANG = 1
    updateLanguageDisplay()

    ## Menu avec choix de langue et de dossier ##
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(accelerator='ctrl+o', command=askDirectoryToParse)
filemenu.add_command(command=resetGUIPreset)
filemenu.add_separator()
filemenu.add_command(command=root.quit)

menubar.add_cascade(menu=filemenu)

langmenu = Menu(menubar, tearoff=0)
langmenu.add_command(label="English", command=changeToEnglish)
langmenu.add_command(label="Français", command=changeToFrench)

menubar.add_cascade(menu=langmenu)

    ## Frame constituee des fichiers pdf ##
fileFrame = LabelFrame(root, padx=3, pady=3)
fileFrame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

butSelectAll = Button(fileFrame)
butSelectAll.grid(row=0, column=0, padx=3, pady=5)

butUnselectAll = Button(fileFrame)
butUnselectAll.grid(row=0, column=1, padx=3, pady=5)

space = Label(fileFrame, text="")
space.grid(row=1, column=2, padx=3, pady=5)

butOpenFolder = Button(fileFrame, command=askDirectoryToParse, bg="#FFF4E5", activebackground='green', activeforeground='white', font=1, borderwidth=2, relief="groove")
butOpenFolder.grid(row=2, column=1, padx=3, pady=5)

    ## Frame constituee des presets pour le parser ##
presetFrame = LabelFrame(root, padx=5, pady=5)
presetFrame.grid(row=0, column=1, padx=10, pady=10, sticky=NE)

valueCheckFilemane = IntVar()
checkFilename = Checkbutton(presetFrame, variable=valueCheckFilemane)
checkFilename.select()
checkFilename.grid(row=0, sticky=W)

valueCheckTitle = IntVar()
checkTitle = Checkbutton(presetFrame, variable=valueCheckTitle)
checkTitle.select()
checkTitle.grid(row=1, sticky=W)

valueCheckAuthor = IntVar()
checkAuthor = Checkbutton(presetFrame, variable=valueCheckAuthor)
checkAuthor.select()
checkAuthor.grid(row=2, sticky=W)

valueCheckAbstract = IntVar()
checkAbstract = Checkbutton(presetFrame, variable=valueCheckAbstract)
checkAbstract.select()
checkAbstract.grid(row=3, sticky=W)

valueCheckIntroduction = IntVar()
checkIntroduction = Checkbutton(presetFrame, variable=valueCheckIntroduction)
checkIntroduction.select()
checkIntroduction.grid(row=4, sticky=W)

valueCheckCorps = IntVar()
checkCorps = Checkbutton(presetFrame, variable=valueCheckCorps)
checkCorps.select()
checkCorps.grid(row=5, sticky=W)

valueCheckConclusion = IntVar()
checkConclusion = Checkbutton(presetFrame, variable=valueCheckConclusion)
checkConclusion.select()
checkConclusion.grid(row=6, sticky=W)

valueCheckDiscussion = IntVar()
checkDiscussion = Checkbutton(presetFrame, variable=valueCheckDiscussion)
checkDiscussion.select()
checkDiscussion.grid(row=7, sticky=W)

valueCheckBiblio = IntVar()
checkBiblio = Checkbutton(presetFrame, variable=valueCheckBiblio)
checkBiblio.select()
checkBiblio.grid(row=8, sticky=W)


    ## Lancement du programme ##
launchFrame = Frame(root, padx=2, pady=2)
launchFrame.grid(row=1, column=0, sticky=SW)

valueCheckXmlOrTxt = IntVar()

radXMLFormat = Radiobutton(launchFrame, variable=valueCheckXmlOrTxt, value=0)
radXMLFormat.grid(row=0, column=0)
radTXTFormat = Radiobutton(launchFrame, variable=valueCheckXmlOrTxt, value=1)
radTXTFormat.grid(row=0, column=1)

butLaunch = Button(launchFrame, command=launch)
butLaunch.grid(row=0, column=2)


    ## Zone de retour, message d'erreur ##
labError = Label(root, text="")
labError.grid(row=1, column=1, sticky=SE)


root.config(menu=menubar)

updateLanguageDisplay();

root.mainloop()