import scipy.linalg
a = [[4, 7, 1], [3, 4, 7], [2, 0, 7]]
(lu, piv, q) = scipy.linalg.lu(a=a, permute_l=False, p_indices=False)