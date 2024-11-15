"""
Helper stuff for generating various puzzle (piece shape) types.
"""
from util import * 

class PieceList:
    height, width = None, None
    plist = None
    def __init__(self, h, w):
        self.height, self.width = h, w
        self.plist = []
        for hi in range(self.height):
            for wi in range(self.width):
                self.plist.append((hi,wi))
    def length(self):
        return len(self.plist)
    def pop(self):
        return self.plist.pop()
    def add(self, p):
        self.plist.append(p)
    def add_around(self, h, w):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= h+dy < self.height and 0 <= w+dx < self.width:
                    self.plist.append((h+dy,w+dx))
                    

class CasualPuzzle:
    def __init__(self, POINT_COUNT):
        self.POINT_COUNT = POINT_COUNT
        self.OUTSIDE_CORNER_MAX_SLOPE = 0.2
        self.CORNER_VARIANCE = 0
        self.CORNER_ANGLE_VARIANCE = 0 * math.pi/4
        self.CORNER_INSIDE_MIN = (self.CORNER_VARIANCE**2/10.0*2)**0.5 # if the centre edge of the corner would be less than this length, then make the length 0. Current equation works out to about 10%
        self.OPENING_MID_VARIANCE = 0
        self.OPENING_MIN = 0.2
        self.OPENING_MAX = 0.2
        self.OPENING_ANGLE = 0 * math.pi/4
        self.OPENING_HEIGHT_VARIANCE = 0.05
        self.BEZIER_DISTANCE_MIN = .15
        self.BEZIER_DISTANCE_MULTIPLIER = 2.2
        self.NUB_POS_VARIANCE = 0
        self.NUB_HEIGHT_MIN = 0.3
        self.NUB_HEIGHT_MAX = 0.35
        self.NUB_TIP_ANGLE_AVERAGE = 0.2 * math.pi/4

        # average angles based on POINT_COUNT: 3=100  4=134  5=139  6=145  7=149  8=153  9=155  10=159  11=160  12=161  13=164  14=164 15=166 16=166 17=167 18=167 19=168
        self.NUB_TIP_ANGLE_ADJUSTMENT = 0.5 * math.pi/2 * self.POINT_COUNT**-0.9 # this is approximately the angle that we can adjust the tip by so that it blends in with the resolution of the curve
        
        self.SHIFT_VARIANCE = 0.3


    def genNub(self):
        """ Geometry of the nub
                tip
               ,-o-,
              /     \
              |     |
      open 1   \   /      open 2
        o------' o '-------o
                mid
        """
        while 1: #test for well-behaved curves
            # The left-right position of the nub
            ropen_mid = random.uniform(-self.OPENING_MID_VARIANCE, self.OPENING_MID_VARIANCE)

            #The nub tip has a point and an angle that we want to use
            rtip = Vector(ropen_mid + random.uniform(-self.NUB_POS_VARIANCE, self.NUB_POS_VARIANCE),
                    random.uniform(self.NUB_HEIGHT_MIN, self.NUB_HEIGHT_MAX))
            rtip_angle = random.uniform(-self.NUB_TIP_ANGLE_AVERAGE, self.NUB_TIP_ANGLE_AVERAGE)
            rtip_angle_left = rtip_angle + random.uniform(0,self.NUB_TIP_ANGLE_ADJUSTMENT)
            rtip_angle_right = rtip_angle - random.uniform(0,self.NUB_TIP_ANGLE_ADJUSTMENT)

            # The left anchor point of the nub is specified
            ropen1 = Vector(ropen_mid - random.uniform(self.OPENING_MIN, self.OPENING_MAX),
                      random.uniform(-self.OPENING_HEIGHT_VARIANCE, self.OPENING_HEIGHT_VARIANCE))
            ropen1_angle = random.uniform(-self.OPENING_ANGLE, self.OPENING_ANGLE)
            # The bézier curve needs additional control points. If the x-distance between the anchor point
            # and the control point is > the x-distance between the anchor point and the tip point,
            # we get a curve that loops back on itself a bit to give us pretty loopy nubs.
            ropen1_bottom_dist = random.uniform(1.1, self.BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen1.x), self.BEZIER_DISTANCE_MIN) / math.cos(ropen1_angle)
            # Again, make the x-distance between the tip point and the second control point > between the anchor point and the tip
            ropen1_top_dist = random.uniform(1.1, self.BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen1.x), self.BEZIER_DISTANCE_MIN) / math.cos(rtip_angle_left)

            #the right anchor point of the nub is specified
            ropen2 = Vector(ropen_mid + random.uniform(self.OPENING_MIN, self.OPENING_MAX),
                      random.uniform(-self.OPENING_HEIGHT_VARIANCE, self.OPENING_HEIGHT_VARIANCE))
            ropen2_angle = random.uniform(-self.OPENING_ANGLE, self.OPENING_ANGLE)
            ropen2_bottom_dist = random.uniform(1, self.BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen2.x), self.BEZIER_DISTANCE_MIN) / math.cos(ropen2_angle)
            ropen2_top_dist = random.uniform(1, self.BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen2.x), self.BEZIER_DISTANCE_MIN) / math.cos(rtip_angle_right)

            # Specify whether the nub is an innie(-1) or an outie(+1)
            rndir = random.randint(0,1) * 2 - 1
                  
            # Create control points for bézier curves
            open1_c_bot = ropen1 + v_extend(ropen1_angle, ropen1_bottom_dist)
            open1_c_top = rtip - v_extend(rtip_angle_left, ropen1_top_dist) # subtract because angle is opposite to what it should be for this direction
            open2_c_bot = ropen2 + v_extend(math.pi - ropen2_angle, ropen2_bottom_dist)
            open2_c_top = rtip + v_extend(rtip_angle_right, ropen2_top_dist)

            # if the top control points are long enough to extend below the opening anchors, this causes loops
            # the same happens when the bottom control points are long enough to extend above the tip
            if rejig_bad_pieces and (open1_c_top.y < ropen1.y or open2_c_top.y < ropen2.y or open1_c_bot.y > rtip.y or open2_c_bot.y > rtip.y):
                continue

            # Create point getters for the two halves of the nub
            bez1 = v_cubic_bezier(ropen1, rtip, open1_c_bot, open1_c_top)
            bez2 = v_cubic_bezier(rtip, ropen2, open2_c_top, open2_c_bot)

            MAX_POINTINESS = 2.5 #the number of times more pointy the tip curve can be than the anchor curve
            SMALL_TURN_RADIUS = 0.3
            MIN_TURN_RADIUS = 0.2
            # We don't want the nub to have too pointy of a curve so do some math to check for this and reject the nub
            # do first bezier
            roots = bez1.dx_roots()
            turn_radius = [bez1.turn_radius(t) for t in roots] #this gives some relative measure of the turn radius
            if len(roots) < 2: #if our curve doesn't turn back on itself to make a pretty nub
                raise Exception("Our bezier curve is not as curvy as we thought it was!")
            elif turn_radius[1] < turn_radius[0]: #if the turn radius of the tip is pointier than the turn radius at the anchor...
                # do a search for the minimum turn radius between roots[1] and 1
                min_turn_radius = turn_radius[1]
                steps = min(20, int((1-roots[1])/0.01))
                for i in range(1,steps+1):
                    new_turn_radius = bez1.turn_radius(lerp(roots[1], 1, 1.0*i/steps))
                    if new_turn_radius < min_turn_radius:
                        min_turn_radius = new_turn_radius
                    else:
                        break

                #if the turn radius of the tip is more than 3x pointier, or the tip turn radius then reject this nub
                if rejig_bad_pieces and (min_turn_radius < MIN_TURN_RADIUS or turn_radius[0] < MIN_TURN_RADIUS or min_turn_radius < SMALL_TURN_RADIUS and min_turn_radius < 1.0*turn_radius[0]/MAX_POINTINESS): 
                    continue

            # do the same calculation for the other bezier but this time the tip is the first root
            roots = bez2.dx_roots()
            roots.reverse()
            turn_radius = [bez2.turn_radius(t) for t in roots] #this gives some relative measure of the turn radius
            if len(roots) < 2: #if our curve doesn't turn back on itself to make a pretty nub
                raise Exception("Our bezier curve is not as curvy as we thought it was!")
            elif turn_radius[1] < turn_radius[0]: #if the turn radius of the tip is pointier than the turn radius at the anchor...
                # do a search for the minimum turn radius between roots[1] and 1
                min_turn_radius = turn_radius[1]
                steps = min(20, int((1-roots[1])/0.01))
                for i in range(1,steps+1):
                    new_turn_radius = bez2.turn_radius(lerp(roots[1], 1, 1.0*i/steps))
                    if new_turn_radius < min_turn_radius:
                        min_turn_radius = new_turn_radius
                    else:
                        break
                if rejig_bad_pieces and (min_turn_radius < MIN_TURN_RADIUS or turn_radius[0] < MIN_TURN_RADIUS or min_turn_radius < SMALL_TURN_RADIUS and min_turn_radius < 1.0*turn_radius[0]/MAX_POINTINESS):
                    continue

            # Generate the final nub shape
            bez1_points = [bez1.point_t(1.0*t/self.POINT_COUNT) for t in range(self.POINT_COUNT)]
            bez2_points = [bez2.point_t(1.0*t/self.POINT_COUNT) for t in range(self.POINT_COUNT + 1)]
            rp = py2d.Polygon.from_tuples(bez1_points + bez2_points)

            rp.add_point(Vector(1,-1))
            rp.add_point(Vector(-1,-1))

            if rejig_bad_pieces and rp.is_self_intersecting():
                continue
            rp = [Vector(x, rndir*y) for x,y in rp.as_tuple_list()[:-2]]
            break
            

        #rp2 = py2d.Polygon.from_tuples([ropen1,rtip,ropen2])
        #rp3 = py2d.Polygon.from_tuples([open1_c_top, open2_c_top])
        #rp4 = py2d.Polygon.from_tuples([ropen1, open1_c_bot])
        #rp5 = py2d.Polygon.from_tuples([ropen2, open2_c_bot])
        
        return rp

    def genVertNub(self, i_row, i_column):
        t1 = py2d.Transform.move(i_column + 0.5, i_row + 1)
        return [t1 * p for p in self.genNub()]

    def genHorizNub(self, i_row, i_column):
        t1 = py2d.Transform.move(i_column + 1, i_row + 0.5)
        t2 = py2d.Transform.rotate(math.pi/2)
        t3 = py2d.Transform.mirror_y()
        return [t1 * t2 * t3 * p for p in self.genNub()]
    
    def isEdgeShort(self, rc1, rc2):
        return True # always do this for casual puzzle

    def genShiftedCorner(self, hi, wi, horiz_nubs, vert_nubs):
        # Get the nub points which will bound how large our center variations can be
        N_point = horiz_nubs[hi+1][wi][0]
        S_point = horiz_nubs[hi][wi][-1]
        W_point = vert_nubs[hi][wi][-1]
        E_point = vert_nubs[hi][wi+1][0]
        
        # Time to make the centre edge
        rdir = random.randint(0,1) #0 is horizontal, 1 is vertical
        
        #this limits how close an EW point can get to an EW nub
        closeness = 0.8
        
        # this measure limits the distance from the origin to a NS point based on the distance from the origin to the EW nubs. Similarly for EW points and NS nubs.
        # we only need on point to be close so pick the negative one arbitrarily
        closeness2 = 0.8
        
        if rdir == 0:
            max_dist = min(abs(S_point[1] - hi - 1), abs(N_point[1] - hi - 1))*closeness2
            rc1 = random.uniform(max(-self.CORNER_VARIANCE, (W_point[0] - wi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(self.CORNER_VARIANCE, (E_point[0] - wi - 1)*closeness))
        else:
            max_dist = min(abs(W_point[0] - wi - 1), abs(E_point[0] - wi - 1))*closeness2
            rc1 = random.uniform(max(-self.CORNER_VARIANCE, (S_point[1] - hi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(self.CORNER_VARIANCE, (N_point[1] - hi - 1)*closeness))
        # ropening == "down" means the corners connect to N & W edges and S & E edges. Likewise "up" means corners connect to SW and NE.
        ropening = ['down','up'][random.randint(0,1)]

        t1 = py2d.Transform.move(wi + 1, hi + 1)
        if self.isEdgeShort(rc1, rc2):
            # if center edge is short, just make all NSEW edges join up to it directly
            # C_edge has a length of 0
            C_edge = [t1 * Vector(rc1, rc2)]
        else:
            """
            Diagram of a shifted corner
            (this example has the openings going "down" because the edges open into the top-right and the bottom-left)
            
                | North edge                Here is the other possible arrangemet but with the openings going "up":
                |       c2                        |
         _______o________o____ East edge     __o__o__
         West  c1 Center |                     |
                         | South edge           
                         |
            """

            rrotation = random.uniform(-self.CORNER_ANGLE_VARIANCE, self.CORNER_ANGLE_VARIANCE)

            # always use c1 as the right or bottom corner
            rc1, rc2 = min(rc1, rc2), max(rc1, rc2)
            #do calculations for a horizontal center edge, then rotate it
            t2 = py2d.Transform.rotate(rdir * math.pi/2)
            C_edge = [t1 * t2 * Vector(p, math.tan(rrotation)*p) for p in [rc1,rc2]]

        if ropening == "down" and rdir == 1:
            # We want the direction of C_edge to always go the direction of the left corner piece to the right corner piece
            # This will make calculations easier later on when figuring out which direction C_edge needs to be appended
            C_edge = list(reversed(C_edge))

        # Time to make the directional edges
        # for each direction, the first point is connected to its appropriate center
        # and the second point is connected to a nub from the piece in that direction
        N_edge = [C_edge[-1 if ropening == 'up' else 0], N_point]
        S_edge = [C_edge[-1 if ropening == 'down' else 0], S_point]
        W_edge = [C_edge[0], W_point]
        E_edge = [C_edge[-1], E_point]

        #swap the center point it is attached to if one is significantly closer to the nub point than the other
        swapped = {'N':0, 'S':0, 'W':0, 'E':0}
        for d in swapped.keys():
            ed = eval(d+'_edge') # eg. N_edge
            other_C = C_edge[0] if ed[0] == C_edge[-1] else C_edge[-1]
            other_len = (other_C - ed[-1]).get_length()
            curr_len = (ed[0] - ed[-1]).get_length()
            if other_len < curr_len * 0.9:
                swapped[d] = 1
                ed[0] = other_C
        
        

        return {"swapped":swapped, "ropening":ropening, "C_edge":C_edge, "N_edge":N_edge, "S_edge":S_edge, "W_edge":W_edge, "E_edge":E_edge}

    def genVertOutside(self, hi, wi):
        rx, ry = wi, hi
        if hi != 0 and hi != self.height:
            nub_point = self.vert_nubs[hi-1][0 if wi == 0 else -1][0 if wi == 0 else -1]
            nub_dist = abs(nub_point.x - wi)
            ry = nub_point.y + self.OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    def genHorizOutside(self, hi, wi):
        rx, ry = wi, hi
        if wi != 0 and wi != self.width:
            nub_point = self.horiz_nubs[0 if hi == 0 else -1][wi-1][0 if hi == 0 else -1]
            nub_dist = abs(nub_point.y - hi)
            rx = nub_point.x + self.OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)


    def generate(self, width, height):
        self.width = width
        self.height = height

        self.vert_nubs = []
        for hi in range(height - 1):
            o = []
            for wi in range(width):
                o.append(self.genVertNub(hi, wi))
            self.vert_nubs += [o]
        
        self.horiz_nubs = []
        for hi in range(height):
            o = []
            for wi in range(width - 1):
                o.append(self.genHorizNub(hi, wi))
            self.horiz_nubs += [o]

        outside_corners = {'vert':[[],[]], 'horiz':[[],[]]}
        for i in range(2):
            for hi in range(height + 1):
                outside_corners['vert'][i].append(self.genVertOutside(hi, i*width))
        for i in range(2):
            for wi in range(width + 1):
                outside_corners['horiz'][i].append(self.genHorizOutside(i*height, wi))

        inside_corners = []
        for hi in range(height - 1):
            o = []
            for wi in range(width - 1):
                o.append(self.genShiftedCorner(hi, wi, self.horiz_nubs, self.vert_nubs))
            inside_corners.append(o)

        
        piece_list = PieceList(height, width)
        piece_dict = {}
        while piece_list.length() > 0:
            has_self_intersecting = 0
            hi, wi = piece_list.pop()
            # Make the piece clockwise from the bottom left corner
            p = py2d.Polygon()

            # Bottom left corner
            if hi == 0:
                p.add_point(outside_corners['horiz'][0][wi])
            elif wi == 0:
                p.add_point(outside_corners['vert'][0][hi])
            else:
                corn = inside_corners[hi-1][wi-1]
                pts = list(reversed(corn['E_edge']))[1:-1]
                # If the centre point that this edge was joined to was swapped, then do the opposite of including the center edge. Do opposite C_edge direction in some cases too. Crazy complicated
                swp = corn['swapped']['N'] or corn['swapped']['E']
                pts += (corn['C_edge'] if corn['swapped']['E'] else list(reversed(corn['C_edge'])))[:-1] if (corn['ropening'] == 'down') != swp else []
                pts += corn['N_edge'][:-1]
                p.add_points([Vector(x,y) for x,y in pts])

            # Left nub
            if wi != 0:
                p.add_points(self.horiz_nubs[hi][wi - 1])
                
            # Top left corner
            if hi == height - 1:
                p.add_point(outside_corners['horiz'][1][wi])
            elif wi == 0:
                p.add_point(outside_corners['vert'][0][hi + 1])
            else:
                corn = inside_corners[hi][wi-1]
                pts = list(reversed(corn['S_edge']))[1:-1]
                swp = corn['swapped']['S'] or corn['swapped']['E']
                pts += (list(reversed(corn['C_edge'])) if corn['swapped']['E'] else corn['C_edge'])[:-1] if (corn['ropening'] == 'up') != swp else []
                pts += corn['E_edge'][:-1]
                p.add_points([Vector(x,y) for x,y in pts])

            # Top nub
            if hi != height - 1:
                p.add_points(self.vert_nubs[hi][wi])

            # Top right corner
            if hi == height - 1:
                p.add_point(outside_corners['horiz'][1][wi + 1])
            elif wi == width - 1:
                p.add_point(outside_corners['vert'][1][hi + 1])
            else:
                corn = inside_corners[hi][wi]
                pts = list(reversed(corn['W_edge']))[1:-1]
                swp = corn['swapped']['S'] or corn['swapped']['W']
                pts += (list(reversed(corn['C_edge'])) if corn['swapped']['W'] else corn['C_edge'])[:-1] if (corn['ropening'] == 'down') != swp else []
                pts += corn['S_edge'][:-1]
                p.add_points([Vector(x,y) for x,y in pts])

            # Right nub
            if wi != width - 1:
                p.add_points(list(reversed(self.horiz_nubs[hi][wi])))
                
            # Bottom right corner
            if hi == 0:
                p.add_point(outside_corners['horiz'][0][wi + 1])
            elif wi == width - 1:
                p.add_point(outside_corners['vert'][1][hi])
            else:
                corn = inside_corners[hi-1][wi]
                pts = list(reversed(corn['N_edge']))[1:-1]
                swp = corn['swapped']['N'] or corn['swapped']['W']
                pts += (corn['C_edge'] if corn['swapped']['W'] else list(reversed(corn['C_edge'])))[:-1] if (corn['ropening'] == 'up') != swp else []
                pts += corn['W_edge'][:-1]
                p.add_points([Vector(x,y) for x,y in pts])

            # Bottom nub
            if hi != 0:
                p.add_points(list(reversed(self.vert_nubs[hi - 1][wi])))

            # check if piece is self-intersecting
            if rejig_bad_pieces and (p.is_self_intersecting() or p.get_closest_distance_to_self() < 0.07):
                #print(f"regen {width}x{height} {wi} {hi}")
                has_self_intersecting = 1
                # regenerate nubs and continue looking for more conflicts
                if wi != 0:
                    self.horiz_nubs[hi][wi - 1] = self.genHorizNub(hi, wi-1)
                if hi != height - 1:
                    self.vert_nubs[hi][wi] = self.genVertNub(hi, wi)
                if wi != width - 1:
                    self.horiz_nubs[hi][wi] = self.genHorizNub(hi, wi)
                if hi != 0:
                    self.vert_nubs[hi - 1][wi] = self.genVertNub(hi-1, wi)
                #Then since the corners rely on the placement of the nubs, regenerate those
                #First outside corners
                if hi == 0:
                    outside_corners['horiz'][0][wi] = self.genHorizOutside(0, wi)
                    outside_corners['horiz'][0][wi+1] = self.genHorizOutside(0, wi+1)
                if hi == height - 1:
                    outside_corners['horiz'][1][wi] = self.genHorizOutside(height, wi)
                    outside_corners['horiz'][1][wi+1] = self.genHorizOutside(height, wi+1)
                if wi == 0:
                    outside_corners['vert'][0][hi] = self.genVertOutside(hi, 0)
                    outside_corners['vert'][0][hi+1] = self.genVertOutside(hi+1, 0)
                if wi == width - 1:
                    outside_corners['vert'][1][hi] = self.genVertOutside(hi, width)
                    outside_corners['vert'][1][hi+1] = self.genVertOutside(hi+1, width)
                
                #Then inside corners
                if hi != 0 and wi != 0:
                    inside_corners[hi-1][wi-1] = self.genShiftedCorner(hi-1, wi-1, self.horiz_nubs, self.vert_nubs)
                if hi != height - 1 and wi != 0:
                    inside_corners[hi][wi-1] = self.genShiftedCorner(hi, wi-1, self.horiz_nubs, self.vert_nubs)
                if hi != height - 1 and wi != width - 1:
                    inside_corners[hi][wi] = self.genShiftedCorner(hi, wi, self.horiz_nubs, self.vert_nubs)
                if hi != 0 and wi != width - 1:
                    inside_corners[hi-1][wi] = self.genShiftedCorner(hi-1, wi, self.horiz_nubs, self.vert_nubs)

                    
            if has_self_intersecting:
                piece_list.add_around(hi, wi)
                continue
            piece_dict[(hi,wi)] = py2d.Polygon.from_tuples([Vector(round(q[0],3), round(q[1],3)) for q in p])
        pieces = []
        for hi in range(height):
            for wi in range(width):
                pieces.append(piece_dict[(hi, wi)])
        return pieces


class FunkyPuzzle(CasualPuzzle):
    def __init__(self, POINT_COUNT):
        super().__init__(POINT_COUNT)

        self.OUTSIDE_CORNER_MAX_SLOPE = 0.4
        self.CORNER_VARIANCE = 0.2
        self.CORNER_ANGLE_VARIANCE = 0.5 * math.pi/4
        self.CORNER_INSIDE_MIN = (self.CORNER_VARIANCE**2/10.0*2)**0.5 # if the centre edge of the corner would be less than this length, then make the length 0. Current equation works out to about 10%
        self.OPENING_MID_VARIANCE = 0.2
        self.OPENING_MIN = 0.15/2
        self.OPENING_MAX = 0.25
        self.OPENING_ANGLE = 0.3 * math.pi/4
        self.OPENING_HEIGHT_VARIANCE = 0.05
        self.BEZIER_DISTANCE_MIN = 0.1
        self.BEZIER_DISTANCE_MULTIPLIER = 1.8
        self.NUB_POS_VARIANCE = 0.15
        self.NUB_HEIGHT_MIN = 0.15
        self.NUB_HEIGHT_MAX = 0.35
        self.NUB_TIP_ANGLE_AVERAGE = 0.5 * math.pi/4

        # average angles based on POINT_COUNT: 3=100  4=134  5=139  6=145  7=149  8=153  9=155  10=159  11=160  12=161  13=164  14=164 15=166 16=166 17=167 18=167 19=168
        self.NUB_TIP_ANGLE_ADJUSTMENT = 0.5 * math.pi/2 * POINT_COUNT**-0.9 # this is approximately the angle that we can adjust the tip by so that it blends in with the resolution of the curve
        
        self.SHIFT_VARIANCE = 0.1

    def isEdgeShort(self, rc1, rc2):
        return abs(rc2 - rc1) < self.CORNER_INSIDE_MIN



class TraditionalPuzzle(CasualPuzzle):
    def __init__(self):
        super().__init__(5) # POINT_COUNT doesn't really matter since we override getNub()

        self.OUTSIDE_CORNER_MAX_SLOPE = 0.2
        self.CORNER_VARIANCE = 0
        self.CORNER_ANGLE_VARIANCE = 0 * math.pi/4

        self.NUB_HEIGHT_VARIANCE = 0.05
        self.NUB_SIDEWAYS_VARIANCE = 0.08

    def genNub(self):
        nub = trNubs.getNub()

        # Randomly place the nub on the edge of the piece
        # Generate a random x,y coordinate within a diamond instead of a square! That way the placement of the nub will never be in an extreme corner
        rx = random.random()
        ry = random.random() - 0.5
        if ry > rx/2:
            ry -= 0.5
            rx += 1
        elif ry < -rx/2:
            ry += 0.5
            rx += 1
        ry *= 2
        rx -= 1
        
        t = py2d.Transform.move(rx*self.NUB_SIDEWAYS_VARIANCE,ry*self.NUB_HEIGHT_VARIANCE)
        nub = [t * p for p in nub]
        isInnie = random.random() > 0.5 # Decide whether nub is an innie or an outie
        if isInnie:
            return py2d.Polygon.from_tuples([(x, -y) for x,y in nub])
        else:
            return py2d.Polygon.from_tuples(nub)



def generateCasualPuzzle(width, height, POINT_COUNT):
    gen = CasualPuzzle(POINT_COUNT)
    return gen.generate(width, height)



def generateFunkyPuzzle(width, height, POINT_COUNT):
    gen = FunkyPuzzle(POINT_COUNT)
    return gen.generate(width, height)


def generateTraditionalPuzzle(width, height):
    gen = TraditionalPuzzle()
    return gen.generate(width, height)




def generateJaggedPuzzle(width, height):
    CORNER_VARIANCE = 0.1
    OPENING_POS_VARIANCE = 0.1
    OPENING_SIZE_MIN = 0.15/2
    OPENING_SIZE_VARIANCE = 0.1/2
    NUB_POS_VARIANCE = 0.1
    NUB_SIZE_MIN = 0.02/2
    NUB_SIZE_VARIANCE = 0.15/2
    NUB_HEIGHT_MIN = 0.1
    NUB_HEIGHT_VARIANCE = 0.15
    NUB_SKEW_VARIANCE = 0.02

    def genHorizOpening():
        rpos = round(random.uniform(-OPENING_POS_VARIANCE,OPENING_POS_VARIANCE),3)
        rsize = round(random.uniform(OPENING_SIZE_MIN, OPENING_SIZE_MIN + OPENING_SIZE_VARIANCE),3)
        rnpos = round(rpos + random.uniform(-NUB_POS_VARIANCE,NUB_POS_VARIANCE),3)
        rnsize = round(rsize + random.uniform(NUB_SIZE_MIN, NUB_SIZE_MIN + NUB_SIZE_VARIANCE),3)
        rnheight = round(random.uniform(NUB_HEIGHT_MIN, NUB_HEIGHT_MIN + NUB_HEIGHT_VARIANCE),3)
        rnskew = round(random.uniform(-NUB_SKEW_VARIANCE, NUB_SKEW_VARIANCE),3)
        rndir = random.randint(0,1)*2 - 1
        rp = py2d.Polygon()
        rp.add_point(py2d.Vector(0, rpos-rsize))
        rp.add_point(py2d.Vector(rndir*(rnheight + rnskew), rnpos - rnsize))
        rp.add_point(py2d.Vector(rndir*(rnheight - rnskew), rnpos + rnsize))
        rp.add_point(py2d.Vector(0, rpos+rsize))
        return rp

    def genVertOpening():
        t1 = py2d.Transform.rotate(math.pi/2)
        t2 = py2d.Transform.mirror_y()
        return py2d.Polygon.from_tuples([t1 * t2 * p for p in genHorizOpening()])
        
    corners = []
    for hi in range(height + 1):
        c = []
        for wi in range(width + 1):
            rx = 0 if wi == 0 or wi == width else random.uniform(-CORNER_VARIANCE,CORNER_VARIANCE)
            ry = 0 if hi == 0 or hi == height else random.uniform(-CORNER_VARIANCE,CORNER_VARIANCE)
            c += [py2d.Vector(rx,ry)]
        corners += [c]
    
    horiz_openings = []
    for hi in range(height):
        o = []
        for wi in range(width - 1):
            o += [genHorizOpening()]
        horiz_openings += [o]
    
    vert_openings = []
    for hi in range(height - 1):
        o = []
        for wi in range(width):
            o += [genVertOpening()]
        vert_openings += [o]

    while 1:
        has_self_intersecting = 0
        pieces = []
        for hi in range(height):
            for wi in range(width):
                p = py2d.Polygon()
                p.add_point(corners[hi][wi])
                if wi != 0:
                    rp = horiz_openings[hi][wi - 1]
                    p.add_points([py2d.Transform.move(0, 0.5) * v for v in rp])
                p.add_point(py2d.Transform.move(0, 1) * corners[hi + 1][wi])
                if hi != height - 1:
                    rp = vert_openings[hi][wi]
                    p.add_points([py2d.Transform.move(0.5, 1) * v for v in rp])
                p.add_point(py2d.Transform.move(1, 1) * corners[hi + 1][wi + 1])
                if wi != width - 1:
                    rp = horiz_openings[hi][wi]
                    p.add_points([py2d.Transform.move(1, 0.5) * v for v in rp.clone().flip()])
                p.add_point(py2d.Transform.move(1, 0) * corners[hi][wi + 1])
                if hi != 0:
                    rp = vert_openings[hi - 1][wi]
                    p.add_points([py2d.Transform.move(0.5, 0) * v for v in rp.clone().flip()])

                # check if piece is self-intersecting
                if p.is_self_intersecting():
                    print(f"regen {width}x{height} {wi} {hi}")
                    has_self_intersecting = 1
                    # regenerate nubs and continue looking for more conflicts
                    if wi != 0:
                        horiz_openings[hi][wi - 1] = genHorizOpening()
                    if hi != height - 1:
                        vert_openings[hi][wi] = genVertOpening()
                    if wi != width - 1:
                        horiz_openings[hi][wi] = genHorizOpening()
                    if hi != 0:
                        vert_openings[hi - 1][wi] = genVertOpening()
                pieces += [py2d.Polygon.from_tuples([py2d.Transform.move(wi, hi) * q for q in p])]
        if not has_self_intersecting:
            break
    return pieces



