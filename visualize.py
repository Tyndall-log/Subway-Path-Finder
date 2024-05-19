import networkx as nx
import matplotlib.pyplot as plt
from algorithm import Subway

# Subway 객체 생성
subway_data = Subway('data/subway_path_data.txt')

while True:
    start_line = int(input("출발 노선 번호를 입력하세요: "))
    start_station = input("출발역을 입력하세요: ")
    end_line = int(input("도착 노선 번호를 입력하세요: "))
    end_station = input("도착역을 입력하세요: ")
    
    start_station_tuple = (start_line, start_station)
    end_station_tuple = (end_line, end_station)
    
    # Subway 클래스의 search_query 메서드를 사용하여 최단 경로를 탐색
    result = subway_data.search_query(start_station_tuple, end_station_tuple)
    
    if result['weight'] == -1:
        print("최단 경로를 찾을 수 없습니다.")
    else:
        print(f"최단 경로: {result['path']}")
        print(f"최단 거리: {result['weight']}분")
        
        # 시각화
        G = nx.Graph()
        for i in range(len(result['path']) - 1):
            G.add_edge(result['path'][i], result['path'][i + 1])

        pos = nx.spring_layout(G, seed=42)  # 노드의 위치 결정 시 seed 값을 설정하여 고정
        plt.figure(figsize=(10, 8))  # 그래프 크기 조정
        nx.draw(G, pos, with_labels=True, node_size=450, font_family='Malgun Gothic', font_size=7, font_weight="bold")

        # 출발역과 도착역을 다른 색상으로 표시
        start_station_color = 'blue'
        end_station_color = 'red'

        # 출발역과 도착역을 별도로 추가하여 위치 지정
        if start_station not in G:
            G.add_node(start_station)
            pos[start_station] = (pos[result['path'][0]][0], pos[result['path'][0]][1] + 0.1)
        if end_station not in G:
            G.add_node(end_station)
            pos[end_station] = (pos[result['path'][-1]][0], pos[result['path'][-1]][1] - 0.1)

        nx.draw_networkx_nodes(G, pos, nodelist=[start_station], node_color=start_station_color, node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=[end_station], node_color=end_station_color, node_size=500)

       
        plt.title('최단 경로')
          

        plt.show()
    
    cont = input("계속해서 경로를 찾으시겠습니까? (Y/N): ")
    if cont.upper() != 'Y':
        break