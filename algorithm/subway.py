import numpy as np
from .parsing_subway_data import subway_parsing
from .floyd_warshall import floyd_warshall
from .johnson import johnson_simple, johnson_simple_matrix, johnson_simple_with_path
from .make_subway_matrix_data import *
import json
import os
import time


def make_subway_matrix_data_path(subway_data, station_move_time=1, station_transfer_time=2):
	# 행렬 이름 생성
	stations = []
	for line, station_list in subway_data.items():
		for station in station_list:
			stations.append((line, station))
	
	# 행렬 데이터 생성
	n = len(stations)
	subway_time_matrix = np.full((n, n), np.inf)
	subway_path_matrix = np.empty((n, n), dtype=object)
	
	# 주대각선 0으로 초기화
	for i in range(n):
		subway_time_matrix[i, i] = 0
		subway_path_matrix[i, i] = [i]
	
	# 같은 노선 상의 인접 역들 간의 이동 시간 설정
	for line, station_list in subway_data.items():
		for i in range(len(station_list) - 1):
			station1 = stations.index((line, station_list[i]))
			station2 = stations.index((line, station_list[i + 1]))
			subway_time_matrix[station1, station2] = station_move_time
			subway_time_matrix[station2, station1] = station_move_time
			subway_path_matrix[station1, station2] = [station1, station2]
			subway_path_matrix[station2, station1] = [station2, station1]
	
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
					subway_time_matrix[i, j] = station_transfer_time
					subway_path_matrix[i, j] = [i, j]
	
	# 알고리즘 실행
	johnson_simple_with_path(subway_time_matrix, subway_path_matrix)
	
	return stations, subway_time_matrix, subway_path_matrix


class Subway:
	def __init__(self, subway_path_data_file_name: str, station_move_time: int = 1, station_transfer_time: int = 2):
		self.subway_data = subway_parsing(subway_path_data_file_name)
		if self.subway_data is None:
			raise FileNotFoundError(f"{subway_path_data_file_name} not found")
		params = {'station_move_time': station_move_time, 'station_transfer_time': station_transfer_time}
		self.stations, self.subway_time_matrix, self.subway_path_matrix\
			= make_subway_matrix_data_path(self.subway_data, **params)
	
	def search_query(self, start_station: tuple[int, str], end_station: tuple[int, str])\
		-> dict[str, int | list[tuple[int, str]]]:
		start_station_index = self.stations.index(start_station)
		end_station_index = self.stations.index(end_station)
		wegiht = self.subway_time_matrix[start_station_index, end_station_index]
		low_path = self.subway_path_matrix[start_station_index, end_station_index]
		if np.isinf(wegiht):
			return {"weight": -1, "path": []}
		path = [self.stations[i] for i in low_path]
		return {
			"weight": int(wegiht),
			"path": path
		}
