# -*- coding : utf-8 -*-

from math import floor, ceil

class ProgressBar:
    total_index = 0

    def __init__(self, total_index) -> None:
        self.total_index = total_index
        self.mod = self.total_index / 20
        
    def progress(self, index):
        percent = floor((index/self.total_index)*100)
        add = 0
        i = 0
        iv = 0

        # premier cas
        if not index:
            iv = 20
        
        # dernier cas
        elif index == self.total_index:
            i = 20
        
        # tous les cas intermediaires
        else:
            i = ceil(index / self.mod)
            iv = 20-i
            add = 1
            i -= 1
        
        # file%
        #print('\r' + "Progress : [" + i*"■" + add*"◼" + iv*"-" + "] " + str(percent) + "%", end="")

        # file% (file/total)
        print('\r' + "Progress : [" + i*"■" + add*"◼" + iv*"-" + "] " + str(percent) + "% (" + str(index) + "/" + str(self.total_index) + ")", end="")

        # (file/total)
        #print('\r' + "Progress : [" + i*"■" + add*"◼" + iv*"-" + "] (" + str(index) + "/" + str(self.total_index) + ")", end="")
