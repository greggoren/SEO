if __name__=="__main__":
    alphas = ["01"]
    folders = ["minmax","minmax_euc","minmax_all_euc","minmax_all","zscore","zscore_all","zscore_euc","zscore_all_euc"]
    file_name = "orig.txt"
    lines = {}

    for alpha in alphas:
        for folder in folders:
            number_of_lines =0
            with open(folder+"/"+alpha+"/"+file_name) as results_file:
                for result in results_file:
                    splited = result.split()
                    if not lines.get(splited[0],False):
                        lines[splited[0]]=[]
                    lines[splited[0]].append(splited[1])
                    number_of_lines+=1
                if number_of_lines<12:
                    for i in range(6,13):
                        lines[str(i)].append("EMPTY")
    cos_res_file = "kendal_with_original_list_measure_result_01.csv"
    result_file_final = open(cos_res_file,'w')
    result_file_final.write("iteration,minmax,minmax_euc,minmax_all_euc,minmax_all,zscore,zscore_all,zscore_euc,zscore_all_euc\n")
    for line in lines:
        writeline = ""
        writeline+=line+","
        writeline+=",".join(lines[line])
        result_file_final.write(writeline+"\n")
    result_file_final.close()

