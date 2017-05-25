class relevance_index:
    def __init__(self,qrels_file):
        self.qrels_file = qrels_file
        self.rel_index={}

    def create_relevance_index(self):
        with open(self.qrels_file) as qrel:
            for query_relevance in qrel:
                splited_data = query_relevance.split()
        self.rel_index[splited_data[2]] = splited_data[3]
