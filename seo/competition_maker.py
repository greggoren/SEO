import knapsack_algorithm as ka
from copy import deepcopy
from scipy.stats import kendalltau as kt
import competition_stats_handler as gbcc
import math
import cPickle as cp

class competition_maker:

    def __init__(self,num_of_iterations,budget_creator,score_file,number_of_competitors,data_set_location,fraction,chosen_models,query_per_fold):
        self.num_of_iterations = num_of_iterations
        self.budget_creator = budget_creator
        self.score_file = score_file
        self.number_of_competitors = number_of_competitors
        self.data_set_location = data_set_location
        self.fraction = fraction
        self.chosen_models = chosen_models
        self.query_per_fold = query_per_fold

    def get_features_to_change(self,competitors,cost_index,values_for_change,competitor_features,original_features):
        features_to_change = {}
        denominator = 0
        sum_of_number_of_features = 0
        for query in cost_index:
            features_to_change[query] = {}
            for competitor in competitors[query]:
                reference_vec = values_for_change[query][competitor]
                current_features = competitor_features[query][competitor]
                original_competitor = original_features[query][competitor]
                items = cost_index[query][competitor]
                packer = ka.knapsack(items, self.budget_creator.max_distance)
                features =[feature[0] for feature in packer.pack(original_competitor,current_features,reference_vec)]
                features_to_change[query][competitor] = features
                sum_of_number_of_features+=len(features)
                denominator+=1
        print "sum of number of features ",sum_of_number_of_features
        return features_to_change ,float(sum_of_number_of_features)/denominator


    def update_competitors(self,features_to_change,competitors_features,value_for_change):
        for query in competitors_features:
            for doc in competitors_features[query]:
                features = competitors_features[query][doc]
                length = len(features)
                for index in range(length):
                    if features_to_change.get(query, False):
                        if index in features_to_change[query][doc]:

                            competitors_features[query][doc][index]=value_for_change[query][index]
        return competitors_features

    def competition(self,cost_model):
        results = {}
        competitors = self.budget_creator.get_competitors_for_query(self.score_file, self.number_of_competitors)
        reference_of_indexes = cp.loads(cp.dumps(competitors,1))
        document_feature_index = self.budget_creator.index_features_for_competitors(competitors,self.data_set_location,True)
        original_vectors = cp.loads(cp.dumps(document_feature_index,-1))
        model_weights_per_fold_index = self.budget_creator.get_chosen_model_weights_for_fold(self.chosen_models)
        x_axis =[]
        y_axis = []
        changed_winner_averages =[]
        average_distances = []
        original_reference = []
        average_winner_rank = []
        average_feature_number = []
        last_winner_original_rank = {}
        original_winner_final_rank = {}
        for iteration in range(0,self.num_of_iterations):

            print "iteration number ",iteration+1
            sum_of_kendalltau = 0
            average_distance = self.budget_creator.create_budget_per_query(self.fraction,document_feature_index)
            cost_index,value_for_change = self.budget_creator.create_items_for_knapsack(competitors, document_feature_index,model_weights_per_fold_index,self.query_per_fold,original_vectors)
            print "getting features to change"
            features_to_change ,avg_feature_num= self.get_features_to_change(competitors,cost_index,value_for_change,document_feature_index,original_vectors)
            print "got features to change"
            average_feature_number.append(avg_feature_num)
            print "updating competitors"
            document_feature_index = self.update_competitors(features_to_change,cp.loads(cp.dumps(document_feature_index,-1)),value_for_change)
            print "update complete"
            print "getting new rankings"
            competitors_new,ties= self.get_new_rankings(competitors,document_feature_index,model_weights_per_fold_index,self.query_per_fold)
            print "number of queries with ties ",ties
            print "finished new rankings"
            number_of_time_winner_changed = 0
            denominator = 0
            sum_of_original_kt=0
            sum_rank_of_winner = 0
            for query in competitors_new:
                old_rank = self.transition_to_rank_vector(query,reference_of_indexes,competitors[query])
                new_rank = self.transition_to_rank_vector(query,reference_of_indexes,competitors_new[query])
                orig_rank = self.transition_to_rank_vector(query,reference_of_indexes,reference_of_indexes[query])
                if iteration+1==self.num_of_iterations:
                    if not last_winner_original_rank.get(new_rank.index(1)+1,False):
                        last_winner_original_rank[new_rank.index(1) + 1] =0
                    last_winner_original_rank[new_rank.index(1)+1]+=1
                    if not original_winner_final_rank.get(new_rank[0],False):
                        original_winner_final_rank[new_rank[0]]=0
                    original_winner_final_rank[new_rank[0]]+=1
                kendall_tau,p_value = kt(old_rank,new_rank)

                if not math.isnan(kendall_tau):
                    sum_of_kendalltau+=kendall_tau
                    denominator += 1
                    if old_rank.index(1) != new_rank.index(1):
                        number_of_time_winner_changed += 1
                    sum_rank_of_winner+=new_rank[0]

                original_kt,p_val = kt(new_rank,orig_rank)
                if not math.isnan(original_kt):
                    sum_of_original_kt += original_kt
            print "number of times winner changed ",number_of_time_winner_changed

            average = sum_of_kendalltau/denominator
            average_distances.append(average_distance)
            changed_winner_averages.append(float(number_of_time_winner_changed)/denominator)
            average_winner_rank.append(float(sum_rank_of_winner)/denominator)
            x_axis.append(iteration+1)
            y_axis.append(average)
            original_reference.append(float(sum_of_original_kt)/denominator)
            competitors = cp.loads(cp.dumps(competitors_new,-1))

        results["kendall"]=(x_axis,y_axis)
        results["cos"] = (x_axis,average_distances)
        results["winner"] = (x_axis,changed_winner_averages)
        results["orig"] =(x_axis,original_reference)
        results["win_rank"]=(x_axis,average_winner_rank)
        results["whoisthewinner"] = last_winner_original_rank
        results["originalwinnerrank"]=original_winner_final_rank
        results["avg_f"] = (x_axis,average_feature_number)
        meta_results = {}
        meta_results[self.budget_creator.model] = results

        return meta_results


    def get_new_rankings(self,original_ranks,document_features,model_weights,query_per_fold):
        new_competitors={}
        ties = 0
        for query in document_features:
            doc_scores = {}
            weights = model_weights[query_per_fold[query]]
            original_rank = original_ranks[query]
            for doc in document_features[query]:
                doc_features = document_features[query][doc]
                score = self.dot_product(doc_features, weights)
                doc_scores[doc] = score

            sorted_ranking = sorted(original_rank, key=lambda x:(doc_scores[x]), reverse=True)
            if len(sorted_ranking)>1:
                if doc_scores[sorted_ranking[0]]==doc_scores[sorted_ranking[1]]:
                    ties+=1
            new_competitors[query] = sorted_ranking
        return new_competitors,ties




    def dot_product(self,list1,list2):
        return sum([i*j for (i, j) in zip(list1, list2)])

    def transition_to_rank_vector(self,query,reference_of_indexes,list_of_docs):
        original_list = reference_of_indexes[query]
        rank_vector = []
        for doc in original_list:
            rank_vector.append(list_of_docs.index(doc)+1)
        return rank_vector
