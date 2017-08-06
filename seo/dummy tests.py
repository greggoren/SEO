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
    """
    cache= initilize_cache_of_normaliztion(10)
    test = []
    weights = cache[1]
    zipped = zip(weights, test)
    temporary_list = []
    for i, list in zipped:
        temporary_list.append([i * d for d in list])
    competitor_refrence_vector = [sum(i) for i in zip(*temporary_list)]
    print weights
    print competitor_refrence_vector"""
    features_index =[100,25,43,44,555]
    reference_vector = [2,55,100,600,555]

    changed_vector = [(abs(a - b), features_index.index(a)) for a, b in
                      zip(features_index, reference_vector)]
    sorted_changed_vector = sorted(changed_vector, key=lambda x: x[0], reverse=True)[:2]
    print [a[1] for a in sorted_changed_vector]