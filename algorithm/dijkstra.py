import numpy as np
import heapq


def dijkstra(graph, source, n):
	distance = {i: np.inf for i in range(n)}
	distance[source] = 0
	priority_queue = [(0, source)]
	
	while priority_queue:
		current_distance, current_vertex = heapq.heappop(priority_queue)
		
		if current_distance > distance[current_vertex]:
			continue
		
		for neighbor, weight in graph[current_vertex].items():
			distance_via_u = current_distance + weight
			if distance_via_u < distance[neighbor]:
				distance[neighbor] = distance_via_u
				heapq.heappush(priority_queue, (distance_via_u, neighbor))
	
	return distance


def dijkstra_matrix(dist_matrix: np.ndarray, u: int, n: int) -> np.ndarray:
	dist = np.full(n, np.inf)
	dist[u] = 0
	visited = np.full(n, False)
	
	for _ in range(n):
		# Find the unvisited node with the smallest distance
		min_dist = np.inf
		min_node = -1
		for v in range(n):
			if not visited[v] and dist[v] < min_dist:
				min_dist = dist[v]
				min_node = v
		
		if min_node == -1:
			break
		
		visited[min_node] = True
		
		# Update distances for neighbors of min_node
		for neighbor in range(n):
			if dist_matrix[min_node, neighbor] != np.inf and not visited[neighbor]:
				new_dist = dist[min_node] + dist_matrix[min_node, neighbor]
				if new_dist < dist[neighbor]:
					dist[neighbor] = new_dist
	
	return dist


def dijkstra_with_path(graph: dict, u: int, n: int):
	dist = np.full(n, float('inf'))
	dist[u] = 0
	previous = np.full(n, -1)
	visited = np.full(n, False)
	
	priority_queue = [(0, u)]
	
	while priority_queue:
		current_distance, current_vertex = heapq.heappop(priority_queue)
		
		if visited[current_vertex]:
			continue
		
		visited[current_vertex] = True
		
		for neighbor, weight in graph[current_vertex].items():
			if not visited[neighbor]:
				new_dist = current_distance + weight
				if new_dist < dist[neighbor]:
					dist[neighbor] = new_dist
					previous[neighbor] = current_vertex
					heapq.heappush(priority_queue, (new_dist, neighbor))
	
	return dist, previous


def dijkstra_matrix_with_path(time_matrix: np.ndarray, u: int, n: int):
	dist = np.full(n, np.inf)
	dist[u] = 0
	previous = np.full(n, -1)
	visited = np.full(n, False)
	
	priority_queue = [(0, u)]
	
	while priority_queue:
		current_distance, current_vertex = heapq.heappop(priority_queue)
		
		if visited[current_vertex]:
			continue
		
		visited[current_vertex] = True
		
		for neighbor in range(n):
			if time_matrix[current_vertex, neighbor] != np.inf and not visited[neighbor]:
				new_dist = current_distance + time_matrix[current_vertex, neighbor]
				if new_dist < dist[neighbor]:
					dist[neighbor] = new_dist
					previous[neighbor] = current_vertex
					heapq.heappush(priority_queue, (new_dist, neighbor))
	
	return dist, previous
