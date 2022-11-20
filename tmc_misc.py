
def getFileSizeString(size):
    
    if size < 1000:
        return "%dB" % ( size, )
    
    if size < 1000*1024:
        s = "%.1fK" % ( size / float(1024), )
        if len(s)<=6 : return s

    if size < 1000*1024*1024:
        s = "%.1fM" % ( size / float(1024*1024), )
        if len(s)<=6 : return s

    if size < 1000*1024*1024*1024:
        s = "%.1fG" % ( size / float(1024*1024*1024), )
        if len(s)<=6 : return s
    
    return "%.1fT" % ( size / float(1024*1024*1024*1024), )
