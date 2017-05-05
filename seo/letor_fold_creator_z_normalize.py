import letor_fold_creator_min_max_normalize as lfcmnn
import os
import numpy as np

class letor_folds_creator_z_normalize(lfcmnn.letor_folds_creator):
    def __init__(self,features_path,new_features_path,recovery_flag):
        self.new_features_path = new_features_path
        self.working_path = new_features_path
        self.features_path = features_path
        self.recovery_flag = recovery_flag

    def normalize_and_write_files(self):
        feature_index = {}
        length_of_features = 0
        query_doc_index = {}
        for dir in os.walk(self.features_path):
            print(dir)
            if not dir[1]:
                for file_name in dir[2]:
                    self.train_file = dir[0]+"/"+file_name
                    if not feature_index:
                        feature_index,length_of_features,query_doc_index = self.create_features_stats()
                    self.get(feature_index,length_of_features,query_doc_index)

    def create_features_stats(self):
        feature_index = {}
        queries_seen ={}
        query_doc_name_index = {}
        all_data_set = []
        for dirs in os.walk(self.features_path):
            if dirs[1]:
                data_dir =dirs[0]+"/"+dirs[1][0]
                for files in os.walk(data_dir):
                    for file_name in files[2]:
                        length_of_features = 0
                        with open(files[0]+"/"+file_name) as train_data:
                            for train_record in train_data:

                                splited_record = train_record.split()
                                if length_of_features == 0:
                                    length_of_features = len(splited_record)
                                qid = splited_record[1].split(":")[1]
                                if not query_doc_name_index.get(qid,False):
                                    query_doc_name_index[qid]={}
                                    queries_seen[qid]=0
                                index = queries_seen[qid]
                                query_doc_name_index[qid][index] = qid+"_"+str(index)
                                queries_seen[qid] = index + 1
                                feature_vec =[]
                                for index in range(2, length_of_features):
                                    feature_value = splited_record[index].split(":")[1]
                                    feature_vec.append(feature_value)
                                all_data_set.append(feature_vec)
        data_set = np.array(all_data_set).astype(np.float)
        variance_vector = list(data_set.std(axis=0))
        mean_vector = list(data_set.mean(axis=0))
        feature_index["variance"] = dict(enumerate(variance_vector,start=1))
        feature_index["mean"] = dict(enumerate(mean_vector,start=1))
        return feature_index,length_of_features,query_doc_name_index


    def change_to_normalized_value(self, feature_index, feature, old_feature_value):
        new_feature_value = 0.0
        if feature_index["variance"][int(feature)] != 0:
            new_feature_value = float(float(old_feature_value) - float(feature_index["mean"][int(feature)]))/float(feature_index["variance"][int(feature)])
        else:
            print "ohhhhhh nooooooooo var = 0"
        return new_feature_value