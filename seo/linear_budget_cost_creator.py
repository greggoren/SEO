import seo.competition_stats_handler as gbcc

import math
class linear_budget_cost_creator(gbcc.competition_stats_handler):
    def __init__(self,model):
        self.model = model

    def activation_func(self,input):
        return abs(input)*2