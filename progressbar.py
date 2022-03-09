from math import floor

class ProgressBar:
    total_index = 0
    mod = 0

    def __init__(self, total_index) -> None:
        self.total_index = total_index
        self.mod = self.total_index/20
        
    def progress(self, index):
        #percent = floor((index/self.total_index)*100)

        i = floor(index%self.mod)
        iv = 20-i
        add = 1

        if index == 0 or index == self.total_index:
            add = 0

        #print('\r' + "Progress : [" + (i-1)*"■" + add*"◼" + iv*"-" + "] " + str(percent) + "% (" + str(index) + "/" + str(self.total_index) + ")", end="")
        print('\r' + "Progress : [" + (i-1)*"■" + add*"◼" + iv*"-" + "] " " (" + str(index) + "/" + str(self.total_index) + ")", end="")
