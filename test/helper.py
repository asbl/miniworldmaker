import imgcompare

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage