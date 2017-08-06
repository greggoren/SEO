import svm_solver as ss
import numpy as np
import preprocess as p
if __name__=="__main__":
    data_set_location = "C:/study/svm_test"
    prep = p.preprocess(data_set_location)
    a,b=prep.index_features_for_competitors(True)
    X,y = prep.create_data_set_svm_rank(a,b)
    svm = ss.SVM(C=0.1)
    svm.fit(X,y)
