from settings import ITEM_PER_PAGE
def pagerget(el,pageindex):
    '''get the items to show in page.
    el: the list of items to show.
    pageindex: the index of current page.'''
    N=len(el)
    totalpages=(N-1)/ITEM_PER_PAGE+1
    if N>pageindex*ITEM_PER_PAGE:
        el20=el[(pageindex-1)*ITEM_PER_PAGE:pageindex*ITEM_PER_PAGE]
        return el20,totalpages
    elif N>(pageindex-1)*ITEM_PER_PAGE:
        el20=el[(pageindex-1)*ITEM_PER_PAGE:]
        return el20,totalpages
    else:
        return None,0
