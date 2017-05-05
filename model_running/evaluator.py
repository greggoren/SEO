import os
import subprocess
import sys
class evaluator:
    def __init__(self):
        self.query_doc_index={}
        self.metrics = ["map","ndcg_cut.20","P.5","P.10"]
        self.evaluation_metric = "ndcg_cut.20"
        self.chosen_model =""

    def run_command(self,command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        return iter(p.stdout.readline, b'')

    def prepare_index_of_test_file(self,test_file):
        with open(test_file) as test_data:

            row_number = 0
            for data_record in test_data:
                query_id = data_record.split(" ")[1].split(":")[1]
                document_name = data_record.split("#")[1].rstrip()
                if not self.query_doc_index.get(row_number,False):
                    self.query_doc_index[row_number]={}
                    self.query_doc_index[row_number][query_id]=document_name
                row_number += 1

    def create_file_in_trec_eval_format(self,scores_file,final_scores_directory,package):
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

                query_id = self.query_doc_index[row_number].keys()[0]
                document_name = self.query_doc_index[row_number][query_id]

                trec_eval_formatted_file_before_sort_file.write(query_id+"\tQ0\t"+document_name+"\t"+str(row_number)+"\t"+str(score)+"\tindri\n")
                row_number += 1
            trec_eval_formatted_file_before_sort_file.close()
            command = "sort -k1,1 -k5nr < "+trec_eval_formatted_file_before_sort+" > "+trec_eval_formatted_file_final
            for output_line in self.run_command(command):
                print(output_line)
            os.remove(trec_eval_formatted_file_before_sort)
        return trec_eval_formatted_file_final


    def run_trec_eval_on_evaluation_set(self,final_scores_directory,qrel_path):
        scores = []
        max_score = ""
        for score_dir in os.walk(final_scores_directory):
            if not score_dir[1]:
                for score_file in score_dir[2]:
                    final_score_file = score_dir[0]+"/"+score_file
                    command="./trec_eval -m "+self.evaluation_metric+ " "+qrel_path+" "+final_score_file
                    for output_line in self.run_command(command):
                        evaluation_score = output_line.split()[-1]
                        scores.append((final_score_file,evaluation_score))
                        if max_score == "":
                            max_score = evaluation_score
                            self.chosen_model = os.path.basename(final_score_file)

                        else:
                            if evaluation_score > max_score:
                                max_score= evaluation_score
                                self.chosen_model = os.path.basename(final_score_file)
                                sys.stdout.flush()

        summary_file = open(final_scores_directory+"/summary_of_evaluation.txt",'w')
        for score in scores:
            summary_file.write(score[0]+"\t"+score[1]+"\n")
        summary_file.close()

    def run_trec_eval_on_test_file(self,qrel_path,score_file):
        score_data = []
        final_scores_directory = os.path.dirname(score_file)
        model_name = os.path.basename(score_file)
        for metric in self.metrics:
            command = "./trec_eval -m "+metric+ " "+qrel_path+" "+score_file
            for output_line in self.run_command(command):
                score = output_line.split()[-1]
                score_data.append((model_name,metric,score))

        summary_file = open(final_scores_directory+"/summary_of_test_run.txt",'w')
        summary_file.write("MODEL\tMETRIC\tSCORE\n")
        for score_record in score_data:
            summary_file.write(score_record[0]+"\t"+score_record[1]+"\t"+score_record[2]+"\n")
        summary_file.close()
