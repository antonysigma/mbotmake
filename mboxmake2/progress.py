import progressbar as pbar


def newProgressBar(maxval: int) -> pbar.ProgressBar:
    return pbar.ProgressBar(maxval=maxval)
