from math import floor

def progress(index, total_index):
    percent = floor((index/total_index)*100)
    i = percent%5
    iv = 20-i
    add = 1

    if index == 0 or index == total_index:
        add = 0

    print('\r' + "Progress : [" + ("■")*i-1 + ("◼")*add + ("-")*iv + "] " + str(percent) + "%", end="")