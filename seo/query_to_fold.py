import os
class qtf:
    def __init__(self,base_dir):
        self.base_dir = base_dir
        self.query_to_fold_index ={}

    def create_query_to_fold_index(self):
        print "creating query to fold index"
        for dir in os.walk(self.base_dir):
            if not dir[1]:
                fold = os.path.basename(dir[0])
                test_file = dir[0]+"/test.txt"
                with open(test_file) as test_data:
                    for test_record in test_data:
                        splited_data = test_record.split()
                        query_id = int(splited_data[1].split(":")[1])
                        self.query_to_fold_index[query_id] = fold
        print "creation finished"