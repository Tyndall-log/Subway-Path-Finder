import numpy as np
from .parsing_subway_data import subway_parsing
from .floyd_warshall import floyd_warshall
from .johnson import johnson_simple, johnson_simple_matrix
import json
import os
import time


def load_subway_matrix_data(file_name):
	with open(file_name, 'r') as file:
		return json.load(file)


def make_subway_matrix_data_benchmark(subway_data, station_move_time=1, station_transfer_time=2):
	# 행렬 이름 생성
	stations = []
	for line, station_list in subway_data.items():
		for station in station_list:
			stations.append((line, station))
	
	# 행렬 데이터 생성
	n = len(stations)
	subway_matrix = np.full((n, n), np.inf)
	
	# 주대각선 0으로 초기화
	for i in range(n):
		subway_matrix[i, i] = 0
	
	# 같은 노선 상의 인접 역들 간의 이동 시간 설정
	for line, station_list in subway_data.items():
		for i in range(len(station_list) - 1):
			station1 = stations.index((line, station_list[i]))
			station2 = stations.index((line, station_list[i + 1]))
			subway_matrix[station1, station2] = station_move_time
			subway_matrix[station2, station1] = station_move_time
	
	# 환승역 간의 환승 시간 설정
	transfer_stations = {}  # 환승역 목록
	for i, (line, station) in enumerate(stations):
		if station not in transfer_stations:
			transfer_stations[station] = []
		transfer_stations[station].append(i)
	for indices in transfer_stations.values():
		for i in indices:
			for j in indices:
				if i != j:
					subway_matrix[i, j] = station_transfer_time
		
	# 알고리즘 실행 시간 측정
	matrix1 = subway_matrix.copy()
	matrix2 = subway_matrix.copy()
	matrix3 = subway_matrix.copy()
	
	t1 = time.time()
	matrix = floyd_warshall(matrix1)
	t2 = time.time()
	matrix2 = johnson_simple(matrix2)
	t3 = time.time()
	matrix3 = johnson_simple_matrix(matrix3)
	t4 = time.time()
	print(f'플로이드-워샬 알고리즘: {t2 - t1:.6f}초')
	print(f'존슨 알고리즘: {t3 - t2:.6f}초')
	print(f'존슨 알고리즘(행렬): {t4 - t3:.6f}초')
	if not np.array_equal(matrix, matrix2):
		print('플로이드-워샬 알고리즘과 존슨 알고리즘의 결과가 다릅니다.')
	if not np.array_equal(matrix, matrix3):
		print('플로이드-워샬 알고리즘과 존슨 알고리즘(행렬)의 결과가 다릅니다.')
	
	return {'stations': stations, 'matrix': matrix}


def make_subway_matrix_data(subway_data, station_move_time=1, station_transfer_time=2):
	subway_matrix_data_file_name = f'data/subway_matrix_data({station_move_time},{station_transfer_time}).txt'
	
	# 행렬 이름 생성
	stations = []
	for line, station_list in subway_data.items():
		for station in station_list:
			stations.append((line, station))
	
	# 이미 생성된 파일이 있는 경우, 해당 파일을 불러옴
	if os.path.exists(subway_matrix_data_file_name):
		subway_matrix_data = load_subway_matrix_data(subway_matrix_data_file_name)
		if subway_matrix_data is not None:
			smds = [tuple(s) for s in subway_matrix_data['stations']]
			if smds == stations:
				return {'stations': stations, 'matrix': np.array(subway_matrix_data['matrix'])}
	
	# 행렬 데이터 생성
	n = len(stations)
	subway_matrix = np.full((n, n), np.inf)
	
	# 주대각선 0으로 초기화
	for i in range(n):
		subway_matrix[i, i] = 0
	
	# 같은 노선 상의 인접 역들 간의 이동 시간 설정
	for line, station_list in subway_data.items():
		for i in range(len(station_list) - 1):
			station1 = stations.index((line, station_list[i]))
			station2 = stations.index((line, station_list[i + 1]))
			subway_matrix[station1, station2] = station_move_time
			subway_matrix[station2, station1] = station_move_time
	
	# 환승역 간의 환승 시간 설정
	transfer_stations = {}  # 환승역 목록
	for i, (line, station) in enumerate(stations):
		if station not in transfer_stations:
			transfer_stations[station] = []
		transfer_stations[station].append(i)
	for indices in transfer_stations.values():
		for i in indices:
			for j in indices:
				if i != j:
					subway_matrix[i, j] = station_transfer_time
	
	matrix = johnson_simple(subway_matrix)
	
	# 결과 저장
	with open(subway_matrix_data_file_name, 'w') as file:
		json.dump({'stations': stations, 'matrix': matrix.tolist()}, file)
	
	return {'stations': stations, 'matrix': matrix}


if __name__ == '__main__':
	subway_data = subway_parsing('../data/subway_path_data.txt')
	if subway_data is None:
		print('지하철 데이터를 불러오는 데 실패했습니다.')
		exit()
	
	params = {'station_move_time': 1, 'station_transfer_time': 2}
	
	subway_matrix_data = make_subway_matrix_data(subway_data, **params)
	# subway_matrix_data = make_subway_matrix_data_benchmark(subway_data, **params)
	
	# 결과 출력
	print(subway_matrix_data)
