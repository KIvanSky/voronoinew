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

class Context(object):
    def __init__(self):
        self.doPrint = 0
        self.debug   = 0
        self.plot    = 0
        self.triangulate = False
        self.vertices  = []    # list of vertex 2-tuples: (x,y)
        self.lines     = []    # equation of line 3-tuple (a b c), for the equation of the line a*x+b*y = c
        self.edges     = []    # edge 3-tuple: (line index, vertex 1 index, vertex 2 index)   if either vertex index is -1, the edge extends to infiinity
        self.triangles = []    # 3-tuple of vertex indices
        self.has_edge = {}    # edge belongs to 2 vertices

    def circle(self,x,y,rad):
        pass

    def clip_line(self,edge):
        pass

    def line(self,x0,y0,x1,y1):
        pass

    def outSite(self,s):
        if(self.debug):
            print "site (%d) at %f %f" % (s.sitenum, s.x, s.y)
        elif(self.triangulate):
            pass
        elif(self.plot):
            self.circle (s.x, s.y, cradius)
        elif(self.doPrint):
            print "s %f %f" % (s.x, s.y)

    def outVertex(self,s):
        self.vertices.append((s.x,s.y))
        if(self.debug):
            print  "vertex(%d) at %f %f" % (s.sitenum, s.x, s.y)
        elif(self.triangulate):
            pass
        elif(self.doPrint and not self.plot):
            print "v %f %f" % (s.x,s.y)

    def outTriple(self,s1,s2,s3):
        self.triangles.append((s1.sitenum, s2.sitenum, s3.sitenum))
        if(self.debug):
            print "circle through left=%d right=%d bottom=%d" % (s1.sitenum, s2.sitenum, s3.sitenum)
        elif(self.triangulate and self.doPrint and not self.plot):
            print "%d %d %d" % (s1.sitenum, s2.sitenum, s3.sitenum)

    def outBisector(self,edge):
        self.lines.append((edge.a, edge.b, edge.c))
        if(self.debug):
            print "line(%d) %gx+%gy=%g, bisecting %d %d" % (edge.edgenum, edge.a, edge.b, edge.c, edge.reg[0].sitenum, edge.reg[1].sitenum)
        elif(self.triangulate):
            if(self.plot):
                self.line(edge.reg[0].x, edge.reg[0].y, edge.reg[1].x, edge.reg[1].y)
        elif(self.doPrint and not self.plot):
            print "l %f %f %f" % (edge.a, edge.b, edge.c)

    def outEdge(self,edge):
        sitenumL = -1
        if edge.ep[Edge.LE] is not None:
            sitenumL = edge.ep[Edge.LE].sitenum
        sitenumR = -1
        if edge.ep[Edge.RE] is not None:
            sitenumR = edge.ep[Edge.RE].sitenum
        self.edges.append((edge.edgenum,sitenumL,sitenumR))
        if(not self.triangulate):
            if self.plot:
                self.clip_line(edge)
            elif(self.doPrint):
                print "e %d" % edge.edgenum,
                print " %d " % sitenumL,
                print "%d" % sitenumR


