import lambdamart_file_handler as lfh
class all_above_stat_handler_lbda(lfh.lambda_mart_stats_handler):

    def __init__(self, model, max_distance, cross_validator):
        self.model = model
        self.max_distance = max_distance
        self.cross_validator = cross_validator

    def create_vector_from_above_competitors(self,competitors,document_features,number_of_competitors):

        print "getting reference vectors"
        chosen_vectors={}
        opt = True
        cache_list_of_weights=self.initialize_cache_of_weights(number_of_competitors)
        for query in document_features:
            chosen_vectors[query]={}
            competitors_list = competitors[query]
            for competitor in document_features[query]:
                if opt:
                    length, opt = len(document_features[query][competitor]), False
                index_of_competitor = competitors_list.index(competitor)
                sub_list = competitors_list[:index_of_competitor]
                if sub_list:
                    list_of_vectors = [document_features[query][x] for x in sub_list]
                else:
                    list_of_vectors=[]
                if list_of_vectors:
                    weights_for_average = cache_list_of_weights[index_of_competitor]
                    temporary_list = [sum(i) for i in zip(*list_of_vectors)]
                    competitor_refrence_vector = [a*b for a,b in zip(weights_for_average,temporary_list)]
                    chosen_vectors[query][competitor]=competitor_refrence_vector
                else:
                    chosen_vectors[query][competitor] = []
        return chosen_vectors


    def initialize_cache_of_weights(self,number_of_competitors):
        cache_list_of_weights = {}
        for index in range(1,number_of_competitors):
            list_of_index = list(reversed(range(1,index+1)))
            sum_of_list = sum(list_of_index)
            result = [float(obj)/sum_of_list for obj in list_of_index]
            cache_list_of_weights[index]=result
        return cache_list_of_weights

    def create_items_for_knapsack(self,competitors,features_index,model_weights_index,query_to_fold,original_vectors,number_of_competitors):
        print "creating items for bag"
        value_for_change = self.create_vector_from_above_competitors(competitors,features_index,number_of_competitors)
        print "items creation ended"
        return value_for_change