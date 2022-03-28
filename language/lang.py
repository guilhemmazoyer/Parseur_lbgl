from tkinter import *

# Ce fichier contient tous les noms et les traductions des éléments du GUI
# Les noms sont écris sous la forme :
# varname = ["english", "français", "日本語"]

    ## Accelerators
MENU_FILES_OPEN_FOLDER_A = "Ctrl+O"

    ## Menus
MENU_FILES_OPEN_FOLDER = ["Open Folder...", "Ouvrir un Dossier...", "フォルダーを開く"]
MENU_FILES_SET_DEFAULT_PRESEST = ["Set Default Presets", "Appliquer les paramètres par défaut", "デフォルト・プリセットを設定する"]
MENU_FILES_EXIT = ["Exit", "Quitter", "終了"]
MENU_FILES_TITLE = ["File", "Fichier", "ファイル"]
MENU_LANGUAGE_TITLE = ["Language", "Langue", "言語"]

    ## File Selection
LABELFRAME_FILE_SELECTION = ["Files selection", "Sélection des fichiers", "ファイル選択"]
BUTTON_SELECT_ALL = ["Select all", "Tout sélectionner", "すべて選択"]
BUTTON_UNSELECT_ALL = ["Unselect all", "Tout désélectionner", "すべて選択解除"]

    ## Presets
LABELFRAME_PRESETS_SELECTION = ["Presets selection", "Sélection des paramètres", "プリセット選択"]
CHECK_FILENAME = ["File name", "Nom du fichier", "ファイル名"]
CHECK_TITLE = ["Title", "Titre", "タイトル"]
CHECK_AUTHOR = ["Authors", "Auteurs", "著者紹介"]
CHECK_ABSTRACT = ["Abstract", "Abstract", "概要"]
CHECK_INTRODUCTION = ["Introduction", "Introduction", "イントロダクション"]
CHECK_CORPS = ["Corps", "Corps", "隊"]
CHECK_CONCLUSION = ["Conclusion", "Conclusion", "結論"]
CHECK_DISCUSSION = ["Discussion", "Discussion", "談義"]
CHECK_REFERENCES = ["Reference", "Bibliographie", "書誌情報"]

    ## Others UI Elements
RADIO_XML_FORMAT = ["XML Format", "Format XML", "XML フォーマット"]
RADIO_TXT_FORMAT = ["TXT Format", "Format TXT", "TXT フォーマット"]
BUTTON_LAUNCH_PARSING = ["Start parsing", "Lancement de l'analyse", "パース開始"]

class lang:

    global langOption
    langOption = IntVar()
    langOption.set(0)
    LANG = 0    

    def __init__(self) -> None:
        pass