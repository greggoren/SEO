if __name__=="__main__":
    lists = [[1,2,3],[1,1,1],[0,2,34]]
    res = [sum(i) for i in zip(*lists)]
    print res