import gini_index_calculator as g
from bs4 import BeautifulSoup
from numpy import hstack
from numpy import matrix
import pandas as pd

def xml2df(xml_doc):
    f = open(xml_doc, 'r')
    soup = BeautifulSoup(f,"lxml")

    name_list=[]
    text_list=[]
    attr_list=[]

    def recurs(soup):
        try:
            for j in soup.contents:
                try:
                    #print j.name
                    if j.name!=None:
                        name_list.append(j.name)
                except:
                    pass
                try:
                    #print j.text
                    if j.name!=None:
                        #print j.string
                        text_list.append(j.string)
                except:
                    pass
                try:
                    #print j.attrs
                    if j.name!=None:
                        attr_list.append(j.attrs)
                except:
                    pass
                recurs(j)
        except:
            pass

    recurs(soup)

    attr_names_list = [q.keys() for q in attr_list]
    attr_values_list = [q.values() for q in attr_list]

    columns = hstack((hstack(name_list),
                      hstack(attr_names_list)) )
    data = hstack((hstack(text_list),
                   hstack(attr_values_list)) )

    df = pd.DataFrame(data=matrix(data.T), columns=columns )

    return df


if __name__=="__main__":
    gini = g.gini()
    gini.parse_file("C:/study/simulation_data/test/model_500_5.txt.txt")
