from algorithm import *

if __name__ == '__main__':
	subway_data = Subway('data/subway_path_data.txt', 1, 0)
	print(subway_data.search_query((1, '서울역'), (1, '종각')))
	print(subway_data.search_query((1, '소요산'), (5, '마천')))
	print(subway_data.search_query((5, '마천'), (1, '소요산')))
	pass
	