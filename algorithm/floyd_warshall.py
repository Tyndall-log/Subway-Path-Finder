import numpy as np


def floyd_warshall(dist_matrix: np.ndarray) -> np.ndarray:
	n = len(dist_matrix)
	for k in range(n):
		for i in range(n):
			for j in range(n):
				dist_matrix[i, j] = min(dist_matrix[i, j], dist_matrix[i, k] + dist_matrix[k, j])
	return dist_matrix
