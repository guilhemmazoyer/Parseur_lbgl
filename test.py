from progressbar import ProgressBar as pbar

big = 500
index = 49
pbar.__init__(pbar, big)
pbar.progress(pbar, index)