import copy
import random
class random_knapsack:
    def __init__(self,items,max):
        self.MAXWT = max
        self.items = items

    def pack(self,original_vector,competitor_features,first_competitor_features):

        bagged = []
        temp_vec = copy(competitor_features)
        for name in self.items:
            index = name
            temp_vec[index] = first_competitor_features[index]
            if self.cosine_dist(temp_vec,original_vector)>self.MAXWT:
                temp_vec[index]=original_vector[index]
                continue

            bagged += [(name,)]

        return bagged