import matplotlib.pyplot as plt
class plot_maker:

    def __init__(self):
        ""

    def create_relvant_plots(self,results,location,max_dist):
        fig = plt.figure()
        fig.suptitle('Average Kendall-tau measure', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Kendal-tau')

        for result in results:

            key = result.keys()[0]
            print result
            kendal_stats = result[key]["kendall"]
            if key == "A":
                ax.plot(kendal_stats[0], kendal_stats[1], 'g')
            elif key == "B":
                ax.plot(kendal_stats[0], kendal_stats[1], 'r')
            elif key == "C":
                ax.plot(kendal_stats[0], kendal_stats[1], 'y')
            elif key == "D":
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
            if key == "A":
                ax.plot(winner_stats[0], winner_stats[1], 'g')
            elif key == "B":
                ax.plot(winner_stats[0], winner_stats[1], 'r')
            elif key == "C":
                ax.plot(winner_stats[0], winner_stats[1], 'y')
            elif key == "D":
                ax.plot(winner_stats[0], winner_stats[1], 'k')
            else:
                ax.plot(winner_stats[0], winner_stats[1], 'b')

        plt.savefig(location+"/winner_swap.jpg")
        plt.clf()
        fig = plt.figure()
        fig.suptitle('Average cosine distance', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Cosine distance')
        for result in results:
            key = result.keys()[0]
            cos_stats = result[key]["cos"]
            if key == "A":
                ax.plot(cos_stats[0], cos_stats[1], 'g')
            elif key == "B":
                ax.plot(cos_stats[0], cos_stats[1], 'r')
            elif key == "C":
                ax.plot(cos_stats[0], cos_stats[1], 'y')
            elif key == "D":
                ax.plot(cos_stats[0], cos_stats[1], 'k')
            else:
                ax.plot(cos_stats[0], cos_stats[1], 'b')
        plt.savefig(location+"/cos_dist.jpg")
        plt.clf()

        fig = plt.figure()
        fig.suptitle('Average Kendall-tau with original rank', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Kendal tau')
        for result in results:

            key = result.keys()[0]
            orig_stats = result[key]["orig"]
            if key == "A":
                ax.plot(orig_stats[0], orig_stats[1], 'g')
            elif key == "B":
                ax.plot(orig_stats[0], orig_stats[1], 'r')
            elif key == "C":
                ax.plot(orig_stats[0], orig_stats[1], 'y')
            elif key == "D":
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
            if key == "A":
                ax.plot(orig_stats[0], orig_stats[1], 'g')
            elif key == "B":
                ax.plot(orig_stats[0], orig_stats[1], 'r')
            elif key == "C":
                ax.plot(orig_stats[0], orig_stats[1], 'y')
            elif key == "D":
                ax.plot(orig_stats[0], orig_stats[1], 'k')
            else:
                ax.plot(orig_stats[0], orig_stats[1], 'b')
        plt.savefig(location+"/orig_win_rank.jpg")
        plt.clf()

        plt.figure(1)
        plt.title("originl winner final rank histogram")
        plot_number = 1
        for result in results:
            key = result.keys()[0]
            plt.subplot(220 + plot_number)
            originl_winner_rank = result[key]["originalwinnerrank"]
            if key == "A":
                plt.title(str(max_dist))

            elif key == "B":
                plt.title(str(max_dist+0.001))

            elif key == "C":
                plt.title(str(max_dist+0.002))

            elif key == "D":
                plt.title(str(max_dist+0.003))

            plt.bar(originl_winner_rank.keys(), originl_winner_rank.values(), align="center")
            plot_number += 1
        plt.savefig(location+"/orig_win_rank_hist.jpg")
        plt.clf()

        plt.title("final winner original rank histogram")
        plot_number = 1
        for result in results:
            key = result.keys()[0]
            plt.subplot(220 + plot_number)
            last_winner_rank = result[key]["whoisthewinner"]
            if key == "A":
                plt.title(str(max_dist))

            elif key == "B":
                plt.title(str(max_dist+0.001))

            elif key == "C":
                plt.title(str(max_dist+0.002))

            elif key == "D":
                plt.title(str(max_dist+0.003))
            plt.bar(last_winner_rank.keys(), last_winner_rank.values(), align="center")
            plot_number += 1
        plt.savefig(location+"/final_win_orig_rank_hist.jpg")

        fig = plt.figure()
        fig.suptitle('Number of features to change', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('Iterations')
        ax.set_ylabel('feature number')
        for result in results:
            key = result.keys()[0]
            cos_stats = result[key]["avg_f"]
            if key == "A":
                ax.plot(cos_stats[0], cos_stats[1], 'g')
            elif key == "B":
                ax.plot(cos_stats[0], cos_stats[1], 'r')
            elif key == "C":
                ax.plot(cos_stats[0], cos_stats[1], 'y')
            elif key == "D":
                ax.plot(cos_stats[0], cos_stats[1], 'k')
            else:
                ax.plot(cos_stats[0], cos_stats[1], 'b')
        plt.savefig(location+"/number_of_features.jpg")
        plt.clf()
