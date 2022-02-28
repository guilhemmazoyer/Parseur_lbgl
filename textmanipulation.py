def spaceandreturn(texttochange):
    texttochange = texttochange.replace('\n', ' ')
    texttochange = texttochange.replace("  ", ' ')
    texttochange = texttochange.replace("- ", '')
    return texttochange