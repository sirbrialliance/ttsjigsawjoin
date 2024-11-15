import math
import random

import py2d
from gzip import GzipFile

# NB: we are importing the local, modified copy of py2d
# You can debug "install" it wtih `pip install -e src/` from the project root.
from py2d import Bezier
from py2d.Math import Vector

rejig_bad_pieces = 1


def v_extend(angle, dist):
    # returns the point at a given distance and angle from (0,0)
    return Vector(math.cos(angle) * dist, math.sin(angle) * dist)

def lerp(p1, p2, t):
    return (1-t)*p1 + t*p2

class v_cubic_bezier:
    p1, p2, c1, c2 = None, None, None, None
    def __init__(self,_p1, _p2, _c1, _c2):
        #print(_p1, _p2, _c1, _c2)
        self.p1, self.p2, self.c1, self.c2 = _p1, _p2, _c1, _c2
        
    def point_t(self, t):
        p1, p2, c1, c2 = self.p1, self.p2, self.c1, self.c2
        return p1 * (-t**3 + 3*t**2 - 3*t + 1) + c1 * ( 3*t**3 - 6*t**2 + 3*t) + c2 * (-3*t**3 + 3*t**2) + p2 * (t**3)

    def point_t_rounded(self, t):
        p = self.point_t(t)
        return Vector(round(p.x,3),round(p.y,3))

    def point_dt(self, t):
        # returns the point of the derivative
        p1, p2, c1, c2 = self.p1, self.p2, self.c1, self.c2
        return p1 * (-3*t**2 + 6*t - 3) + c1 * ( 9*t**2 - 12*t + 3) + c2 * (-9*t**2 + 6*t) + p2 * (3*t**2)

    def point_d2t(self, t):
        p1, p2, c1, c2 = self.p1, self.p2, self.c1, self.c2
        return p1 * (-6*t + 6) + c1 * ( 18*t - 12) + c2 * (-18*t + 6) + p2 * (6*t)

    def dx_roots(self):
        # finds the locations r1 and r2 for t where the curve's tangent is vertical
        # always returns the roots in order r1 < r2
        # point_t(r) is a possible local extrema
        # point_dt(r) is small if the curve is tight
        
        
        p1, p2, c1, c2 = self.p1, self.p2, self.c1, self.c2
        a = p1.x * -3.0 + c1.x * 9 + c2.x * -9 + p2.x * 3
        b = p1.x * 6.0 + c1.x * -12 + c2.x * 6
        c = p1.x * -3.0 + c1.x * 3
        
        if a == 0:
            # find the root of the straight line
            if b == 0:
                # roots are either everywhere or nowhere, ignore this case and return no roots
                return []
            return [-c/b]

        # find the roots of the quadratic
        s = b**2 - 4*a*c

        if s < 0:
            # roots are imaginary, return no roots
            return []
        r1 = (-b - s**.5)/2/a
        r2 = (-b + s**.5)/2/a
        if r1 > r2:
            r1, r2 = r2, r1
        return [x for x in [r1, r2] if x >= 0 and x <= 1]

    def turn_radius(self, t):
        p = self.point_dt(t)
        return (p.x**2 + p.y**2)**0.5

class KnobSelector:
    # Class that returns nubs that point up
    # Nubs are centered horizontally around 0
    # Nubs are set horizontally between [-0.5, 0.5]
    # Nubs look good when attached to a horizontal line at 0 height
    def __init__(self, zippath):
        self.knobs = []
        with GzipFile(zippath, 'r') as zip:
            for line in zip:
                self.knobs.append(py2d.Polygon.from_tuples([[(float(x)-0.5, float(y)) for x, y in [p.split(b',')]][0] for p in line.split(b' ')]))

    def getNub(self):
        knob = random.choice(self.knobs)
        # get 2 different nubs for each 1 nub using horizontal reflection
        if random.randrange(2) == 1:
            tmp = [(-p[0], p[1]) for p in knob]
            tmp.reverse()
            return py2d.Polygon.from_tuples(tmp)
        return knob

trNubs = KnobSelector('knobs.gz')
