import query_to_fold as qtf
import os
import winner_refrence_point as d
#from seo import competition_maker as cm
import competition_maker_winner_reference as cm
from multiprocessing import Pool as p
from functools import partial
import matplotlib.pyplot as plt
def simulation(chosen_models,data_set_location,query_to_fold_index,score_file,budget_creator):

    c = cm.competition_maker_winner_reference(12, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    #c = cm.competition_maker(5, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    return c.competition(budget_creator.model)


if __name__ == "__main__":

    data_set_location_minmax = "C:/study/letor_fixed1"
    data_set_location_z_score = "C:/study/letor_fixed2"
    q = qtf.qtf(data_set_location_minmax)
    q.create_query_to_fold_index()

    score_file_minmax = "C:/study/simulation_data/test_scores_trec_format/SVM/final_score_combined.txt"

    pool = p(2)



    gg = d.winner_reference_point("05", 0.5)
    bg = d.winner_reference_point("001", 0.01)
    ff = d.winner_reference_point("01",0.1)

    #chosen_models_min_max = gg.recover_models_per_fold("C:/study/simulation_data/models/SVM",
    #                                           "C:/study/simulation_data/test_scores_trec_format/SVM/")

    #minmax = partial(simulation, chosen_models_min_max, data_set_location_minmax, q.query_to_fold_index, score_file_minmax)

    g_input = [gg, bg, ff]
#    results_minmax = pool.map(minmax, g_input)

    score_file_zscore = "C:/study/simulation_z_data/test_scores_trec_format/SVM/final_score_combined.txt"
    chosen_models_z_score = gg.recover_models_per_fold("C:/study/simulation_z_data/models/SVM","C:/study/simulation_z_data/test_scores_trec_format/SVM/")
    zscore = partial(simulation, chosen_models_z_score, data_set_location_z_score, q.query_to_fold_index, score_file_zscore)

    results_zscore = pool.map(zscore,g_input)

    minmax_result_location = "minmax_euc/"
    """for result in results_minmax:
        key = result.keys()[0]
        for stat in result[key]:
            if not os.path.exists(minmax_result_location+key+"/"):
                os.makedirs(minmax_result_location+key+"/")
            out_file = open(minmax_result_location+key+"/"+stat+".txt",'w')
            if len(result[key][stat])==2:
                for x,y in zip(result[key][stat][0],result[key][stat][1]):
                    out_file.write(str(x)+"\t"+str(y)+"\n" )
            else:
                for x,y in zip(result[key][stat].keys(),result[key][stat].values()):
                    out_file.write(str(x)+"\t"+str(y)+"\n")
            out_file.close()"""
    zscore_result_location = "zscore/"

    for result in results_zscore:
        key = result.keys()[0]
        for stat in result[key]:
            if not os.path.exists(zscore_result_location+key+"/"):
                os.makedirs(zscore_result_location+key+"/")
            out_file = open(zscore_result_location+key+"/"+stat+".txt",'w')
            try:
                if isinstance(result[key][stat], tuple):

                    for x,y in zip(result[key][stat][0],result[key][stat][1]):
                        out_file.write(str(x)+"\t"+str(y)+"\n")
                else:
                    for x,y in zip(result[key][stat].keys(),result[key][stat].values()):
                        out_file.write(str(x)+"\t"+str(y)+"\n")
            except:
                print result[key]
                print stat
            out_file.close()
