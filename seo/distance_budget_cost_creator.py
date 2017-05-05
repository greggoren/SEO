import seo.competition_stats_handler as gbcc
from copy import deepcopy
from scipy import spatial as sp
from math import sqrt
class distance_budget_cost_creator(gbcc.competition_stats_handler):

    def __init__(self,model,max_distance):
        self.model = model
        self.max_distance = max_distance

    def square_rooted(self,x):
        return sqrt(sum([a * a for a in x]))

    def cosine_dist(self,x, y):
        numerator = sum(a * b for a, b in zip(x, y))

        denominator = self.square_rooted(x) * self.square_rooted(y)
        return 1 - numerator / float(denominator)

    def activation_func(self,input):
        index = input[0]
        first_competitor_features=input[1]
        competitor_features = input[2]
        original_vector = input[3]
        competitor_features[index]=first_competitor_features[index]
        return self.cosine_dist(competitor_features,original_vector)
