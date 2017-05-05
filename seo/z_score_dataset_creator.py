from seo import letor_fold_creator_z_normalize as lfc
from model_running import cross_validator as cv
if __name__ == "__main__":

    data_set_location = "/lv_local/home/sgregory/letor"

    new_data_set_location = "/lv_local/home/sgregory/letor_fixed2"
    l = lfc.letor_folds_creator_z_normalize(data_set_location,new_data_set_location,False)
    c = cv.cross_validator(5,l,"LTOR2")
    #c.k_fold_cross_validation("SVM","qrels")


