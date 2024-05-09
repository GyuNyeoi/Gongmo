import matplotlib.font_manager as fm

path = '/usr/local/lib/python3.10/dist-packages/matplotlib/mpl-data/fonts/ttf/MaruBuri-Regular.ttf'
fontprop = fm.FontProperties(fname=path)

optimal_locations_coords = [graph.nodes[node_id]['geometry'].coords[0] for node_id in optimal_locations]
optimal_locations_names = [graph.nodes[node_id]['name'] for node_id in optimal_locations]

fig, ax = plt.subplots(figsize=(10, 10))
links_df = gpd.read_file(link_shp, encoding='cp949')
links_df.plot(ax=ax, color='gray')

for coord, name in zip(optimal_locations_coords, optimal_locations_names):
    x, y = round(coord[0], 3), round(coord[1], 3)
    ax.scatter(x, y, c='red', zorder=3)
    ax.annotate(name, (x, y), xytext=(5, -5),
                textcoords='offset points', fontsize=8, fontproperties=fontprop)

ax.set_xlabel('경도', fontproperties=fontprop)
ax.set_ylabel('위도', fontproperties=fontprop)
ax.set_title('최적의 자전거 위치 선정', fontproperties=fontprop)
ax.legend()

plt.show()
