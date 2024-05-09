import random
import networkx as nx
from shapely.geometry import Point
import math


def simulate_travel(graph, optimal_locations, num_people, min_distance, max_distance, bicycle_usage_rate):
    """
        bicycle_usage_rate: 자전거 보관함 만나면 타는 확률.

        리턴:
        자전거 탄 사람들과 안타는 사람의 평균 시간값을 튜플로 반환
    """
    cyclist_times = []
    non_cyclist_times = []

    # Set the travel speeds (in meters per second)
    cyclist_speed = 13 * 1000 / 3600  # 13 km/h
    walking_speed = 4 * 1000 / 3600   # 4 km/h

    for _ in range(num_people):
        # Select a random start node
        start_node = random.choice(list(graph.nodes))
        start_geom = graph.nodes[start_node]['geometry']

        # Select a random end node at least min_distance away
        end_node = None
        while end_node is None:
            candidate_node = random.choice(list(graph.nodes))
            candidate_geom = graph.nodes[candidate_node]['geometry']
            if start_geom.distance(candidate_geom) >= min_distance:
                end_node = candidate_node
            if start_geom.distance(candidate_geom) <= max_distance:
                end_node = candidate_node

        # Find the shortest path between start and end nodes
        shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight='length')
        #간단한 코드
        point = (shortest_path[0], shortest_path[-1])
        nearest_optimal_locations = find_nearest_optimal_node(graph,optimal_locations, point)

        used_bicycle = False
        # Check if any optimal bicycle locker location is on the shortest path
        for i in range(len(shortest_path) - 1):
            start_node_id = shortest_path[i]
            end_node_id = shortest_path[i + 1]
            if start_node_id in optimal_locations or end_node_id in optimal_locations:
              used_bicycle = True
              break
        # Calculate travel time
        travel_distance = sum(graph.edges[start_node_id, end_node_id]['geometry'].length for start_node_id, end_node_id in zip(shortest_path[:-1], shortest_path[1:]))
        if used_bicycle:
            travel_time = travel_distance / cyclist_speed
            cyclist_times.append(travel_time / 60)  # Convert to minutes
        else:
            travel_time = travel_distance / walking_speed
            non_cyclist_times.append(travel_time / 60)  # Convert to minutes

    avg_cyclist_time = sum(cyclist_times) / len(cyclist_times) if cyclist_times else 0
    avg_non_cyclist_time = sum(non_cyclist_times) / len(non_cyclist_times) if non_cyclist_times else 0

    return avg_cyclist_time, avg_non_cyclist_time

# ... (load the graph and find optimal locations as before)
# 평균 거리 출력하기
def find_nearest_optimal_node(G, optimal_locations, point):
  """
    주어진 지점에서 가장 가까운 optimal_locations의 노드를 찾습니다.

    Args:
        G (networkx.Graph): 네트워크 그래프
        optimal_locations (list): 최적 위치 노드 ID 리스트
        point (tuple): 지점의 좌표 (x, y)

    Returns:
        nearest_node: 가장 가까운 최적 위치 노드의 ID
  """
  point_geom = Point(point)
  max_distance = 500
  nearest_node = None

  for node_id in optimal_locations:
    node_geom = G.nodes[node_id]['geometry']
    distance = point_geom.distance(node_geom)
    if distance > max_distance:
      min_distance = distance
      nearest_node = node_id

  return nearest_node

avg_cyclist_time, avg_non_cyclist_time= simulate_travel(graph, optimal_locations, 10000, 1000, 10000, 0.1)
print(f"Average travel time for cyclists: {math.ceil(avg_cyclist_time)} minutes")
print(f"Average travel time for non-cyclists: {math.ceil(avg_non_cyclist_time)} minutes")
