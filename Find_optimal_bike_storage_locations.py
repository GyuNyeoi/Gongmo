import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import networkx as nx
import osmnx as ox
import openpyxl

import numpy as np
from shapely.geometry import Point

def load_networkx_from_shapefiles(node_shp, link_shp):

  # Load the node and link dataframes
  nodes_df = gpd.read_file(node_shp, encoding='cp949')
  links_df = gpd.read_file(link_shp, encoding='cp949')

  # Create the graph
  graph = nx.Graph()

  # Add nodes to the graph
  for _, row in nodes_df.iterrows():
    node_id = row['NODE_ID']
    node_geom = row['geometry']
    node_name = row['NODE_NAME']
    #node_adm = row['ADM_NM']
    #adm=node_adm
    graph.add_node(node_id, geometry=node_geom, name=node_name)

  # Add edges to the graph
  for _, row in links_df.iterrows():
    start_node_id = row['F_NODE']
    end_node_id = row['T_NODE']
    edge_geom = row['geometry']
    road_name = row['ROAD_NAME']
    graph.add_edge(start_node_id, end_node_id, geometry=edge_geom, road_name=road_name)

  return graph


def find_optimal_bike_storage_locations_c(graph, num_locations, min_distance):

    closeness_centrality = nx.closeness_centrality(graph)

    sorted_nodes = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)

    optimal_locations = []
    selected_nodes = []

    for node_id, _ in sorted_nodes:
        if node_id not in selected_nodes:
            node = graph.nodes[node_id]
            node_geom = node['geometry']

            # Check if the node is far enough from the already selected nodes
            if all(node_geom.distance(graph.nodes[selected_node_id]['geometry']) >= min_distance for selected_node_id in selected_nodes):
                optimal_locations.append(node_id)
                selected_nodes.append(node_id)

                if len(optimal_locations) == num_locations:
                    break

    return optimal_locations, closeness_centrality

def find_optimal_bike_storage_locations_b(graph, num_locations, min_distance):

    betweenness_centrality = nx.betweenness_centrality(graph, weight='length')

    sorted_nodes = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)

    optimal_locations = []
    selected_nodes = []
    for node_id, _ in sorted_nodes:
        if node_id not in selected_nodes:
            node = graph.nodes[node_id]
            node_geom = node['geometry']
            # Check if the node is far enough from the already selected nodes
            if all(node_geom.distance(graph.nodes[selected_node_id]['geometry']) >= min_distance for selected_node_id in selected_nodes):
                optimal_locations.append(node_id)
                selected_nodes.append(node_id)
                if len(optimal_locations) == num_locations:
                    break

    return optimal_locations, betweenness_centrality

import networkx.algorithms.centrality as cent

def find_optimal_bike_storage_locations_h(graph, num_locations, min_distance):

    harmony_centrality = cent.harmonic_centrality(graph)

    sorted_nodes = sorted(harmony_centrality.items(), key=lambda x: x[1], reverse=True)

    optimal_locations = []
    selected_nodes = []
    for node_id, _ in sorted_nodes:
        if node_id not in selected_nodes:
            node = graph.nodes[node_id]
            node_geom = node['geometry']
            # Check if the node is far enough from the already selected nodes
            if all(node_geom.distance(graph.nodes[selected_node_id]['geometry']) >= min_distance for selected_node_id in selected_nodes):
                optimal_locations.append(node_id)
                selected_nodes.append(node_id)
                if len(optimal_locations) == num_locations:
                    break

    return optimal_locations, harmony_centrality

node_shp = '/content/drive/MyDrive/shp2/EditNode.shp'
link_shp = '/content/drive/MyDrive/shp2/EditLink.shp'
graph = load_networkx_from_shapefiles(node_shp, link_shp)

#optimal_locations, betweenness_centrality = find_optimal_bike_storage_locations_b(graph, 20, 600)
optimal_locations, closeness_centrality = find_optimal_bike_storage_locations_c(graph, 20, 400)
#optimal_locations, harmony_centrality = find_optimal_bike_storage_locations_h(graph, 20, 500)

print("최적의 자전거 보관함 위치:")
for node_id in optimal_locations:
    node = graph.nodes[node_id]
    print(f"- Node: {node_id}, closeness_centrality: {closeness_centrality[node_id]}, Node Name: {node['name']}") # closeness_centrality or betweenness_centrality or harmony_centrality