def voronoi(siteList, context):
    edgeList = EdgeList(siteList.xmin, siteList.xmax, len(siteList))
    priorityQ = PriorityQueue(siteList.ymin, siteList.ymax, len(siteList))
    siteIter = siteList.iterator()

    bottomsite = siteIter.next()
    context.outSite(bottomsite)
    newsite = siteIter.next()
    minpt = Site(-BIG_FLOAT, -BIG_FLOAT)
    while True:
        if not priorityQ.isEmpty():
            minpt = priorityQ.getMinPt()

        if (newsite and (priorityQ.isEmpty() or cmp(newsite, minpt) < 0)):
            # newsite is smallest -  this is a site event
            context.outSite(newsite)

            # get first Halfedge to the LEFT and RIGHT of the new site
            lbnd = edgeList.leftbnd(newsite)
            rbnd = lbnd.right

            # if this halfedge has no edge, bot = bottom site (whatever that is)
            # create a new edge that bisects
            bot = lbnd.rightreg(bottomsite)
            edge = Edge.bisect(bot, newsite)
            context.outBisector(edge)
            try:
                context.has_edge[bot.sitenum].append(edge.edgenum)
            except:
                context.has_edge[bot.sitenum] = [edge.edgenum]

            try:
                context.has_edge[newsite.sitenum].append(edge.edgenum)
            except:
                context.has_edge[newsite.sitenum] = [edge.edgenum]

            # create a new Halfedge, setting its pm field to 0 and insert
            # this new bisector edge between the left and right vectors in
            # a linked list
            bisector = Halfedge(edge, Edge.LE)
            edgeList.insert(lbnd, bisector)

            # if the new bisector intersects with the left edge, remove
            # the left edge's vertex, and put in the new one
            p = lbnd.intersect(bisector)
            if p is not None:
                priorityQ.delete(lbnd)
                priorityQ.insert(lbnd, p, newsite.distance(p))

            # create a new Halfedge, setting its pm field to 1
            # insert the new Halfedge to the right of the original bisector
            lbnd = bisector
            bisector = Halfedge(edge, Edge.RE)
            edgeList.insert(lbnd, bisector)

            # if this new bisector intersects with the right Halfedge
            p = bisector.intersect(rbnd)
            if p is not None:
                # push the Halfedge into the ordered linked list of vertices
                priorityQ.insert(bisector, p, newsite.distance(p))

            newsite = siteIter.next()

        elif not priorityQ.isEmpty():
            # intersection is smallest - this is a vector (circle) event

            # pop the Halfedge with the lowest vector off the ordered list of
            # vectors.  Get the Halfedge to the left and right of the above HE
            # and also the Halfedge to the right of the right HE
            lbnd = priorityQ.popMinHalfedge()
            llbnd = lbnd.left
            rbnd = lbnd.right
            rrbnd = rbnd.right

            # get the Site to the left of the left HE and to the right of
            # the right HE which it bisects
            bot = lbnd.leftreg(bottomsite)
            top = rbnd.rightreg(bottomsite)

            # output the triple of sites, stating that a circle goes through them
            mid = lbnd.rightreg(bottomsite)
            context.outTriple(bot, top, mid)

            # get the vertex that caused this event and set the vertex number
            # couldn't do this earlier since we didn't know when it would be processed
            v = lbnd.vertex
            siteList.setSiteNumber(v)
            context.outVertex(v)

            # set the endpoint of the left and right Halfedge to be this vector
            if lbnd.edge.setEndpoint(lbnd.pm, v):
                context.outEdge(lbnd.edge)

            if rbnd.edge.setEndpoint(rbnd.pm, v):
                context.outEdge(rbnd.edge)

            # delete the lowest HE, remove all vertex events to do with the
            # right HE and delete the right HE
            edgeList.delete(lbnd)
            priorityQ.delete(rbnd)
            edgeList.delete(rbnd)

            # if the site to the left of the event is higher than the Site
            # to the right of it, then swap them and set 'pm' to RIGHT
            pm = Edge.LE
            if bot.y > top.y:
                bot, top = top, bot
                pm = Edge.RE

            # Create an Edge (or line) that is between the two Sites.  This
            # creates the formula of the line, and assigns a line number to it
            edge = Edge.bisect(bot, top)
            context.outBisector(edge)
            try:
                context.has_edge[bot.sitenum].append(edge.edgenum)
            except:
                context.has_edge[bot.sitenum] = [edge.edgenum]

            try:
                context.has_edge[top.sitenum].append(edge.edgenum)
            except:
                context.has_edge[top.sitenum] = [edge.edgenum]

            # create a HE from the edge
            bisector = Halfedge(edge, pm)

            # insert the new bisector to the right of the left HE
            # set one endpoint to the new edge to be the vector point 'v'
            # If the site to the left of this bisector is higher than the right
            # Site, then this endpoint is put in position 0; otherwise in pos 1
            edgeList.insert(llbnd, bisector)
            if edge.setEndpoint(Edge.RE - pm, v):
                context.outEdge(edge)

            # if left HE and the new bisector don't intersect, then delete
            # the left HE, and reinsert it
            p = llbnd.intersect(bisector)
            if p is not None:
                priorityQ.delete(llbnd);
                priorityQ.insert(llbnd, p, bot.distance(p))

            # if right HE and the new bisector don't intersect, then reinsert it
            p = bisector.intersect(rrbnd)
            if p is not None:
                priorityQ.insert(bisector, p, bot.distance(p))
        else:
            break

    he = edgeList.leftend.right
    while he is not edgeList.rightend:
        context.outEdge(he.edge)
        he = he.right


print(vertices)
print(lines)
print(edges)
print(has_edge)