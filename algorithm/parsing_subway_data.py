import os


def subway_parsing(file_name):
	subway_line = {}
	if not os.path.exists(file_name):
		return None
	with open(file_name, 'r') as file:
		subway_line_num = 0
		while True:
			text = file.readline()
			if not text:
				break
			if text.strip() == '':
				continue
			station = [t.strip() for t in text.split('-')]
			subway_line_num += 1
			subway_line[subway_line_num] = station
	
	return subway_line