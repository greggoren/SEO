import os
import subprocess
import sys

from model_running import evaluator

from model_running import folds_creator as fc


class cross_validator:
    def __init__(self,k,folds_creator,data_set,number_of_queries=-1,fold_prefix = "fold"):
        self.folds_creator = folds_creator# fc.folds_creator(k,train_data,number_of_queries,fold_prefix)
        self.folds_creator.split_train_file_into_folds()
        self.fold_prefix = fold_prefix
        self.k =k
        self.number_of_trees_for_test = [500, 250]
        self.number_of_leaves_for_test = [5, 10]
        self.svm_c_params_to_test = [0.1, 0.01, 0.001]
        self.data_set = data_set
        self.chosen_models = {}
        self.final_score_path = ""
        self.models_path = ""



    def run_command(self,command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        return iter(p.stdout.readline, b'')

    def create_model_lmbda_mart(self, number_of_trees, number_of_leaves, train_file,model_directory,query_relevance_file):

        command = '/lv_local/home/sgregory/jdk1.8.0_121/bin/java -jar ../model_running/RankLib.jar -train '+train_file+ \
                  ' -ranker 6 -qrel '+query_relevance_file+' -metric2t NDCG@20'\
                  ' -tree '+str(number_of_trees) +' -leaf '+str(number_of_leaves) +\
                  ' -save '+model_directory+'/model_'+str(number_of_trees)+"_"+str(number_of_leaves)+'.txt' #path to java 1.8
        print "command = ",command
        for output_line in self.run_command(command):
            print(output_line)



    def run_model_lmbda_mart(self,model_file,test_file,score_directory):
        score_file_prefix_with_extension=os.path.basename(model_file)
        score_file_prefix = os.path.splitext(score_file_prefix_with_extension)[0]
        score_file = score_directory + '/' + score_file_prefix + '.txt'
        run_command = '/lv_local/home/sgregory/jdk1.8.0_121/bin/java -jar ../model_running/RankLib.jar -load ' + model_file + \
                  ' -rank '+test_file+' -score '+score_file #path to java 1.8
        for output_line in self.run_command(run_command):
            print(output_line)

        return score_file


    def run_lmbda_mart_models_on_validation_set_and_pick_the_best(self, models_dir, validation_file, score_directory, scores_in_trec_format_path,qrel_path):
        models_dirs = os.walk(models_dir)
        evaluation =  evaluator.evaluator()
        evaluation.prepare_index_of_test_file(validation_file)
        for models_dir in models_dirs:
            if not models_dir[1]:
                for model in models_dir[2]:
                    model_file = models_dir[0]+"/"+model
                    self.run_model_lmbda_mart(model_file,validation_file,score_directory)
        for scores_dir_data in os.walk(score_directory):
            if not scores_dir_data[1]:#no subdirectories
                for scores_file_name in scores_dir_data[2]:
                    scores_file = scores_dir_data[0]+"/"+scores_file_name
                    evaluation.create_file_in_trec_eval_format(scores_file,scores_in_trec_format_path,'RANKLIB')
        for final_score_dir in os.walk(scores_in_trec_format_path):
            if not final_score_dir[1]:
                evaluation.run_trec_eval_on_evaluation_set(final_score_dir[0],qrel_path)
                fold = os.path.basename(final_score_dir[0])
                self.chosen_models[fold] = evaluation.chosen_model

    def k_fold_cross_validation(self,model,query_relevance_file):
        test_score_files = []
        print("w=", self.folds_creator.working_path)
        dirs = os.walk(self.folds_creator.working_path)

        result_dir = os.path.abspath(os.path.join(self.folds_creator.working_path,os.pardir))
        print(result_dir)
        final_result_file_combined = result_dir + "/" + self.data_set + "/test_scores_trec_format/" + model+"/final_score_combined.tmp"
        for dir in dirs:
            if not dir[1]:#no subdirectories
                dir_name = os.path.basename(dir[0])
                self.models_path = models_path = result_dir+"/"+self.data_set+"/models"+"/"+model+"/"+dir_name
                if not os.path.exists(models_path):
                    os.makedirs(models_path)
                scores_path = result_dir+"/"+self.data_set+"/scores"+"/"+model+"/"+dir_name
                scores_in_trec_format_path = result_dir+"/"+self.data_set+"/final_format_scores"+"/"+model+"/"+dir_name
                if not os.path.exists(scores_path):
                    os.makedirs(scores_path)
                if not os.path.exists(scores_in_trec_format_path):
                    os.makedirs(scores_in_trec_format_path)
                test_scores_path = result_dir+"/"+self.data_set+"/test_scores/"+model+"/"+dir_name
                self.final_score_path = final_test_scores_in_trec_format = result_dir+"/"+self.data_set+"/test_scores_trec_format/"+model+"/"+dir_name
                if not os.path.exists(test_scores_path):
                    os.makedirs(test_scores_path)
                if not os.path.exists(final_test_scores_in_trec_format):
                    os.makedirs(final_test_scores_in_trec_format)
                if model == "LAMBDAMART":
                    self.lambda_mart_models_creator(dir[0] + "/train.txt",models_path,query_relevance_file)
                    self.run_lmbda_mart_models_on_validation_set_and_pick_the_best(models_path, dir[0] + "/validation.txt", scores_path, scores_in_trec_format_path,query_relevance_file)
                    test_score_files.append(self.run_chosen_model_on_test_lambda_mart(dir_name,models_path,dir[0]+"/test.txt",test_scores_path,final_test_scores_in_trec_format,query_relevance_file))
                elif model == "SVM":
                    self.svm_models_creator(dir[0] + "/train.txt",models_path)
                    self.run_svm_on_validation_set_and_pick_the_best(models_path, dir[0] + "/validation.txt", scores_path, scores_in_trec_format_path,query_relevance_file)
                    test_score_files.append(self.run_svm_on_test_set(dir_name,models_path, dir[0]+"/test.txt",test_scores_path,final_test_scores_in_trec_format,query_relevance_file))
        with open(final_result_file_combined,'w') as final_file:
            for trec_file in test_score_files:
                with open(trec_file) as infile:
                    for record in infile:
                        final_file.write(record)
        self.sort_and_evaluate_final_file(final_result_file_combined,query_relevance_file)



    def sort_and_evaluate_final_file(self,final_file_name,qrel_path):
        final_file_as_txt = final_file_name.replace("tmp","txt")
        command = "sort -k1,1 -k5nr "+final_file_name+" > "+final_file_as_txt
        for output_line in self.run_command(command):
            print(output_line)
        evaluation = evaluator.evaluator()
        evaluation.run_trec_eval_on_test_file(qrel_path,final_file_as_txt)


    def lambda_mart_models_creator(self, train_file,models_directory,query_relevance_file):
        print "inside models creator"
        for number_of_trees in self.number_of_trees_for_test:
            for number_of_leaves in self.number_of_leaves_for_test:
                self.create_model_lmbda_mart(number_of_trees, number_of_leaves, train_file,models_directory,query_relevance_file)


    def svm_models_creator(self,train_file,models_directory):
        for c_value in self.svm_c_params_to_test:
            learning_command = "./svm_rank_learn -c " + str(c_value) + " "+train_file+" "+models_directory+"/svm_model"+str(c_value)+".txt"
            for output_line in self.run_command(learning_command):
                print(output_line)



    def run_chosen_model_on_test_lambda_mart(self,fold,models_path,test_file,score_dir,final_score_directory,qrel_path):
        key =fold
        model_file_name = models_path+"/"+self.chosen_models[key]
        score_file = self.run_model_lmbda_mart(model_file_name,test_file,score_dir)
        evaluation = evaluator.evaluator()
        evaluation.prepare_index_of_test_file(test_file)
        final_score_trec_file = evaluation.create_file_in_trec_eval_format(score_file,final_score_directory,'RANKLIB')
        return final_score_trec_file
        #evaluation.run_trec_eval_on_test_file(qrel_path,final_score_trec_file)

    def run_svm_on_validation_set_and_pick_the_best(self,models_dir, validation_file, score_directory, scores_in_trec_format_path,qrel_path):
        models_dirs = os.walk(models_dir)
        evaluation = evaluator.evaluator()
        evaluation.prepare_index_of_test_file(validation_file)
        for models_dir in models_dirs:
            if not models_dir[1]:
                for model in models_dir[2]:
                    model_file = models_dir[0] + "/" + model
                    self.run_model_svm(model_file, validation_file, score_directory)
        for scores_dir_data in os.walk(score_directory):
            if not scores_dir_data[1]:  # no subdirectories
                for scores_file_name in scores_dir_data[2]:
                    scores_file = scores_dir_data[0] + "/" + scores_file_name
                    evaluation.create_file_in_trec_eval_format(scores_file, scores_in_trec_format_path, '')
        for final_score_dir in os.walk(scores_in_trec_format_path):
            if not final_score_dir[1]:
                evaluation.run_trec_eval_on_evaluation_set(final_score_dir[0], qrel_path)
                fold = os.path.basename(final_score_dir[0])
                self.chosen_models[fold] = evaluation.chosen_model


    def run_model_svm(self,model_file, test_file, score_directory):
        model_name = os.path.basename(model_file)
        score_file = score_directory+"/"+model_name
        test_command = "./svm_rank_classify "+test_file+" "+model_file +" "+score_directory+"/"+model_name
        for output_line in self.run_command(test_command):
            print(output_line)
        return score_file

    def run_svm_on_test_set(self,fold,models_path,test_file,score_dir,final_score_directory,qrel_path):
        key = fold
        print(self.chosen_models.keys())
        sys.stdout.flush()
        model_file_name = models_path + "/" + self.chosen_models[key]
        score_file = self.run_model_svm(model_file_name, test_file, score_dir)
        evaluation = evaluator.evaluator()
        evaluation.prepare_index_of_test_file(test_file)
        final_score_trec_file = evaluation.create_file_in_trec_eval_format(score_file, final_score_directory, '')
        return final_score_trec_file
        #evaluation.run_trec_eval_on_test_file(qrel_path, final_score_trec_file)





    """def run_cross_validation_with_svm(self,c_value):
        learning_command = "svm_rank_learn -c "+str(c_value)+" train.txt svm_model.txt"
        for output_line in self.run_command(learning_command):
            print(output_line)

        #TODO:handle what happens if no model file created

        test_command = "svm_rank_classify test.txt svm_model.txt predictions.txt"
        for output_line in self.run_command(test_command):
            print(output_line)

        #TODO:handle what happens if no predictions file created

        self.evaluate_svm("predictions.txt")"""
























    """ def create_train_set_for_ltr(self,test,validation):

        folds = self.folds_creator.folds
        not_train = [test,validation]
        train_set =[]
        for fold in folds:
            if fold not in not_train:
                train_set.extend(folds[fold])
        path = os.path.dirname(__file__)+"/"
        absolute_path = os.path.abspath(path+ "train.txt")
        if os.path.isfile("/train.txt"):
            os.remove(absolute_path)
        file_for_ltr = open('train.txt', 'w')
        for train_data in train_set:
            file_for_ltr.write("%s" % train_data)
        file_for_ltr.close()


    def create_validation_set_for_ltr(self, validation):

        validation_set = self.folds_creator.folds[validation]
        path = os.path.dirname(__file__) + "/"
        absolute_path = os.path.abspath(path+"validation.txt")
        if os.path.isfile(absolute_path):
            os.remove(absolute_path)
        file_for_ltr = open(absolute_path, 'w')
        for validation_data in validation_set:
            file_for_ltr.write("%s" % validation_data)
        file_for_ltr.close()

    def create_test_set_for_ltr(self, test):

        test_set = self.folds_creator.folds[test]
        path = os.path.dirname(__file__) + "/"
        absolute_path = os.path.abspath(path + "test.txt")
        if os.path.isfile(absolute_path):
            os.remove(absolute_path)
        file_for_ltr = open(absolute_path, 'w')
        for test_data in test_set:
            file_for_ltr.write("%s" % test_data)
        file_for_ltr.close()"""

    """    def run_cross_validation_for_models(self,model):
        if model == "SVMRANK":
            self.k_fold_cross_validation_svm()
        elif model == "LAMBDAMART":
            self.lambda_mart_models_creator()
        elif model == "ALL":#TODO to be tested
            svm_process = mp.Process(name='svm',target=self.k_fold_cross_validation_svm)
            lambdamart_process = mp.Process(name='lmbda', target=self.lambda_mart_models_creator)
            process_handler = [svm_process,lambdamart_process]

            for process in process_handler:
                process.start()

            for process in process_handler:
                process.join()
        else:
            raise Exception("A wrong parameter was entered for which model to run")"""