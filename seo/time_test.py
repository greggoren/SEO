from seo import lambdamart_competition_creator_time_test as l
from model_running import cross_validator as c
import sys
from seo import query_to_fold as qtf
from seo import letor_fold_creator_min_max_normalize as lfc
from scipy import spatial as sp
import cPickle as cp
from copy import copy
import time
import pandas as pd
from math import *
import numpy as np

def square_rooted(x):
    return sqrt(sum([a * a for a in x]))


def cosine_dist(x, y):
    numerator = sum(a * b for a, b in zip(x, y))


    denominator = square_rooted(x) * square_rooted(y)
    return 1-numerator / float(denominator)

if __name__=="__main__":
    a=[[8,8,2],[2,2,3],[8,13,2]]
    arr = np.array(a)
    b=arr.std(axis=0)
    dictionary = dict(enumerate(b,start=1))
    print(dictionary)

    """dict = {'a':2,'b':2,'c':1}
    print sorted(dict,key=lambda x: (dict[x],x),reverse=True)"""
    """A=[1,2,3]
    begin = time.time()
    a,c,v=0,0,0
    for i in range(0,100000):
        a=sp.distance.cosine(A,A)
    print "took ",time.time()-begin
    begin = time.time()
    for i in range(0, 100000):
        c=sp.distance.cdist([A], [A],'cosine')
    print "took ", time.time() - begin
    begin = time.time()
    for i in range(0, 100000):
        v=cosine_dist(A, A)
    print "took ", time.time() - begin
    print a,c,v
    #print sp.distance.cdist(A,B,'cosine')"""
    """k=5
    data_set = ""
    folds_creator = lfc.letor_folds_creator("","",True)
    cv = c.cross_validator(k,folds_creator,data_set)
    tester = l.lambda_mart_competition_time_test(cv)
    models_path = "/lv_local/home/sgregory/LTOR_MART/models/LAMBDAMART"
    final_scores_path = "/lv_local/home/sgregory/LTOR_MART/test_scores_trec_format/LAMBDAMART"
    chosen_mdoels = tester.recover_models_per_fold(models_path,final_scores_path)
    score_file = "/lv_local/home/sgregory/LTOR_MART/test_scores_trec_format/LAMBDAMART/final_score_combined.txt"
    q = qtf.qtf("/lv_local/home/sgregory/final_test")
    q.create_query_to_fold_index()
    competitors = tester.get_competitiors(score_file,10)

    index = tester.index_features_for_competitors(competitors,"/lv_local/home/sgregory/final_test",True)

    tester.rewrite_test_set_for_classification(index,"/lv_local/home/sgregory/time_test/",q.query_to_fold_index)
    tester.testing_times("/lv_local/home/sgregory/time_test/",chosen_mdoels,score_directory="/lv_local/home/sgregory/test_scores")"""