import competition_stats_handler as csh
import os
import subprocess
from model_running import  cross_validator as cv
from model_running import evaluator as ev
import sys
#aaaaZ
class lambda_mart_stats_handler(csh.competition_stats_handler):

    def __init__(self,model,max_distance,cross_validator):
        self.model = model
        self.max_distance = max_distance
        self.cross_validator = cross_validator


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
            if os.path.exists(file_name):
                os.remove(file_name)

    def run_models(self,chosen_models,new_scores_path,data_set_location,final_scores_directory):
        foramted_score_files = []
        if not os.path.exists(final_scores_directory):
            os.makedirs(final_scores_directory)
        final_score_file=final_scores_directory+"/final_competition_score.txt"
        if os.path.exists(final_score_file):
            os.remove(final_score_file)
        for fold in chosen_models:
            if not os.path.exists(new_scores_path+"/"+fold):
                os.makedirs(new_scores_path+ "/" + fold)
            if not os.path.exists(final_scores_directory+"/"+fold):
                os.makedirs(final_scores_directory+ "/" + fold)
            model = chosen_models[fold]
            competition_file = data_set_location+"/"+fold+"/test.txt"
            print "running on file",competition_file
            score_file = self.cross_validator.run_model_lmbda_mart(model, competition_file, new_scores_path+"/"+fold)
            query_doc_index = self.prepare_index_of_test_file(competition_file)
            foramted_score_files.append(self.create_file_in_trec_eval_format(score_file, final_scores_directory + "/" + fold, 'RANKLIB',query_doc_index))

        out = open(final_score_file,'a')
        for file in foramted_score_files:
            print "working on file ",file
            with open(file) as score_file:
                for score in score_file:
                    out.write(score)
        out.close()
        return final_score_file

    def retrieve_new_ranking(self,final_score_file):
        scores = {}
        with open(final_score_file) as score_file:
            for score in score_file:
                splits = score.split()
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

    #Freaky code check ----------------------------------------------------------------------------------------------------
    def prepare_index_of_test_file(self,test_file):
        query_doc_index = {}
        with open(test_file) as test_data:

            row_number = 0
            for data_record in test_data:
                query_id = data_record.split(" ")[1].split(":")[1]
                document_name = data_record.split("#")[1].rstrip()
                if not query_doc_index.get(row_number,False):
                    query_doc_index[row_number]={}
                    query_doc_index[row_number][query_id]=document_name
                row_number += 1
        return query_doc_index

    def create_file_in_trec_eval_format(self,scores_file,final_scores_directory,package,query_doc_index):
        scores_file_name = os.path.basename(scores_file)
        scores_file_name_temp = os.path.basename(scores_file).replace(".txt",".tmp")
        trec_eval_formatted_file_before_sort = final_scores_directory+"/"+scores_file_name_temp
        trec_eval_formatted_file_before_sort_file = open(trec_eval_formatted_file_before_sort,'w')
        trec_eval_formatted_file_final =  final_scores_directory+"/"+scores_file_name
        with open(scores_file) as scores_data:
            row_number = 0
            for score_record in scores_data:
                score = score_record.rstrip()

                if package == 'RANKLIB':
                    if "\t" in score:
                        score = score.split("\t")[2]# for ranklib score files

                query_id = query_doc_index[row_number].keys()[0]
                document_name = query_doc_index[row_number][query_id]

                trec_eval_formatted_file_before_sort_file.write(query_id+"\tQ0\t"+document_name+"\t"+str(row_number)+"\t"+str(score)+"\tindri\n")
                row_number += 1
        trec_eval_formatted_file_before_sort_file.close()
        command = "sort -k1,1 -k5nr  "+trec_eval_formatted_file_before_sort+" > "+trec_eval_formatted_file_final
        for output_line in self.run_command(command):
            print(output_line)
        if os.path.exists(trec_eval_formatted_file_before_sort):
            os.remove(trec_eval_formatted_file_before_sort)
        return trec_eval_formatted_file_final