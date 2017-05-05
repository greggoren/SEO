import competition_stats_handler as csh
class winner_reference_point(csh.competition_stats_handler):
    def __init__(self, model, max_distance):
        self.model = model
        self.max_distance = max_distance

    def activation_func(self,input):
        print ""

    def create_items_for_knapsack(self,competitors,features_index,model_weights_index,query_to_fold,original_vectors):
        print "creating items for bag"
        cost_index = {}
        value_for_change = {}
        for query in competitors:
            cost_index[query] = {}
            competitors_list = competitors[query]
            first_competitor_features = features_index[query][competitors_list[0]]
            value_for_change[query] = first_competitor_features
            for competitor in competitors_list:

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


