
from seo import query_to_fold as qtf

from seo import winner_refrence_point as d

from seo import competition_maker_winner_reference as cm
from multiprocessing import Pool as p
from functools import partial
import matplotlib.pyplot as plt
def simulation(chosen_models,data_set_location,query_to_fold_index,score_file,budget_creator):

    c = cm.competition_maker_winner_reference(12, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    return c.competition(budget_creator.model)


if __name__ == "__main__":

    data_set_location = "C:/study/letor_fixed1"
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()

    score_file = "C:/study/simulation_data/test_scores_trec_format/SVM/final_score_combined.txt"

    pool = p(2)


    lg = d.winner_reference_point("002", 0.02)
    gg = d.winner_reference_point("001", 0.1)
    bg = d.winner_reference_point("0005", 0.05)
    ff = d.winner_reference_point("0008", 0.005)

    chosen_models = lg.recover_models_per_fold("C:/study/simulation_data/models/SVM",
                                               "C:/study/simulation_data/test_scores_trec_format/SVM/")
    f = partial(simulation, chosen_models, data_set_location, q.query_to_fold_index, score_file)

    g_input = [gg, bg, lg, ff]
    results = pool.map(f, g_input)

    fig = plt.figure()
    fig.suptitle('Average Kendall-tau measure', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Kendal-tau')

    for result in results:

        key = result.keys()[0]
        print result
        kendal_stats = result[key]["kendall"]
        if key == "001":
            ax.plot(kendal_stats[0], kendal_stats[1], 'g')
        elif key == "002":
            ax.plot(kendal_stats[0], kendal_stats[1], 'r')
        elif key == "003":
            ax.plot(kendal_stats[0], kendal_stats[1], 'y')
        elif key == "0005":
            ax.plot(kendal_stats[0], kendal_stats[1], 'k')
        else:
            ax.plot(kendal_stats[0], kendal_stats[1], 'b')
    plt.savefig("kendall_tau.jpg")
    plt.clf()
    fig = plt.figure()
    fig.suptitle('Average winner changing', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('winner changed')
    for result in results:

        key = result.keys()[0]

        winner_stats = result[key]["winner"]
        if key == "001":
            ax.plot(winner_stats[0], winner_stats[1], 'g')
        elif key == "002":
            ax.plot(winner_stats[0], winner_stats[1], 'r')
        elif key == "003":
            ax.plot(winner_stats[0], winner_stats[1], 'y')
        elif key == "0005":
            ax.plot(winner_stats[0], winner_stats[1], 'k')
        else:
            ax.plot(winner_stats[0], winner_stats[1], 'b')

    plt.savefig("winner_swap.jpg")
    plt.clf()
    fig = plt.figure()
    fig.suptitle('Average cosine distance', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cosine distance')
    for result in results:
        key = result.keys()[0]
        cos_stats = result[key]["cos"]
        if key == "001":
            ax.plot(cos_stats[0], cos_stats[1], 'g')
        elif key == "002":
            ax.plot(cos_stats[0], cos_stats[1], 'r')
        elif key == "003":
            ax.plot(cos_stats[0], cos_stats[1], 'y')
        elif key == "0005":
            ax.plot(cos_stats[0], cos_stats[1], 'k')
        else:
            ax.plot(cos_stats[0], cos_stats[1], 'b')
    plt.savefig("cos_dist.jpg")
    plt.clf()

    fig = plt.figure()
    fig.suptitle('Average Kendall-tau with original rank', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Kendal tau')
    for result in results:

        key = result.keys()[0]
        orig_stats = result[key]["orig"]
        if key == "001":
            ax.plot(orig_stats[0], orig_stats[1], 'g')
        elif key == "002":
            ax.plot(orig_stats[0], orig_stats[1], 'r')
        elif key == "003":
            ax.plot(orig_stats[0], orig_stats[1], 'y')
        elif key == "0005":
            ax.plot(orig_stats[0], orig_stats[1], 'k')
        else:
            ax.plot(orig_stats[0], orig_stats[1], 'b')
    plt.savefig("orig_tau.jpg")
    plt.clf()
    fig = plt.figure()
    fig.suptitle('Average original winner rank', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('winner rank')
    for result in results:

        key = result.keys()[0]
        orig_stats = result[key]["win_rank"]
        if key == "001":
            ax.plot(orig_stats[0], orig_stats[1], 'g')
        elif key == "002":
            ax.plot(orig_stats[0], orig_stats[1], 'r')
        elif key == "003":
            ax.plot(orig_stats[0], orig_stats[1], 'y')
        elif key == "0005":
            ax.plot(orig_stats[0], orig_stats[1], 'k')
        else:
            ax.plot(orig_stats[0], orig_stats[1], 'b')
    plt.savefig("orig_win_rank.jpg")
    plt.clf()

    plt.figure(1)
    plt.title("originl winner final rank histogram")
    plot_number = 1
    for result in results:
        label = ""
        key = result.keys()[0]
        plt.subplot(220 + plot_number)
        originl_winner_rank = result[key]["originalwinnerrank"]
        if key == "001":
            plt.title("0.1")
            label = "0.1"
        elif key == "002":
            plt.title("0.02")
            label = "0.02"
        elif key == "0005":
            plt.title("0.05")
            label = "0.05"
        elif key == "003":
            plt.title("0.03")
            label = "0.03"
        else:
            plt.title("0.005")
            label = "0.005"
        plt.bar(originl_winner_rank.keys(), originl_winner_rank.values(), align="center")
        plot_number += 1
    plt.savefig("orig_win_rank_hist.jpg")
    plt.clf()

    plt.title("final winner original rank histogram")
    plot_number = 1
    for result in results:
        key = result.keys()[0]
        plt.subplot(220 + plot_number)
        last_winner_rank = result[key]["whoisthewinner"]
        if key == "001":
            plt.title("0.1")
            label = "0.1"
        elif key == "002":
            plt.title("0.02")
            label = "0.02"
        elif key == "0005":
            plt.title("0.05")
            label = "0.05"
        elif key == "003":
            plt.title("0.03")
            label = "0.03"
        else:
            plt.title("0.005")
            label = "0.005"
        plt.bar(last_winner_rank.keys(), last_winner_rank.values(), align="center")
        plot_number += 1
    plt.savefig("final_win_orig_rank_hist.jpg")

    fig = plt.figure()
    fig.suptitle('Number of features to change', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('feature number')
    for result in results:
        key = result.keys()[0]
        cos_stats = result[key]["avg_f"]
        if key == "001":
            ax.plot(cos_stats[0], cos_stats[1], 'g')
        elif key == "002":
            ax.plot(cos_stats[0], cos_stats[1], 'r')
        elif key == "003":
            ax.plot(cos_stats[0], cos_stats[1], 'y')
        elif key == "0005":
            ax.plot(cos_stats[0], cos_stats[1], 'k')
        else:
            ax.plot(cos_stats[0], cos_stats[1], 'b')
    plt.savefig("number_of_features.jpg")
    plt.clf()
