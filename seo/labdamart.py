
from seo import query_to_fold as qtf
from seo import letor_fold_creator_min_max_normalize as lfc
from model_running import cross_validator as cv

import sys

if __name__=="__main__":
    data_set_location = sys.argv[1]
    print data_set_location
    new_data_set_location = sys.argv[2]

    qrel_path = sys.argv[3]
    print qrel_path

    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator(data_set_location,new_data_set_location,True)
    c = cv.cross_validator(5,l,"LTOR_MART")
    c.k_fold_cross_validation("LAMBDAMART",qrel_path)
