import os
from model_running import cross_validator
import time
class lambda_mart_competition_time_test:

    def __init__(self,cross_validator):
        self.cross_validator = cross_validator

    def recover_models_per_fold(self,models_path,final_scores_path):#code duplication baahusharmuta.
        print "recovering chosen models"
        chosen_model = {}
        for fold in os.walk(final_scores_path):
            if not fold[1]:
                fold_number = os.path.basename(fold[0])
                model_file = models_path+"/"+fold_number+"/"+fold[2][0]
                chosen_model[fold_number]=model_file
        return chosen_model

    def get_competitiors(self,score_file,number_of_competitors):
        competitors = {}

        queries_finished = {}
        with open(score_file) as scores_data:
            for score_record in scores_data:
                data = score_record.split()
                query_number = int(data[0])
                document = data[2]
                if not queries_finished.get(query_number, False):
                    if not competitors.get(query_number, False):
                        competitors[query_number] = []
                    if len(competitors[query_number]) < number_of_competitors:
                        competitors[query_number].append(document)
                    else:
                        queries_finished[query_number] = True

        return competitors


    def index_features_for_competitors(self,competitors,data_set_location,normalized):
        print "features index creation started"
        document_feature_index = {}
        document_name_getter = {}
        amount = 0
        if (normalized):
            amount = 1
        for dirs in os.walk(data_set_location):
            if dirs[1]:
                first_directory = dirs[0]+"/"+dirs[1][0]
                for files in os.walk(first_directory):
                    for file_name in files[2]:
                        current_file = files[0]+"/"+file_name
                        with open(current_file) as features:
                            for feature in features:
                                feature_data = feature.split()
                                qid = int(feature_data[1].split(":")[1])
                                if not document_name_getter.get(qid,False):
                                    document_name_getter[qid]=0
                                doc_name = str(qid)+"_"+str(document_name_getter[qid])
                                document_name_getter[qid] = document_name_getter[qid] + 1
                                if doc_name in competitors[qid]:
                                    if not document_feature_index.get(qid, False):
                                        document_feature_index[qid] = {}
                                    features_length = len(feature_data)
                                    document_feature_index[qid][doc_name] = []
                                    for index in range(2, features_length - 1 - amount):
                                        data = feature_data[index]
                                        document_feature_index[qid][doc_name].append(float(data.split(":")[1]))
                print "feature index creation ended"
                return document_feature_index


    def rewrite_test_set_for_classification(self,document_feature_index,test_path,query_to_fold):
        relvant_file=""
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        for query in document_feature_index:
            if not os.path.exists(test_path+"/"+query_to_fold[query]):
                os.makedirs(test_path+"/"+query_to_fold[query])
            if not os.path.exists(test_path+"/"+query_to_fold[query]+"/test.txt"):
                relvant_file = open(test_path+"/"+query_to_fold[query]+"/test.txt","w")
            else:
                relvant_file = open(test_path+"/"+query_to_fold[query]+"/test.txt","a")
            for competitor in document_feature_index[query]:
                features = document_feature_index[query][competitor]
                new_record = "0 qid:"+str(query)+" "
                length = len(features)
                for i in range(0, length):
                    new_record+=str(i+1)+":"+str(features[i])+" "
                new_record+="# "+competitor+"\n"
                relvant_file.write(new_record)
            relvant_file.close()

    def testing_times(self,test_path,chosen_model,score_directory):
        if not os.path.exists(score_directory):
            os.makedirs(score_directory)
        for fold in os.walk(test_path):

            if not fold[1]:
                fold_number = os.path.basename(fold[0])
                model_file= chosen_model[fold_number]
                test_file = fold[0]+"/"+fold[2][0]
                begin = time.time()
                self.cross_validator.run_model_lmbda_mart(model_file,test_file,score_directory)
                time_taken = time.time()-begin
                print "it took ",time_taken