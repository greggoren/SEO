import os
if __name__ == "__main__":
    qrels = open("./qrels",'w')
    for dirs in os.walk("C:/study/letor_fixed"):
        if dirs[1]:
            dir = dirs[0]+"/"+dirs[1][0]
            for files in os.walk(dir):
                for file in files[2]:
                    file_name = dir+"/"+file
                    with open(file_name) as data_set:
                        for data_record in data_set:
                            splited = data_record.split()
                            length = len(splited)
                            qid = splited[1].split(":")[1]
                            doc = splited[length-1]
                            relevance = splited[0]
                            qrels.write(qid+" "+"0 "+doc+" "+relevance+"\n")
            qrels.close()