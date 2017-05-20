from functools import partial
from multiprocessing import Pool as p
import os
import matplotlib.pyplot as plt

import lambdamart_file_handler as d
import lbda_competition_maker as cm
import letor_fold_creator_z_normalize as lfc
import query_to_fold as qtf
from model_running import cross_validator as cv


def simulation(chosen_models,data_set_location,query_to_fold_index,score_file,c_d_loc,new_scores_path,models_path,budget_creator):

    c = cm.competition_maker(1, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index,c_d_loc,new_scores_path,models_path)
    return c.competition("/lv_local/home/sgregory/LTOR_MART_min_max/new_scores/final")


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


if __name__ == "__main__":
    plt.ioff()
    data_set_location = "/lv_local/home/sgregory/letor_fixed1"
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator_z_normalize(data_set_location, data_set_location, True)
    c = cv.cross_validator(5, l, "LTOR_MART_min_max")
    score_file = "/lv_local/home/sgregory/LTOR_MART_min_max/test_scores_trec_format/LAMBDAMART/final_score_combined.txt"

    pool = p(2)

    gg = d.lambda_mart_stats_handler("01", 0.1,c)
    aa = d.lambda_mart_stats_handler("005", 0.05,c)
    bb = d.lambda_mart_stats_handler("001", 0.01, c)

    chosen_models = gg.recover_models_per_fold("/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART",
                                               "/lv_local/home/sgregory/LTOR_MART_min_max/test_scores_trec_format/LAMBDAMART/")
    f = partial(simulation, chosen_models, data_set_location, q.query_to_fold_index, score_file,"/lv_local/home/sgregory/LTOR_MART_min_max/competition","/lv_local/home/sgregory/LTOR_MART_min_max/new_scores/","/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART/")

    g_input = [gg,aa,bb]
    results = pool.map(f,g_input)#[simulation(chosen_models,data_set_location,q.query_to_fold_index,score_file,"/lv_local/home/sgregory/LTOR_MART_min_max/competition","/lv_local/home/sgregory/LTOR_MART_min_max/new_scores","/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART/",gg)]#pool.map(f, g_input)
    for result in results:
        write_res_to_file(result,"LAMDAMART")

