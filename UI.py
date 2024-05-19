import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import Subway
import os
from matplotlib.lines import Line2D
import ctypes
try:
	ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
	ctypes.windll.user32.SetProcessDPIAware()


class SubwayApp:
	def __init__(self, root):
		current_dpi = root.winfo_fpixels('1i')
		scal = current_dpi / 96
		print(scal)
		self.font = ("Malgun Gothic", 15)

		self.root = root
		self.root.title("Subway Path Finder")
		self.root.geometry(f"{int(1080 * scal)}x{int(600 * scal)}")
		root.tk.call('tk', 'scaling', scal)

		# 한글 폰트를 설정합니다.
		plt.rcParams['font.family'] = 'Malgun Gothic'
		plt.rcParams['axes.unicode_minus'] = False

		# 경로 시각화를 위한 Figure 및 FigureCanvas 생성
		self.fig, self.ax = plt.subplots(figsize=(10, 8))
		self.ax.set_title("지하철 노선 경로", fontsize=20)
		self.ax.axis('off')
		self.canvas = FigureCanvasTkAgg(self.fig, master=root)
		self.canvas.draw()

		# 배경 이미지 설정
		self.background_image_reset()

		# 버튼과 텍스트 위젯을 포함할 프레임 생성
		frame = tk.Frame(root, bg="white")
		frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

		self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		def add_labeled_entry(parent, label_text, default_value, font=self.font):
			row = tk.Frame(parent, bg="white")
			label = tk.Label(row, text=label_text, bg="white", font=font)
			entry = tk.Entry(row, font=font)
			entry.insert(0, default_value)
			row.pack(fill=tk.X, pady=5)
			label.pack(side=tk.LEFT)
			entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
			return entry

		self.station_move_time = 1
		self.station_transfer_time = 2

		self.start_line_entry = add_labeled_entry(frame, "출발 노선 번호:", '1')
		self.start_station_entry = add_labeled_entry(frame, "출발역:", '소요산')
		self.end_line_entry = add_labeled_entry(frame, "도착 노선 번호:", '5')
		self.end_station_entry = add_labeled_entry(frame, "도착역:", '마천')
		self.station_move_time_entry = add_labeled_entry(frame, "역간 시간(분):", str(self.station_move_time))
		self.station_transfer_time_entry = add_labeled_entry(frame, "환승 시간(분):", str(self.station_transfer_time))

		# 검색 버튼
		self.search_button = tk.Button(frame, text="경로 검색", command=self.search_path, bg="#f0f0f0", font=self.font)
		self.search_button.pack(fill=tk.X, pady=5)

		# 초기화 버튼
		self.reset_button = tk.Button(frame, text="초기화", command=self.reset_app, bg="#f0f0f0", font=self.font)
		self.reset_button.pack(fill=tk.X, pady=5)

		# 스크롤 가능한 텍스트 위젯 생성
		self.result_text = scrolledtext.ScrolledText(frame, width=40, height=10, font=self.font)
		self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)

		subway_path_data_file_name = os.path.join(os.path.dirname(__file__), 'data/subway_path_data.txt')
		self.subway_data = Subway(subway_path_data_file_name, self.station_move_time, self.station_transfer_time)

	def search_path(self):
		if not self.start_line_entry.get().isdigit() or not self.end_line_entry.get().isdigit():
			messagebox.showerror("Error", "노선 번호는 숫자로 입력해주세요.")
			return

		if not self.station_move_time_entry.get().isdigit() or not self.station_transfer_time_entry.get().isdigit():
			messagebox.showerror("Error", "시간은 숫자로 입력해주세요.")
			return

		if not self.start_station_entry.get() or not self.end_station_entry.get():
			messagebox.showerror("Error", "역 이름을 입력해주세요.")
			return

		start_line = int(self.start_line_entry.get())
		start_station = self.start_station_entry.get()
		end_line = int(self.end_line_entry.get())
		end_station = self.end_station_entry.get()

		start_station_tuple = (start_line, start_station)
		end_station_tuple = (end_line, end_station)

		self.result_text.delete(1.0, tk.END)
		if self.station_move_time != int(self.station_move_time_entry.get()) or self.station_transfer_time != int(self.station_transfer_time_entry.get()):
			self.station_move_time = int(self.station_move_time_entry.get())
			self.station_transfer_time = int(self.station_transfer_time_entry.get())
			subway_path_data_file_name = os.path.join(os.path.dirname(__file__), 'data/subway_path_data.txt')
			self.subway_data = Subway(subway_path_data_file_name, self.station_move_time, self.station_transfer_time)

		result = self.subway_data.search_query(start_station_tuple, end_station_tuple)

		start_station_check = False
		end_station_check = False
		while result['weight'] == -2:
			if result['path'][0] == start_station_tuple:
				if start_station_check:
					messagebox.showerror("Error", f"출발역 {start_station}이 존재하지 않습니다.")
					return
				start_station_tuple = (start_line, start_station[:-1] if start_station[-1] == "역" else start_station + "역")
				start_station_check = True
			elif result['path'][0] == end_station_tuple:
				if end_station_check:
					messagebox.showerror("Error", f"도착역 {end_station}이 존재하지 않습니다.")
					return
				end_station_tuple = (end_line, end_station[:-1] if end_station[-1] == "역" else end_station + "역")
				end_station_check = True
			else:
				if start_station_check:
					messagebox.showerror("Error", f"출발역인 {start_station}이 존재하지 않습니다.")
					return
				if end_station_check:
					messagebox.showerror("Error", f"도착역인 {end_station}이 존재하지 않습니다.")
					return
				return
			result = self.subway_data.search_query(start_station_tuple, end_station_tuple)

		if result['weight'] == -1:
			self.result_text.insert(tk.END, "최단 경로를 찾을 수 없습니다.\n")
		else:
			# 역 추가
			path: list[tuple[int, str]] = [station if station[1][-1] == "역" else (station[0], station[1] + "역") for station in result['path']]

			path_str = ' -> '.join(station[1] for station in result['path'])
			result_str = f"최단 경로: {path_str}\n최단 거리: {result['weight']}분\n"

			# 요약된 결과 출력
			self.result_text.insert(tk.END, "요약 정보\n")
			self.result_text.insert(tk.END, f"\n최단 소요 시간: {result['weight']}분\n")
			self.result_text.insert(tk.END, f"출발: {path[0][1]}({path[0][0]}호선)\n")
			line_num = path[0][0]
			for station in path:
				if station[0] != line_num:
					self.result_text.insert(tk.END, f"환승: {station[1]}({line_num}호선 -> {station[0]}호선)\n")
					line_num = station[0]
			self.result_text.insert(tk.END, f"도착: {path[-1][1]}({path[-1][0]}호선)\n")

			# 상세 경로 출력
			self.result_text.insert(tk.END, "\n상세 경로(마우스 스크롤로 확인 가능)")
			line_num = -1
			for station in path:
				if station[0] != line_num:
					line_num = station[0]
					self.result_text.insert(tk.END, f"\n\n{line_num}호선: ", "line_num")
				else:
					self.result_text.insert(tk.END, " -> ")
				self.result_text.insert(tk.END, f"{station[1]}")
			self.result_text.tag_config('line_num', foreground='blue')

			self.visualize_path(path, path[0][1], path[-1][1])

	def visualize_path(self, path, start_station, end_station):
		line_color_dict = {
			1: "#0032a0", 2: "#00b140", 3: "#fc4c02", 4: "#00a9e0", 5: "#a05eb5",
		}

		G = nx.Graph()
		line_num = path[0][0]
		for i in range(len(path) - 1):
			if path[i][0] == path[i + 1][0]:
				G.add_edge(path[i][1], path[i + 1][1], weight=4, color=line_color_dict[path[i][0]])

		# pos = nx.spring_layout(G, seed=42)
		# pos = nx.spectral_layout(G)

		def custom_layout(G):
			pos = {}
			G_N = len(G.nodes)
			N = ((G_N + 9) // 20) * 2 + 1
			T = [int(G_N*i/N) for i in range(0, N + 1)]
			nodes = list(G.nodes())
			t = 0
			print(T)
			while t < N:
				size = T[t + 1] - T[t] - 1
				print(nodes[T[t]:T[t + 1]])
				if t % 2 == 0:
					for i, node in enumerate(nodes[T[t]:T[t + 1]]):
						pos[nodes[T[t]+i]] = (i/size, 1-t/N)
				else:
					for i, node in enumerate(nodes[T[t]:T[t + 1]]):
						pos[nodes[T[t]+i]] = (1-i/size, 1-t/N)
				t += 1
			print(pos)
			return pos
		pos = custom_layout(G)

		self.ax.clear()

		font_properties = {'family': 'Malgun Gothic', 'size': 12}

		edge_colors = [G[u][v]['color'] for u, v in G.edges]
		widths = [G[u][v]['weight'] for u, v in G.edges]
		node_colors = ['gray' for _ in G.nodes]
		node_edge_colors = ['gray' for _ in G.nodes]  # 노드의 아웃라인 색상을 회색으로 설정
		nx.draw(G, pos, with_labels=False, edge_color=edge_colors, width=widths, node_color='none', linewidths=2, edgecolors=node_edge_colors,
		node_size=300, font_family=font_properties['family'], font_size=font_properties['size'], font_weight="bold",
		verticalalignment='bottom')

		# 출발역과 도착역을 다른 색상으로 표시
		start_station_color = 'blue'
		end_station_color = 'red'
		nx.draw_networkx_nodes(G, pos, nodelist=[start_station], node_color=start_station_color, node_size=500)
		nx.draw_networkx_nodes(G, pos, nodelist=[end_station], node_color=end_station_color, node_size=500)

		# 환승역 표시
		transfer_stations = {}
		for line, station in path:
			if station not in transfer_stations:
				transfer_stations[station] = set()
			transfer_stations[station].add(line)

		for station, lines in transfer_stations.items():
			if len(lines) > 1:  # 환승역인 경우
				nx.draw_networkx_nodes(G, pos, nodelist=[station], node_color='green', node_size=500, ax=self.ax)

		# 노드 라벨을 수동으로 추가
		move_flag = False
		big_flag = False
		for i, (node, (x, y)) in enumerate(pos.items()):
			y_offset = 0.04
			if 5 < len(node):
				if not move_flag:
					y_offset += 0.04
					move_flag = True
				else:
					move_flag = False
				big_flag = True
			else:
				if big_flag and not move_flag:
					y_offset += 0.04
					move_flag = True
				else:
					move_flag = False
				big_flag = False
			self.ax.text(x, y-y_offset, node, fontsize=12,
			ha='center', va='center', rotation=0, fontweight='bold',
			fontfamily='Malgun Gothic', bbox=dict(facecolor='#e0e0e0', alpha=0.5, edgecolor='none'))

		# 범례 추가
		used_lines = set()  # 사용된 노선을 추적

		for i in range(len(path) - 1):
			if path[i][0] == path[i + 1][0]:
				G.add_edge(path[i][1], path[i + 1][1], weight=4, color=line_color_dict[path[i][0]])
				used_lines.add(path[i][0])  # 사용된 노선을 추가

		legend_elements = [Line2D([0], [0], color=line_color_dict[line], lw=4, label=f'{line} 호선')
		for line in used_lines]
		self.ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.1, 1.1), title='노선 별 색상', title_fontsize=12, fontsize=10)

		self.ax.set_title(f'"{start_station}"에서 "{end_station}"까지의 경로', fontsize=20)
		self.canvas.draw()

	def reset_app(self):
		# 엔트리 초기화
		self.start_line_entry.delete(0, tk.END)
		self.start_station_entry.delete(0, tk.END)
		self.end_line_entry.delete(0, tk.END)
		self.end_station_entry.delete(0, tk.END)

		# 결과 텍스트 초기화
		self.result_text.delete(1.0, tk.END)

		# 경로 시각화 초기화
		self.background_image_reset()

	def background_image_reset(self):
		self.ax.clear()
		self.ax.axis('off')
		image_path = os.path.join(os.path.dirname(__file__), 'subway.png')
		try:
			image = plt.imread(image_path)
			self.ax.imshow(image, extent=[-1, 1, -1, 1], aspect='auto', alpha=0.5)
		except FileNotFoundError:
			messagebox.showerror("Error", f"Image file not found: {image_path}")
		self.canvas.draw()


if __name__ == "__main__":
	root = tk.Tk()
	app = SubwayApp(root)
	root.mainloop()