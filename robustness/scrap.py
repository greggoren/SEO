import svm_solver as ss
import numpy as np
import preprocess as p
from sklearn.decomposition import PCA

if __name__=="__main__":
    data_set_location = "../../../svm_test"
    prep = p.preprocess(data_set_location)
    a,b=prep.index_features_for_competitors(True)
    X,y = prep.create_data_set_svm_rank(a,b)
    """prep = p.preprocess(data_set_location)
    a,b,c=prep.retrieve_data_from_file(data_set_location)
    X,y = prep.create_data_set(a,b,c)"""
    svm = ss.SVM(C=0.1)
    matrix =np.matrix(X,copy=False)
    """pca = PCA(n_components=5,copy=False,svd_solver='arpack')
    reduced = pca.fit_transform(matrix)
    print pca.explained_variance_ratio_"""
    svm.fit(matrix,np.array(y))

