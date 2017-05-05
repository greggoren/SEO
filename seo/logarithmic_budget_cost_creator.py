import seo.competition_stats_handler as gbcc

import math
class logarithmic_budget_cost_creator(gbcc.competition_stats_handler):
    def __init__(self,model):
        self.model = model


    def activation_func(self,input):
        return math.log(math.exp(1)+abs(input))