from seo import competition_stats_handler as csh

class abs_stat_handler_svm(csh.competition_stats_handler):
    def __init__(self,model,max_distance):
        self.model = model
        self.max_distance = max_distance


    def activation_func(self,input):
        ""


    def create_vector_from_above_competitors(self,competitors,document_features,number_of_competitors):

        print "getting reference vectors"
        chosen_vectors={}
        opt = True
        cache_list_of_weights=self.initilize_cache_of_normaliztion(number_of_competitors)
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
                    zipped = zip(weights_for_average, list_of_vectors)
                    temporary_list = []
                    for i, list in zipped:
                        temporary_list.append([i * d for d in list])
                    competitor_refrence_vector = [sum(i) for i in zip(*temporary_list)]
                    chosen_vectors[query][competitor] = competitor_refrence_vector
                else:
                    chosen_vectors[query][competitor] = []
        return chosen_vectors


    def initilize_cache_of_normaliztion(self,number_of_competitors,alpha=60):
        cache_list_of_weights = {}
        for index in range(1, number_of_competitors):
            list_of_index = list((range(1, index)))
            temp_result = [1.0 / (obj + alpha) for obj in list_of_index]
            denominator = sum(temp_result)
            result = [float(obj)/denominator for obj in temp_result]
            cache_list_of_weights[index] = result
        return cache_list_of_weights

    def initialize_cache_of_weights(self,number_of_competitors):
        cache_list_of_weights = {}
        for index in range(1,number_of_competitors):
            list_of_index = list(reversed(range(1,index+1)))
            sum_of_list = sum(list_of_index)
            result = [float(obj)/sum_of_list for obj in list_of_index]
            cache_list_of_weights[index]=result
        return cache_list_of_weights

    def create_items_for_knapsack(self,competitors,features_index,number_of_competitors):
        print "creating items for bag"
        indexes_for_change = {}
        value_for_change = {}
        for query in competitors:
            reference_vector = features_index[query][competitors[query][0]]
            value_for_change[query]=reference_vector
            indexes_for_change[query]={}
            for document in competitors[query]:
                changed_vector = [(abs(a-b),features_index[query][document].index(a)) for a,b in zip(features_index[query][document],reference_vector)]
                sorted_changed_vector =sorted(changed_vector,key=lambda x:x[0],reverse=True)[:50]
                indexes_for_change[query][document] = [a[1] for a in sorted_changed_vector]
        print "items creation ended"
        return indexes_for_change,value_for_change