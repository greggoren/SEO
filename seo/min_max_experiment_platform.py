import query_to_fold as qtf

import winner_refrence_point as d

import competition_maker_winner_reference as cm
from multiprocessing import Pool as p
from functools import partial
import sys
import plot_maker as pm
import os


def simulation(chosen_models,data_set_location,query_to_fold_index,score_file,budget_creator):

    c = cm.competition_maker_winner_reference(12, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    return c.competition(budget_creator.model)


if __name__ == "__main__":
    iterations = int(sys.argv[1])
    #data_set_location = "C:/study/letor_fixed2"
    data_set_location = "/lv_local/home/sgregory/letor_fixed1"
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()

    #score_file = "C:/study/simulation_z_data/test_scores_trec_format/SVM/final_score_combined.txt"
    score_file = "/lv_local/home/sgregory/LTOR1/test_scores_trec_format/SVM/final_score_combined.txt"

    pool = p(2)



    lg = d.winner_reference_point("002", 0.02)
    chosen_models = lg.recover_models_per_fold("/lv_local/home/sgregory/LTOR1/models/SVM",
                                               "/lv_local/home/sgregory/LTOR1/test_scores_trec_format/SVM/")
    #chosen_models = lg.recover_models_per_fold("C:/study/simulation_z_data/models/SVM",
    #                                          "C:/study/simulation_z_data/test_scores_trec_format/SVM/")
    f = partial(simulation, chosen_models, data_set_location, q.query_to_fold_index, score_file)

    max_dist = 0.001
    for i in range(iterations):
        ag = d.winner_reference_point("A",max_dist)
        gg = d.winner_reference_point("B", max_dist+0.001)
        bg = d.winner_reference_point("C", max_dist+0.002)
        ff = d.winner_reference_point("D", max_dist+0.003)
        g_input = [ag, bg, gg, ff]
        results = pool.map(f, g_input)
        plot = pm.plot_maker()
        if not os.path.exists("min_max/"+str(max_dist)):
            os.makedirs("min_max/"+str(max_dist))
        plot.create_relvant_plots(results,"min_max/"+str(max_dist),max_dist)
        max_dist+=0.004
