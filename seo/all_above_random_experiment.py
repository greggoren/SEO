from functools import partial
from multiprocessing import Pool as p
import os
import all_above_competition_maker_lbda as scm
import all_above_competition_maker_svm as lcm
import letor_fold_creator_min_max_normalize as lfc
import query_to_fold as qtf
from model_running import cross_validator as cv
import all_above_stat_handler_svm as aashs
import all_above_stat_handler_lbda as aashl
import relevance_index as ri


def lbda_simulation(chosen_models, data_set_location, query_to_fold_index, score_file, c_d_loc, new_scores_path, models_path, rel_index,alpha,budget_creator):

    c = scm.competition_maker(12, budget_creator, score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index, c_d_loc + "/" + budget_creator.model, new_scores_path + "/" + budget_creator.model, models_path)
    return c.competition("/lv_local/home/sgregory/LTOR_MART_min_max/new_scores/"+budget_creator.model+"/final",rel_index,alpha)

def svm_simulation(chosen_models,data_set_location,query_to_fold_index,score_file,rel_index,alpha,mapped_args):
    items_holder, budget_creator = mapped_args
    c = lcm.competition_maker(12, budget_creator, score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    return c.competition(items_holder,rel_index,alpha)

def write_res_to_file(result,model):
    for key in result:
        if not os.path.exists(model+"/"+key):
            os.makedirs(model+"/"+key)
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

def determine_argument_pairs(file_handlers,item_holders):
    final_pairing_list = []
    for file_handler in file_handlers:
        for meta_item_holder in item_holders:
            key = meta_item_holder.keys()[0]
            if key == file_handler.model:
                final_pairing_list.append((meta_item_holder[key],file_handler))
    return final_pairing_list


def sum_lists(list_a,list_b):
    return [a + b for a,b in zip(list_a,list_b)]

def average_list(list_a,iterations):
    return [float(a)/iterations for a in list_a]

def sum_dicts(x,y):
    return {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}

def average_dict(dict_a,iterations):
    return {k: float(dict_a.get(k, 0))/iterations for k in set(dict_a)}

if __name__ == "__main__":
    data_set_location = "/lv_local/home/sgregory/letor_fixed1"
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator(data_set_location, data_set_location, True)
    c = cv.cross_validator(5, l, "LTOR_MART_min_max")


    lbda_score_file = "/lv_local/home/sgregory/LTOR_MART_min_max/test_scores_trec_format/LAMBDAMART/final_score_combined.txt"
    svm_score_file = lbda_score_file #"/lv_local/home/sgregory/LTOR1/test_scores_trec_format/SVM/final_score_combined.txt"
    rel_index = ri.relevance_index("qrels")
    rel_index.create_relevance_index()
    pool = p(3)
    alphas =[5,10,20,30,40,50,60]
    gg = aashl.all_above_stat_handler_lbda("01", 0.1,c)
    aa = aashl.all_above_stat_handler_lbda("005", 0.05,c)
    bb = aashl.all_above_stat_handler_lbda("001", 0.01, c)
    svm_gg = aashs.all_above_stat_handler("01",0.1)
    svm_aa = aashs.all_above_stat_handler("005", 0.05)
    svm_bb = aashs.all_above_stat_handler("001", 0.01)

    lbda_chosen_models = gg.recover_models_per_fold("/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART",
                                               "/lv_local/home/sgregory/LTOR_MART_min_max/test_scores_trec_format/LAMBDAMART/")
    svm_chosen_models = svm_gg.recover_models_per_fold("/lv_local/home/sgregory/LTOR1/models/SVM",
                                               "/lv_local/home/sgregory/LTOR1/test_scores_trec_format/SVM/")
    #lbda_simulation(lbda_chosen_models, data_set_location, q.query_to_fold_index, lbda_score_file, "/lv_local/home/sgregory/LTOR_MART_min_max/competition", "/lv_local/home/sgregory/LTOR_MART_min_max/new_scores/", "/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART/",rel_index.rel_index,gg)


    lbda_g_input = [gg, aa, bb]
    svm_handlers_input = [svm_gg,svm_aa,svm_bb]
    iterations = 10
    lbda_final_results = {}
    svm_final_results = {}
    for alpha in alphas:
        lbda_f = partial(lbda_simulation, lbda_chosen_models, data_set_location, q.query_to_fold_index, lbda_score_file,
                         "/lv_local/home/sgregory/LTOR_MART_min_max/competition",
                         "/lv_local/home/sgregory/LTOR_MART_min_max/new_scores/",
                         "/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART/", rel_index.rel_index, alpha)
        for i in range(iterations):
            meta_results = pool.map(lbda_f, lbda_g_input)#[simulation(chosen_models,data_set_location,q.query_to_fold_index,score_file,"/lv_local/home/sgregory/LTOR_MART_min_max/competition","/lv_local/home/sgregory/LTOR_MART_min_max/new_scores","/lv_local/home/sgregory/LTOR_MART_min_max/models/LAMBDAMART/",gg)]#pool.map(f, g_input)
            lbda_results = [meta_result[0] for meta_result in meta_results]
            item_holders = [meta_result[1] for meta_result in meta_results]
            svm_g_input = determine_argument_pairs(svm_handlers_input,item_holders)
            svm_f =partial(svm_simulation, svm_chosen_models, data_set_location, q.query_to_fold_index, svm_score_file,rel_index.rel_index,alpha)
            svm_results = pool.map(svm_f,svm_g_input)
            if not lbda_final_results:
                for result in lbda_results:
                    lbda_final_results[result.keys()[0]]= result[result.keys()[0]]
            else:
                for result in lbda_results:
                    key = result.keys()[0]
                    for stat in result[key]:
                        try:
                            if isinstance(result[key][stat], tuple):
                                lbda_final_results[key][stat]=(lbda_final_results[key][stat][0], sum_lists(lbda_final_results[key][stat][1], result[key][stat][1]))
                            else:
                                lbda_final_results[key][stat]= sum_dicts(lbda_final_results[key][stat], result[key][stat])
                        except:
                            print result[key]
                            print stat
            if not svm_final_results:
                for result in svm_results:
                    svm_final_results[result.keys()[0]] = result[result.keys()[0]]
            else:
                for result in svm_results:
                    key = result.keys()[0]
                    for stat in result[key]:
                        try:
                            if isinstance(result[key][stat], tuple):
                                svm_final_results[key][stat]=(svm_final_results[key][stat][0], sum_lists(svm_final_results[key][stat][1], result[key][stat][1]))
                            else:
                                svm_final_results[key][stat]= sum_dicts(svm_final_results[key][stat], result[key][stat])
                        except:
                            print result[key]
                            print stat
        for key in lbda_final_results:
            for stat in lbda_final_results[key]:
                if isinstance(svm_final_results[key][stat], tuple):
                    lbda_final_results[key][stat] =(lbda_final_results[key][stat][0], average_list(lbda_final_results[key][stat][1], iterations))
                else:
                    lbda_final_results[key][stat] = average_dict(lbda_final_results[key][stat], iterations)
        write_res_to_file(lbda_final_results, "LAMDAMART_all_above_lbda_"+str(alpha))

        for key in svm_final_results:
            for stat in svm_final_results[key]:
                if isinstance(svm_final_results[key][stat], tuple):
                    svm_final_results[key][stat] =(svm_final_results[key][stat][0], average_list(svm_final_results[key][stat][1], iterations))
                else:
                    svm_final_results[key][stat] = average_dict(svm_final_results[key][stat], iterations)
        write_res_to_file(svm_final_results,"SVM_all_above_lbda_"+str(alpha))
