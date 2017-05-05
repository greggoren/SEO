from copy import copy
from scipy import spatial as sp
import cPickle as cp
from math import sqrt
class knapsack:

    def __init__(self,items,MAXWT):
        self.items = items
        self.MAXWT = MAXWT

    def square_rooted(self,x):
        return sqrt(sum([a * a for a in x]))

    def cosine_dist(self,x, y):
        numerator = sum(a * b for a, b in zip(x, y))

        denominator = self.square_rooted(x) * self.square_rooted(y)
        return 1 - numerator / float(denominator)

    def pack(self,original_vector,competitor_features,first_competitor_features):
        sorted_items = sorted(((value/amount, amount, name)
                               for name, amount, value  in self.items),
                              reverse = True)
        wt = val = 0
        bagged = []
        temp_vec = copy(competitor_features)
        for unit_value, amount, name in sorted_items:
            index = name
            temp_vec[index] = first_competitor_features[index]
            if self.cosine_dist(temp_vec,original_vector)>self.MAXWT:
                temp_vec[index]=original_vector[index]
                continue

            bagged += [(name,)]

        return bagged