import math
import os
import time
import subprocess

class folds_creator:
    def __init__(self,k=5,train_file="", number_of_queries=-1,fold_prefix="fold"):
        self.k = k
        self.train_file = train_file
        self.number_of_queries = number_of_queries
        self.fold_prefix = fold_prefix
        self.folds = {}
        self.working_path = ""

    def normalize_training_file(self):#TODO: make function more generic - to fit each data set
        amount = 2
        feature_index = {}
        length_of_features = 0
        with open(self.train_file) as train_data:
            for train_record in train_data:
                splited_record = train_record.split()
                if length_of_features == 0:
                    length_of_features = len(splited_record)
                for index in range(2,length_of_features-amount):
                    feature = splited_record[index].split(":")[0]
                    feature_value = splited_record[index].split(":")[1]
                    if not feature_index.get(feature,False):
                        feature_index[feature] = {}
                        feature_index[feature]["min"] = feature_value
                        feature_index[feature]["max"] = feature_value
                    else:
                        if float(feature_value) > float(feature_index[feature]["max"]):
                            feature_index[feature]["max"]  = feature_value
                        elif float(feature_value) < float(feature_index[feature]["min"]):
                            feature_index[feature]["min"] = feature_value
            self.get(feature_index,length_of_features)

    def get(self,feature_index,length_of_features):
        train_file_folder = os.path.dirname(os.path.dirname(__file__))
        new_feature_file = open(train_file_folder + "/normalized_features", 'w')
        with open(self.train_file) as train_data:
            for train_record in train_data:

                new_record = ""
                train_record_splitted = train_record.split()
                new_record += train_record_splitted[0] + " " + train_record_splitted[1] + " "
                for index in range(2, length_of_features-2):
                    feature = train_record_splitted[index].split(":")[0]
                    feature_value = train_record_splitted[index].split(":")[1]
                    new_value = self.change_to_normalized_value(feature_index, feature, feature_value)
                    new_record += str(feature) + ":" + str(new_value) + " "
                new_record += train_record_splitted[length_of_features-2]+" "+train_record_splitted[length_of_features-1]+ "\n"
                new_feature_file.write(new_record)
            new_feature_file.close()
            self.train_file = train_file_folder + "/normalized_features"


    def change_to_normalized_value(self,feature_index,feature, old_feature_value):
        new_feature_value = 0.0
        if feature_index[feature]['min'] != feature_index[feature]['max']:
            new_feature_value = ((float(old_feature_value) - float(feature_index[feature]['min']))/(float(feature_index[feature]['max']) - float(feature_index[feature]['min'])))
        return new_feature_value




    def init_files(self, number_of_queries_in_fold):

        query_to_fold = {}
        fold_number = 1
        current_number_of_queries = 0
        for query_number in range(1,self.number_of_queries+1):

            if current_number_of_queries >= number_of_queries_in_fold:
                fold_number += 1
                current_number_of_queries=0

            query_to_fold[query_number] = self.fold_prefix + str(fold_number)
            current_number_of_queries += 1

        return query_to_fold


    def go_over_train_file_and_split_to_folds(self, query_to_fold):
        absolute_path = os.path.abspath(self.train_file)
        folds = {}
        with open(absolute_path) as train_set:
            for doc in train_set:
                features = doc.split(" ")
                query_number = features[1].split(":")[1]
                query_number = int(query_number)
                fold_name = query_to_fold[query_number]
                if not folds.get(fold_name,False):
                    folds[fold_name] =[]
                folds[fold_name].append(doc)

        return folds

    def create_folds_splited_into_folders(self):
        print("starting working set creation")
        path = os.path.dirname(__file__)
        parent_path = os.path.abspath(os.path.join(path, os.pardir))
        #if not os.path.exists(parent_path + "/working_sets"):
         #   os.makedirs(parent_path + "/working_sets")
        self.working_path = parent_path+"/working_sets"+str(time.time())+"/"

        for fold in range(2,self.k+1):
            self.create_files_in_working_folder(fold,fold-1,self.working_path)
        self.create_files_in_working_folder(1,self.k,self.working_path)
        print("working set creation is done")


    def create_files_in_working_folder(self,test_fold,validation_fold,path):
        if not os.path.exists(path+"fold"+str(test_fold)):
            os.makedirs(path+"fold"+str(test_fold))
        print("creating fold"+str(test_fold))
        not_train = [self.fold_prefix+str(test_fold),self.fold_prefix+str(validation_fold)]
        train_set = []
        for fold in self.folds:
            if fold not in not_train:
                print(fold)
                train_set.extend(self.folds[fold])

        train_path = os.path.abspath(path+"fold"+str(test_fold)+"/"+ "train.tmp")
        train_for_ltr = open(train_path, 'w')
        for train_data in train_set:
            train_for_ltr.write("%s" % train_data)
        train_for_ltr.close()
        command = "sort -k2 "+path+"fold"+str(test_fold)+"/"+ "train.tmp > "+path+"fold"+str(test_fold)+"/"+ "train.txt"
        for output_line in self.run_command(command):
            print (output_line)
        if os.path.exists(path + "fold" + str(test_fold) + "/" + "train.tmp"):
            os.remove(path + "fold" + str(test_fold) + "/" + "train.tmp")
        print("finished train.txt")

        validation_path = os.path.abspath(path+"fold"+str(test_fold)+"/"+ "validation.tmp")
        validation_file = open(validation_path,'w')
        validation_set = self.folds[self.fold_prefix+str(validation_fold)]
        for validation_data in validation_set:
            validation_file.write("%s" % validation_data)
        validation_file.close()
        command = "sort -k2 " + path + "fold" + str(test_fold) + "/" + "validation.tmp > " + path + "fold" + str(test_fold) + "/" + "validation.txt"
        for output_line in self.run_command(command):
            print (output_line)
        if os.path.exists(path + "fold" + str(test_fold) + "/" + "validation.tmp"):
            os.remove(path + "fold" + str(test_fold) + "/" + "validation.tmp")
        print("finished validation.txt")

        test_path = os.path.abspath(path+"fold"+str(test_fold)+"/"+ "test.tmp")
        test_file = open(test_path,'w')
        test_set = self.folds[self.fold_prefix+str(test_fold)]
        for test_data in test_set:
            test_file.write(test_data)
        test_file.close()
        command = "sort -k2  " + path + "fold" + str(test_fold) + "/" + "test.tmp > " + path + "fold" + str(test_fold) + "/" + "test.txt"
        for output_line in self.run_command(command):
            print (output_line)
        if os.path.exists(path + "fold" + str(test_fold) + "/" + "test.tmp"):
            os.remove(path + "fold" + str(test_fold) + "/" + "test.tmp")
        print("finished test.txt")


    def run_command(self,command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        return iter(p.stdout.readline, b'')

    def split_train_file_into_folds(self):
        number_of_queries_in_file = math.floor(float(float(self.number_of_queries)/self.k))
        query_to_fold = self.init_files(number_of_queries_in_file)
        self.normalize_training_file()
        self.folds = self.go_over_train_file_and_split_to_folds(query_to_fold)
        self.create_folds_splited_into_folders()