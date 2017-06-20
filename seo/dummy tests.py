def initilize_cache_of_normaliztion(number_of_competitors, alpha=60):
    cache_list_of_weights = {}
    for index in range(1, number_of_competitors):
        list_of_index = list((range(1, index )))
        temp_result = [1.0 / (obj + alpha) for obj in list_of_index]
        denominator = sum(temp_result)
        result = [float(obj) / denominator for obj in temp_result]
        cache_list_of_weights[index] = result
    return cache_list_of_weights


if __name__=="__main__":

    cache= initilize_cache_of_normaliztion(10)
    test = [[1,2,3],[1,1,1],[2,2,2]]
    weights = cache[4]
    zipped = zip(weights, test)
    temporary_list = []
    for i, list in zipped:
        temporary_list.append([i * d for d in list])
    competitor_refrence_vector = [sum(i) for i in zip(*temporary_list)]
    print weights
    print competitor_refrence_vector