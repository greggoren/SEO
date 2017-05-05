import os
import sys

from model_running import cross_validator as cv

if __name__=="__main__":
    model = sys.argv[1]#user's input of model
    if model!="LAMBDAMART" and model!="SVM":
        print("please insert correct model to run")
        sys.exit(1)
    featues_file = sys.argv[2]
    if not os.path.exists(featues_file):
        print("please insert correct path to train file")
        sys.exit(1)
    query_relevance_file = sys.argv[3]
    if not os.path.exists(query_relevance_file):
        print("please insert correct path to relevance file")
        sys.exit(1)
    data_set = sys.argv[4]
    cross_validator = cv.cross_validator(5,featues_file,data_set,200)#TODO: maybe add user input params for more generality
    cross_validator.k_fold_cross_validation(model, query_relevance_file)
