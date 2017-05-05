from model_running import folds_creator as fc
import os
from seo import query_to_fold as qtf

class letor_folds_creator(fc.folds_creator):
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

                                for index in range(2, length_of_features):
                                    feature = splited_record[index].split(":")[0]
                                    feature_value = splited_record[index].split(":")[1]
                                    if not feature_index.get(feature, False):
                                        feature_index[feature] = {}
                                        feature_index[feature]["min"] = feature_value
                                        feature_index[feature]["max"] = feature_value
                                    else:
                                        if float(feature_value) > float(feature_index[feature]["max"]):
                                            feature_index[feature]["max"] = feature_value
                                        elif float(feature_value) < float(feature_index[feature]["min"]):
                                            feature_index[feature]["min"] = feature_value
                    return feature_index,length_of_features,query_doc_name_index



    def get(self,feature_index,length_of_features,query_doc_index):
        queries_seen = {}
        final_file_name = os.path.basename(self.train_file)
        file_name = os.path.basename(self.train_file).replace("txt","tmp")

        fold =os.path.basename(os.path.dirname(self.train_file))
        train_file_folder = self.new_features_path+"/"+fold
        if not os.path.exists(train_file_folder):
            os.makedirs(train_file_folder)
        new_feature_file = open(train_file_folder + "/"+file_name, 'w')
        with open(self.train_file) as train_data:
            for train_record in train_data:
                new_record = ""
                train_record_splitted = train_record.split()
                qid = train_record_splitted[1].split(":")[1]
                if not queries_seen.get(qid,False):
                    queries_seen[qid]=0
                index = queries_seen[qid]
                doc_generated_name = query_doc_index[qid][index]
                queries_seen[qid]=index+1
                new_record += train_record_splitted[0] + " " + train_record_splitted[1] + " "
                for index in range(2, length_of_features):
                    feature = train_record_splitted[index].split(":")[0]
                    feature_value = train_record_splitted[index].split(":")[1]
                    new_value = self.change_to_normalized_value(feature_index, feature, feature_value)
                    new_record += str(feature) + ":" + str(new_value) + " "

                new_record += "# "+doc_generated_name+"\n"
                new_feature_file.write(new_record)
            new_feature_file.close()
            command = "sort -t ':' -nk 2,2 "  +train_file_folder + "/"+file_name+ ">" + train_file_folder + "/"+final_file_name
            for line in self.run_command(command):
                print line
            os.remove(train_file_folder + "/"+file_name)


    def split_train_file_into_folds(self):
        if not self.recovery_flag:
            self.normalize_and_write_files()
