import voronoi
PointsMap = {'a1':[1,2],'a2':[4,3],'a3':[5,8]}
Sitepts = []
pts = {}

# print CurrentDate, PointsMap[PointsMap.keys()[0]]
for grid, stn in PointsMap.items():
    x = float(stn[0])
    y = float(stn[1])
    station = grid
    # station.extend( stn[3:])
    # print x,y,station

    pts[(x, y)] = station

stncounts = len(pts.keys())
# print stncounts, "points"

site_points = []
for pt in pts.keys():
    Sitepts.append(voronoi.Site(pt[0], pt[1]))
    print(type(voronoi.Site(pt[0], pt[1])))
    site_points.append((pt[0], pt[1]))

# print "Calculating Voronoi Lattice",

siteList = voronoi.SiteList(Sitepts)
context = voronoi.Context()
voronoi.Edge.EDGE_NUM = 0
voronoi.voronoi(siteList, context)

vertices = context.vertices
lines = context.lines
edges = context.edges
triangles = context.triangles
has_edge = context.has_edge

print(vertices, lines, edges, has_edge)