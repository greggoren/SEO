import competition_stats_handler as csh
import os
import subprocess
import model_running.cross_validator as cv
from model_running import evaluator as ev
import sys
#aaaaZ
class lambda_mart_stats_handler(csh.competition_stats_handler):

    def __init__(self,model,max_distance,cross_validator,evaluator):
        self.model = model
        self.max_distance = max_distance
        self.cross_validator = cross_validator
        self.evaluator = evaluator

    def activation_func(self,input):
        print ""

    def rewrite_data_set(self,new_document_fetures,query_to_fold,data_set_location):
        for query in new_document_fetures:
            fold = query_to_fold[query]
            data_file = data_set_location+"/"+fold+"/test.tmp"
            if not os.path.exists(data_set_location+"/"+fold):
                os.makedirs(data_set_location+"/"+fold)
            file_writer = open(data_file,'a')
            for competitor in new_document_fetures[query]:
                feature_vec = new_document_fetures[query][competitor]
                features = [str(i)+":"+str(j) for i,j in enumerate(feature_vec,start=1)]
                line ="0 qid:"+str(query)+" "
                line += " ".join(features)
                line += " # "+competitor
                file_writer.write(line+"\n")
            file_writer.close()
        for fold in set(query_to_fold.values()):
            file_name = data_set_location+"/"+fold+"/test.tmp"
            command = "sort -t ':' -nk 2,2 " + file_name +" > " + data_set_location+"/"+fold+"/test.txt"
            for out_line in self.run_command(command):
                print out_line
            print "preparing index of test for ",fold
            self.evaluator.prepare_index_of_test_file(data_set_location + "/" + fold + "/test.txt")
            if os.path.exists(file_name):
                os.remove(file_name)

    def run_models(self,chosen_models,new_scores_path,data_set_location,final_scores_directory):
        score_files = []
        foramted_score_files = []
        if not os.path.exists(final_scores_directory):
            os.makedirs(final_scores_directory)
        final_score_file=final_scores_directory+"/final_competition_score.txt"
        for fold in chosen_models:
            if not os.path.exists(new_scores_path+"/"+fold):
                os.makedirs(new_scores_path+ "/" + fold)
            if not os.path.exists(final_scores_directory+"/"+fold):
                os.makedirs(final_scores_directory+ "/" + fold)
            model = chosen_models[fold]
            competition_file = data_set_location+"/"+fold+"/test.txt"
            print "running on file",competition_file
            score_files.append(self.cross_validator.run_model_lmbda_mart(model, competition_file, new_scores_path+"/"+fold))
        for file in score_files:
            foramted_score_files.append(self.evaluator.create_file_in_trec_eval_format(file,final_scores_directory+"/"+fold,'RANKLIB'))
        out = open(final_score_file,'a')
        for file in foramted_score_files:
            with open(file) as score_file:
                for score in score_file:
                    out.write(score)
        out.close()
        return final_score_file

        #TODO : create unified score file

    def retrieve_new_ranking(self,final_score_file):
        scores = {}
        with open(final_score_file) as score_file:
            for score in score_file:
                splits = score.split()
                if splits[2]== '29914_77':
                    print "ok"
                    sys.stdout.flush()
                if not scores.get(int(splits[0]),False):
                    scores[int(splits[0])]=[]
                scores[int(splits[0])].append(splits[2])
        return scores

    def create_items_for_knapsack(self,competitors, document_feature_index):
        value_for_change = {}
        for query in competitors:
            value_for_change[query] = document_feature_index[query][competitors[query][0]]
        return value_for_change


    def run_command(self, command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        return iter(p.stdout.readline, b'')
