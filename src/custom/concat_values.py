def concat_values(mylist):
    value = mylist[0]["value"]
    if len(mylist) > 1:
        for elmt in mylist:
            value = value + " - " + elmt["value"]
    return value