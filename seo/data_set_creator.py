
import sys
from seo import letor_fold_creator_min_max_normalize as lfc
from model_running import cross_validator as cv
from seo import exponential_budget_cost_creator as e
if __name__ == "__main__":

    data_set_location = "/lv_local/home/sgregory/letor"
    new_data_set_location = "/lv_local/home/sgregory/letor_fixed1"
    l = lfc.letor_folds_creator(data_set_location,new_data_set_location,True)
    c = cv.cross_validator(5,l,"LTOR1")
    c.k_fold_cross_validation("SVM","qrels")


