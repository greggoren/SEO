if __name__=="__main__":
    a = set()
    if a:
        print "I dont know what to do anymore...."
    else:
        print "ok make sense"


    a = set([1,2,3,4])
    b = set([4,5,6,7])
    c = a.intersection(b)
    print c

    if not c:
        print "shit..."
    else:
        print "ok..."