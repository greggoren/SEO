from functools import partial
from multiprocessing import Pool as p
import os
import matplotlib.pyplot as plt

import svm_random_file_handler as d
import svm_random_competition_maker as cm
import letor_fold_creator_z_normalize as lfc
import query_to_fold as qtf
from model_running import cross_validator as cv


def simulation(chosen_models,data_set_location,query_to_fold_index,score_file,budget_creator):

    c = cm.competition_maker(12, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    return c.competition("/lv_local/home/sgregory/LTOR1/new_scores/"+budget_creator.model+"/final")


def write_res_to_file(result,model):
    for key in result:
        if not os.path.exists(model+"/"+key):
            os.makedirs(model+"/"+key)
        key = result.keys()[0]
        for stat in result[key]:

            out_file = open(model+"/"+key + "/" + stat + ".txt", 'w')
            try:
                if isinstance(result[key][stat], tuple):

                    for x, y in zip(result[key][stat][0], result[key][stat][1]):
                        out_file.write(str(x) + "\t" + str(y) + "\n")
                else:
                    for x, y in zip(result[key][stat].keys(), result[key][stat].values()):
                        out_file.write(str(x) + "\t" + str(y) + "\n")
            except:
                print result[key]
                print stat
            out_file.close()

def sum_dictionaries(dict_a,dict_b):
    result ={}
    for key in dict_a:
        for stat in  dict_a[key]:
            if isinstance(dict_a[key][stat], tuple):
                ""

if __name__ == "__main__":
    plt.ioff()
    data_set_location = "/lv_local/home/sgregory/letor_fixed1"
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator_z_normalize(data_set_location, data_set_location, True)
    score_file = "/lv_local/home/sgregory/LTOR1/test_scores_trec_format/SVM/final_score_combined.txt"

    pool = p(2)

    gg = d.winner_reference_point_random("01", 0.1)
    aa = d.winner_reference_point_random("005", 0.05)
    bb = d.winner_reference_point_random("001", 0.01)

    chosen_models = gg.recover_models_per_fold("/lv_local/home/sgregory/LTOR1/models/SVM",
                                               "/lv_local/home/sgregory/LTOR1/test_scores_trec_format/SVM/")
    f = partial(simulation, chosen_models, data_set_location, q.query_to_fold_index, score_file)

    g_input = [gg,aa,bb]
    results = pool.map(f,g_input)#[simulation(chosen_models,data_set_location,q.query_to_fold_index,score_file,"/lv_local/home/sgregory/LTOR_MART_min_max/competition","/lv_local/home/sgregory/LTOR_MART_min_max/new_scores","/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART/",gg)]#pool.map(f, g_input)
    for result in results:
        write_res_to_file(result,"SVM")
