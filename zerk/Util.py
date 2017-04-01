def prettyList(tok, conj = "and"):
    if len(tok) < 2:
        return tok
    else:
        return ', '.join(tok[:-1]) + (' %s %s' % (conj, tok[-1]))
