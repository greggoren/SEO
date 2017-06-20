from copy import copy
import random
from math import sqrt
class random_knapsack:
    def __init__(self,items,max):
        self.MAXWT = max
        self.items = items

    def square_rooted(self,x):
        return sqrt(sum([a * a for a in x]))

    def cosine_dist(self,x, y):
        numerator = sum(a * b for a, b in zip(x, y))

        denominator = self.square_rooted(x) * self.square_rooted(y)
        return 1 - numerator / float(denominator)


    def pack(self,original_vector,competitor_features,first_competitor_features):

        bagged = []
        temp_vec = copy(competitor_features)
        for name in self.items:
            index = name
            if len(first_competitor_features) == 0:
                break
            if first_competitor_features[index]==temp_vec[index]:
                continue
            temp_vec[index] = first_competitor_features[index]
            if self.cosine_dist(temp_vec,original_vector)>self.MAXWT:
                temp_vec[index]=competitor_features[index]
                continue

            bagged += [(name,)]
        return bagged