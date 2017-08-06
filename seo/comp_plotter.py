import pandas as pd
import matplotlib.pyplot as plt
import os
import math

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
            try:
                x_axis.append(int(splited[0]))
            except:
                x_axis.append(splited[0])
            y_axis.append(math.ceil(float(splited[1])))
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
                  ("whoisthewinner", "Final Winner Original Rank"),("finalwinnerrel","Final Winner Original Relevance"),("originalrelhist","Original Winner Relevance Hist")]
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
    plot_names = [("avg_f","Feature Changed","Average Number Of Features Changed"),("cos","Average Cosine Distance","Average Cosine Distance Of Competitors"),("kendall","Kendall Tau Measure","Average Kendall-Tau With Last Iteration"),("orig","Kendall Tau","Average Kendall-Tau With Original List"),("winner","Change Rate","Winner Change Frequency")]
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


def create_combined_graphs(main_folder):
    plot_names = [("avg_f", "Feature Changed", "Average Number Of Features Changed"),
                  ("cos", "Average Cosine Distance", "Average Cosine Distance Of Competitors"),
                  ("kendall", "Kendall Tau Measure", "Average Kendall-Tau With Last Iteration"),
                  ("orig", "Kendall Tau", "Average Kendall-Tau With Original List"),
                  ("winner", "Change Rate", "Winner Change Frequency")]
    sub_folders = ["01", "001", "005"]

    for plot_name in plot_names:
        i = 1
        plt.figure(figsize=(13, 10)).suptitle(plot_name[2], fontsize=14, fontweight='bold')

        for sub_folder in sub_folders:
            results = {}
            file_svm = main_folder + "/SVM/" + sub_folder + "/" + plot_name[0] + ".txt"
            x, y = parse_file(file_svm)
            results["SVM"] = (x, y)
            file_lbda = main_folder + "/LAMDAMART/" + sub_folder + "/" + plot_name[0] + ".txt"
            results["LAMBDA"] = (parse_file(file_lbda))
            plt.subplot(220+i)
            plt.title(sub_folder.replace("0","0.",1))
            plt.ylabel(plot_name[1])
            plt.xlabel("Iterations")
            svm_res = results["SVM"]
            lbda_res = results["LAMBDA"]
            plt.plot(svm_res[0], svm_res[1], "g",label="SVMRank")
            plt.plot(lbda_res[0], lbda_res[1], "b",label="LambdaMart")
            plt.legend(loc="best")
            i += 1
        plt.savefig(main_folder + "/" + plot_name[0].replace(" ", "") + ".jpg")
        plt.clf()

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

def create_csv_files(main_folder):
    sub_folders = ["01", "001", "005"]
    data = {}
    data["SVM"]={}
    data["LAMBDAMART"]={}
    for sub_folder in sub_folders:
        joined_file = "results/"+sub_folder+"/decorasc.csv"
        file_svm = main_folder + "/SVM/" + sub_folder + "/decOrAsc.txt"
        file_lbda = main_folder + "/LAMDAMART/" + sub_folder + "/decOrAsc.txt"
        with open(file_svm) as svm_data:
            for line in svm_data:
                splited = line.split()
                data["SVM"][splited[0]] = splited[1]
        with open(file_lbda) as lbda_data:
            for line in lbda_data:
                splited = line.split()
                data["LAMBDAMART"][splited[0]] = splited[1]
        with open(joined_file,'w') as out:
            out.write("EVENT,SVM,LAMBDAMART\n")
            for key in data["SVM"]:
                if key=="dec":
                    event = "Decreased"
                else:
                    event= "Increased"
                out.write(event+","+data["SVM"][key]+","+data["LAMBDAMART"][key]+"\n")

def create_combined_histograms(main_folder):
    hist_names = [("originalwinnerrank", "Original Winner Final Rank"),
                  ("whoisthewinner", "Final Winner Original Rank"),
                  ("finalwinnerrel", "Final Winner Original Relevance"),
                  ("originalrelhist", "Original Winner Relevance Hist")]
    sub_folders = ["01", "001", "005"]
    for hist in hist_names:
        i =1
        plt.figure(figsize=(13,10)).suptitle(hist[1], fontsize=14, fontweight='bold')
        for sub_folder in sub_folders:
            plt.title(sub_folder.replace("0","0.",1))
            results = {}
            file_svm = main_folder + "/SVM/" + sub_folder + "/" + hist[0] + ".txt"
            x, y = parse_file_hist(file_svm)
            results["SVM"] = (x, y)
            file_lbda = main_folder + "/LAMDAMART/" + sub_folder + "/" + hist[0] + ".txt"
            results["LAMBDA"] = (parse_file_hist(file_lbda))
            plt.subplot(220+i)
            plt.bar(results["SVM"][0], results["SVM"][1],width=0.3, align="center",color='g',label="SVMRank")
            t = [a -0.3 for a in results["LAMBDA"][0]]
            plt.bar(t, results["LAMBDA"][1], width=0.3, align="center", color='b',label="LambdaMart")
            plt.legend(loc='best')
            plt.ylabel("Number Of Queries")
            if hist[1].__contains__("Rel"):
                plt.xlabel("Relevance")
            else:
                plt.xlabel("Rank")
            i+=1
        plt.savefig(main_folder + "/" + hist[0] + ".jpg")
        plt.clf()

if __name__=="__main__":
    main_folder = "C:/study/res/svmlist"
    create_combined_graphs(main_folder)
    create_combined_histograms(main_folder)
    main_folder = "C:/study/res/lbdalist"
    create_combined_graphs(main_folder)
    create_combined_histograms(main_folder)
    #run_on_folders(main_folder)
    #create_hist_graph(main_folder)
    #create_csv_files(main_folder)