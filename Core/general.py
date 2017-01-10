from Rexy.config import max_tag_density


def cal_sim_product(tags1, tags2, return_diff=True):
    key1 = tags1.keys()
    key2 = tags2.keys()
    common_keys = key1 & key2
    # calculate the similarity based on the distance between densities
    avg = sum(1 - abs(tags1[id_] - tags2[id_]) / max_tag_density for id_ in common_keys)
    final_result = (avg + len(common_keys) / min(len(tags1), len(tags2))) / 2
    if return_diff:
        diff_p1p2 = {k: tags1[k] for k in key1 - key2}
        diff_p2p1 = {k: tags2[k] for k in key2 - key1}
        return final_result, diff_p1p2, diff_p2p1
    return final_result
