import winner_refrence_point as csh
class winner_reference_point_random(csh.winner_reference_point):
    def __init__(self, model, max_distance):
        self.model = model
        self.max_distance = max_distance


    def create_items_for_knapsack(self, competitors, document_feature_index):
        value_for_change = {}
        for query in competitors:
            value_for_change[query] = document_feature_index[query][competitors[query][0]]
        return value_for_change
