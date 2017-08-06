import os
import numpy as np
import itertools
from sklearn.datasets import load_svmlight_file


class preprocess:



    def __init__(self,data_set_location):
        self.data_set_location = data_set_location

    def index_features_for_competitors(self,normalized):
        feature_index_query = {}
        labels_index = {}
        print "features index creation started"
        amount = 0
        if (normalized):
            amount = 1
        label_index =0
        for dirs in os.walk(self.data_set_location):
            if dirs[1]:
                first_directory = dirs[0]+"/"+dirs[1][0]
                for files in os.walk(first_directory):
                    for file_name in files[2]:
                        current_file = files[0]+"/"+file_name
                        with open(current_file) as features:
                            for feature in features:

                                feature_data = feature.split()
                                qid = feature_data[1]
                                if not feature_index_query.get(qid,False):
                                    feature_index_query[qid]=[]
                                    label_index = 0
                                    labels_index[qid]={}
                                features_length = len(feature_data)
                                features_vec = []
                                for index in range(2, features_length - 1 - amount):
                                    data = feature_data[index]
                                    features_vec.append(float(data.split(":")[1]))
                                labels_index[qid][label_index]=int(feature_data[0])
                                label_index+=1
                                feature_index_query[qid].append(np.array(features_vec))
            print "feature index creation ended"
            return feature_index_query,labels_index

    def retrieve_data_from_file(self,file):
        X, y, groups= load_svmlight_file(file,query_id=True)
        return X,y,groups

    def create_data_set(self,X,y,groups):
        print "creating data set"
        data = []
        labels = []
        k=0
        comb = itertools.combinations(range(X.shape[0]), 2)
        for (i,j) in comb:
            if (y[i]==y[j]) or (groups[i]!=groups[j]):
                continue
            data.append(X[i]-X[j])
            labels.append(np.sign(y[i]-y[j]))
            if labels[-1] != (-1) ** k:
                labels[-1] *= -1
                data[-1] *= -1
            k += 1
        return data,labels


    def create_data_set_svm_rank(self,feature_index_query,labels_index):
        print "data set creation started",
        k=0
        data_set=[]
        labels = []
        for qid in feature_index_query:
            print "working on ",qid
            comb = itertools.combinations(range(len(feature_index_query[qid])), 2)
            for (i,j) in comb:
                if labels_index[qid][i]==labels_index[qid][j]:
                    continue
                data_set.append(feature_index_query[qid][i]-feature_index_query[qid][j])
                labels.append(np.sign(labels_index[qid][i]-labels_index[qid][j]))
                if labels[-1]!= (-1) ** k:
                    labels[-1]*=-1
                    data_set[-1]*=-1
                k+=1
        print "data set creation ended"
        del(feature_index_query)
        return data_set,labels


