import competition_maker as cm
import knapsack_algorithm as ka

class competition_maker_winner_reference(cm.competition_maker):


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
            reference_vec = values_for_change[query]
            for competitor in competitors[query]:
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