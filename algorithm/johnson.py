import numpy as np
from .dijkstra import dijkstra, dijkstra_matrix, dijkstra_with_path, dijkstra_matrix_with_path


def johnson_simple(dist_matrix: np.ndarray) -> np.ndarray:
	n = len(dist_matrix)
	
	# 거리 행렬을 그래프로 변환
	graph = {i: {} for i in range(n)}
	for i in range(n):
		for j in range(n):
			if dist_matrix[i, j] != np.inf and i != j:
				graph[i][j] = dist_matrix[i, j]
	
	# 모든 쌍 최단 경로 계산
	all_pairs_dist = np.full((n, n), np.inf)
	for u in range(n):
		dist_from_u = dijkstra(graph, u, n)
		for v in range(n):
			all_pairs_dist[u, v] = dist_from_u[v]
	
	return all_pairs_dist


def johnson_simple_matrix(dist_matrix: np.ndarray) -> np.ndarray:
	n = len(dist_matrix)
	
	# 거리 행렬을 그래프로 변환
	graph = {i: {} for i in range(n)}
	for i in range(n):
		for j in range(n):
			if dist_matrix[i, j] != np.inf and i != j:
				graph[i][j] = dist_matrix[i, j]
	
	# 모든 쌍 최단 경로 계산
	all_pairs_dist = np.full((n, n), np.inf)
	for u in range(n):
		dist_from_u = dijkstra_matrix(dist_matrix, u, n)
		for v in range(n):
			all_pairs_dist[u, v] = dist_from_u[v]
	
	return all_pairs_dist


def reconstruct_path(previous: np.ndarray, start: int, end: int) -> list:
	path = []
	current = end
	while current != -1:
		path.append(current)
		current = previous[current]
	path.reverse()
	return path if path[0] == start else []


def johnson_simple_with_path2(time_matrix: np.ndarray, path_matrix: np.ndarray):
	n = len(time_matrix)
	
	# 최단 거리 및 경로 저장을 위한 배열 초기화
	shortest_paths = np.full((n, n), np.inf)
	all_paths = np.empty((n, n), dtype=object)
	
	for i in range(n):
		for j in range(n):
			all_paths[i, j] = []
	
	# 모든 쌍 최단 경로 계산
	for u in range(n):
		dist_from_u, previous = dijkstra_matrix_with_path(time_matrix, u, n)
		for v in range(n):
			shortest_paths[u, v] = dist_from_u[v]
			if u != v and dist_from_u[v] != np.inf:
				all_paths[u, v] = reconstruct_path(previous, u, v)
	
	# 결과를 원래 행렬에 반영
	for i in range(n):
		for j in range(n):
			time_matrix[i, j] = shortest_paths[i, j]
			path_matrix[i, j] = all_paths[i, j]


def johnson_simple_with_path(time_matrix: np.ndarray, path_matrix: np.ndarray):
	n = len(time_matrix)
	
	# 그래프 생성
	graph = {i: {} for i in range(n)}
	for i in range(n):
		for j in range(n):
			if time_matrix[i, j] != float('inf') and i != j:
				graph[i][j] = time_matrix[i, j]
	
	# 최단 거리 및 경로 저장을 위한 배열 초기화
	shortest_paths = np.full((n, n), float('inf'))
	all_paths = np.empty((n, n), dtype=object)
	
	for i in range(n):
		for j in range(n):
			all_paths[i, j] = []
	
	# 모든 쌍 최단 경로 계산
	for u in range(n):
		dist_from_u, previous = dijkstra_with_path(graph, u, n)
		for v in range(n):
			shortest_paths[u, v] = dist_from_u[v]
			if u != v and dist_from_u[v] != float('inf'):
				all_paths[u, v] = reconstruct_path(previous, u, v)
	
	# 결과를 원래 행렬에 반영
	for i in range(n):
		for j in range(n):
			time_matrix[i, j] = shortest_paths[i, j]
			path_matrix[i, j] = all_paths[i, j]
