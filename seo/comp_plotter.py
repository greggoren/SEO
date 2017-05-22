import pandas as pd
import matplotlib.pyplot as plt
import os

def parse_file(file):
    x_axis = []
    y_axis = []
    with open(file) as records:
        for record in records:
            splited = record.split()
            x_axis.append(int(splited[0]))
            y_axis.append(float(splited[1]))
    return x_axis,y_axis


def parse_file_hist(file):
    x_axis = []
    y_axis = []
    with open(file) as records:
        for record in records:
            splited = record.split()
            x_axis.append(int(splited[0]))
            y_axis.append(int(splited[1]))
    return x_axis,y_axis

def create_relevant_plot(results,label,location,title):
    if not os.path.exists(location):
        os.makedirs(location)
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel(label)
    svm_res = results["SVM"]
    lbda_res = results["LAMBDA"]
    ax.plot(svm_res[0],svm_res[1],"g")
    ax.plot(lbda_res[0], lbda_res[1],"b")
    plt.savefig(location + "/"+label.replace(" ","")+".jpg")
    plt.clf()

def create_hist_graph(main_folder):
    hist_names = [("originalwinnerrank", "Original Winner Final Rank"),
                  ("whoisthewinner", "Final Winner Original Rank")]
    sub_folders = ["01", "001", "005"]
    for sub_folder in sub_folders:
        for hist in hist_names:
            results={}
            file_svm = main_folder + "/SVM/" + sub_folder + "/" + hist[0] + ".txt"
            x, y = parse_file_hist(file_svm)
            results["SVM"] = (x, y)
            file_lbda = main_folder + "/LAMDAMART/" + sub_folder + "/" + hist[0] + ".txt"
            results["LAMBDA"] = (parse_file_hist(file_lbda))
            create_histograms(results, hist[0], "results/"+sub_folder, hist[1])

def run_on_folders(main_folder):
    plot_names = [("avg_f","Feature Changed","Average Number Of Features Changed"),("cos","Average Cosine Distance","Average Diameter Of Competitors"),("kendall","Kendall Tau Measure","Average Kendall-Tau With Last Iteration"),("orig","Kendall Tau","Average Kendall-Tau With Original List"),("winner","Change Rate","Winner Change Frequency")]
    sub_folders = ["01","001","005"]
    for sub_folder in sub_folders:
        for plot_name in plot_names:
            results = {}
            file_svm = main_folder+"/SVM/"+sub_folder+"/"+plot_name[0]+".txt"
            x,y=parse_file(file_svm)
            results["SVM"] = (x,y)
            file_lbda = main_folder+"/LAMDAMART/"+sub_folder+"/"+plot_name[0]+".txt"
            results["LAMBDA"] = (parse_file(file_lbda))
            create_relevant_plot(results,plot_name[1],"results/"+sub_folder,plot_name[2])



def create_histograms(results,label,location,title):
    plt.figure(1)
    plt.title(title)

    plt.subplot(221)

    plt.title("SVM_RANK")
    plt.bar(results["SVM"][0], results["SVM"][1], align="center")
    plt.subplot(222)
    plt.title("LAMBDA_MART")
    plt.bar(results["LAMBDA"][0], results["LAMBDA"][1], align="center")

    plt.savefig(location + "/"+label+".jpg")
    plt.clf()


if __name__=="__main__":
    main_folder = "C:/study/res/random"
    run_on_folders(main_folder)
    create_hist_graph(main_folder)
