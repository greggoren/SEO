from abc import ABCMeta, abstractmethod
import os
from copy import copy
from math import sqrt

class competition_stats_handler():
    __metaclass__ = ABCMeta

    @abstractmethod
    def activation_func(self,input):
        pass

    def get_competitors_for_query(self,score_file,number_of_competitors):
        competitors = {}
        queries_finished = {}
        with open(score_file) as scores_data:
            for score_record in scores_data:
                data = score_record.split()
                query_number = int(data[0])
                document = data[2]
                if not queries_finished.get(query_number,False):
                    if not competitors.get(query_number,False):
                        competitors[query_number] = []
                    if len(competitors[query_number]) < number_of_competitors:
                        competitors[query_number].append(document)
                    else:
                        queries_finished[query_number]=True

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
                                #if not document_name_getter.get(qid,False):
                                    #document_name_getter[qid]=0
                                doc_name = feature.split("# ")[1].rstrip()#str(qid)+"_"+str(document_name_getter[qid])
                                #document_name_getter[qid] = document_name_getter[qid] + 1
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

    def get_the_perfect_feature_vector_from_competitors(self,competitors,document_features,chosen_models,qtf):
        print "getting perfect vector"
        chosen_vectors={}
        length = 0
        opt = True
        for query in document_features:
            model_weights = chosen_models[qtf[query]]
            chosen_vectors[query]={}
            competitors_list = competitors[query]
            for competitor in document_features[query]:
                competitor_refrence_vector=[]
                if opt:
                    length, opt = len(document_features[query][competitor]), False
                index_of_competitor = competitors_list.index(competitor)
                sub_list = competitors_list[:index_of_competitor]
                if sub_list:
                    list_of_vectors = [document_features[query][x] for x in sub_list]
                else:
                    list_of_vectors=[]
                if list_of_vectors:
                    for index in range(0,length):
                        weight = model_weights[index]
                        competitor_refrence_vector.append(self.max_value(list_of_vectors,index,weight))
                    chosen_vectors[query][competitor]=competitor_refrence_vector
                else:
                    chosen_vectors[query][competitor] = []
        return chosen_vectors


    def max_value(self,input_list,index,weight):
        if weight>=0:
            return max([sublist[index] for sublist in input_list])
        else:
            return min([sublist[index] for sublist in input_list])


    def get_diameter_documents(self,query_number,document_features):
        candidate_one = ""
        candidate_two = ""
        max_distance = 0.0
        for document_one in document_features[query_number]:
            for document_two in document_features[query_number]:
                distance = self.cosine_dist(document_features[query_number][document_one],document_features[query_number][document_two])
                if distance > max_distance:
                    max_distance = distance
                    candidate_one = document_one
                    candidate_two = document_two
        return candidate_one,candidate_two,max_distance

    def square_rooted(self,x):
        return sqrt(sum([a * a for a in x]))

    def cosine_dist(self,x, y):
        numerator = sum(a * b for a, b in zip(x, y))

        denominator = self.square_rooted(x) * self.square_rooted(y)
        return 1 - numerator / float(denominator)

    def create_budget_per_query(self,fraction,competitor_features):
        print "creating budget per query"
        #budget_per_query = {}
        sum_of_distances = 0
        denominator = 0
        for query in competitor_features:
            doc_one,doc_two,max_distance= self.get_diameter_documents(query,competitor_features)
            if doc_two != "" and doc_one != "":
                #budget_per_query[query] = fraction*self.get_budget(query,doc_one,doc_two,competitor_features)
                sum_of_distances+=max_distance
                denominator+=1
            #else:
                #budget_per_query[query] = 0
        return sum_of_distances/denominator


    def get_budget(self,query,doc_one,doc_two,document_features):
        features_of_doc_one = document_features[query][doc_one]
        features_of_doc_two = document_features[query][doc_two]
        length_of_features = len(features_of_doc_one)
        budget = 0.0
        for index in range(0,length_of_features):
            diff = abs(features_of_doc_one[index]-features_of_doc_two[index])
            budget+=self.activation_func(diff)
        return budget


    def get_chosen_model_weights_for_fold(self,chosen_models):
        print "getting model weights"
        model_wheights_per_fold = {}
        for fold in chosen_models:
            chosen_model_file = chosen_models[fold]
            model_wheights_per_fold[fold] = []
            indexes_covered = []
            with open(chosen_model_file) as model_file:
                for line in model_file:
                    if line.__contains__(":"):
                        wheights = line.split()
                        wheights_length = len(wheights)

                        for index in range(1, wheights_length-1):

                            feature_id = int(wheights[index].split(":")[0])
                            if index < feature_id:
                                for repair in range(index,feature_id):
                                    if repair in indexes_covered:
                                        continue
                                    model_wheights_per_fold[fold].append(0)
                                    indexes_covered.append(repair)
                            model_wheights_per_fold[fold].append(float(wheights[index].split(":")[1]))
                            indexes_covered.append(feature_id)
        print "weights index ended"
        return model_wheights_per_fold

    def recover_models_per_fold(self,models_path,final_scores_path):
        print "recovering chosen models"
        chosen_model = {}
        for fold in os.walk(final_scores_path):
            if not fold[1]:
                fold_number = os.path.basename(fold[0])
                model_file = models_path+"/"+fold_number+"/"+fold[2][0]
                chosen_model[fold_number]=model_file
        return chosen_model

    def create_items_for_knapsack(self,competitors,features_index,model_weights_index,query_to_fold,original_vectors):
        print "creating items for bag"
        value_for_change = self.get_the_perfect_feature_vector_from_competitors(competitors,features_index,model_weights_index,query_to_fold)
        cost_index = {}
        for query in competitors:
            cost_index[query] = {}
            competitors_list = competitors[query]
            for competitor in competitors_list:
                first_competitor_features = value_for_change[query][competitor]
                features_value_and_weight = []
                competitor_features = features_index[query][competitor]
                length_of_features = len(first_competitor_features)
                for index in range(0,length_of_features):

                    value = model_weights_index[query_to_fold[query]][index]*(first_competitor_features[index] - competitor_features[index])
                    if value > 0:
                        features_value_and_weight.append((index, 1, value))

                cost_index[query][competitor]=features_value_and_weight
        print "items creation ended"
        return cost_index,value_for_change





    def get_all_possible_single_changes(self,current_vec,winner_vec):
        list_of_vectors=[]
        length = len(current_vec)
        for index in range(0,length):
            temp = copy(current_vec)
            temp[index]=winner_vec[index]
            list_of_vectors.append(temp)
        return list_of_vectors

