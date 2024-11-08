#!/usr/bin/env python3.7
import gzip
import math
import os
from pathlib import Path
import random
import sys

# import poly_decomp as pd
import py2d
import pygame
import numpy as np
import io
from gzip import GzipFile

# NB: we are importing the local, modified copy of py2d
# You can debug "install" it wtih `pip install -e src/` from the project root.
from py2d import Bezier
from py2d.Math import Vector

random.seed(1)

rejig_bad_pieces = 1

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

isPyGameStarted = 0
gameDisplay = None

def startPyGame():
    global gameDisplay, isPyGameStarted
    isPyGameStarted = 1
    pygame.init()
    gameDisplay = pygame.display.set_mode((1550,850))
    gameDisplay.fill(black)

def drawLine(p1,p2, clr = white):
    sq = 800
    thick = 1
    #clr = white; thick = 15;
    if isPyGameStarted:
        pygame.draw.line(gameDisplay, clr, (25+p1[0]*sq,sq+50-(25+p1[1]*sq)), (25 + p2[0]*sq,sq+50 - (25 + p2[1]*sq)),thick)
    


#path_of_obj_pieces = Path(r"E:\Virtual Drives\Tabletop Simulator\Tabletop Simulator\Mods\Models\New folder")
#obj_pieces_files = [x for x in path_of_obj_pieces.iterdir()]


#test_vertices = [[0.461744,-0.277219],[0.457329,-0.162697],[0.484049,-0.088212],[0.553679,-0.084445],[0.644116,-0.110628],[0.724793,-0.108135],[0.770059,-0.038035],[0.773943,0.059833],[0.735395,0.125938],[0.658684,0.121358],[0.569373,0.089594],[0.498344,0.094756],[0.468193,0.181023],[0.468358,0.312813],[0.491069,0.532882],[0.270479,0.556003],[0.138191,0.558057],[0.051171,0.532851],[0.045067,0.470831],[0.076238,0.393653],[0.081221,0.330763],[0.017102,0.305873],[-0.076856,0.319744],[-0.14084,0.367403],[-0.13536,0.440454],[-0.102209,0.516864],[-0.103503,0.571179],[-0.18223,0.585521],[-0.51084,0.532882],[-0.484498,0.171714],[-0.507592,0.081002],[-0.566116,0.071608],[-0.64013,0.100473],[-0.702354,0.104723],[-0.730489,0.041689],[-0.722158,-0.050438],[-0.679965,-0.113255],[-0.610377,-0.108154],[-0.535315,-0.075739],[-0.480563,-0.076402],[-0.464433,-0.15199],[-0.51084,-0.468816],[-0.308215,-0.432687],[-0.188621,-0.425008],[-0.114273,-0.451421],[-0.1183,-0.525167],[-0.155031,-0.62148],[-0.159096,-0.706083],[-0.086874,-0.750347],[0.018261,-0.748215],[0.09119,-0.699273],[0.088724,-0.609263],[0.055415,-0.508463],[0.057747,-0.433294],[0.141831,-0.409872],[0.272275,-0.423057],[0.491069,-0.468816]]
#spear shape
#objtxt = """v -0.148628 0.037500 -0.424926\nv -0.072528 0.037500 -0.438042\nv -0.078018 0.037500 -0.494872\nv -0.118991 0.037500 -0.576992\nv -0.129184 0.037500 -0.657901\nv -0.063891 0.037500 -0.713714\nv 0.035355 0.037500 -0.731005\nv 0.105463 0.037500 -0.698964\nv 0.104539 0.037500 -0.615634\nv 0.075474 0.037500 -0.514482\nv 0.082356 0.037500 -0.437825\nv 0.169400 0.037500 -0.416294\nv 0.301326 0.037500 -0.433759\nv 0.521116 0.037500 -0.487363\nv 0.555944 0.037500 -0.276884\nv 0.563669 0.037500 -0.152078\nv 0.539149 0.037500 -0.073168\nv 0.470238 0.037500 -0.074801\nv 0.382690 0.037500 -0.112971\nv 0.311729 0.037500 -0.124005\nv 0.285432 0.037500 -0.064529\nv 0.303301 0.037500 0.027657\nv 0.357693 0.037500 0.094454\nv 0.437709 0.037500 0.097258\nv 0.519430 0.037500 0.075427\nv 0.575681 0.037500 0.087813\nv 0.587566 0.037500 0.174790\nv 0.521116 0.037500 0.514335\nv 0.160303 0.037500 0.586648\nv 0.072998 0.037500 0.574817\nv 0.069925 0.037500 0.516193\nv 0.104701 0.037500 0.432711\nv 0.110179 0.037500 0.355493\nv 0.041228 0.037500 0.310727\nv -0.059232 0.037500 0.304856\nv -0.126270 0.037500 0.339388\nv -0.116920 0.037500 0.410346\nv -0.076076 0.037500 0.491807\nv -0.070601 0.037500 0.552364\nv -0.147057 0.037500 0.569469\nv -0.270796 0.037500 0.556015\nv -0.480793 0.037500 0.514335\nv -0.435956 0.037500 0.170917\nv -0.452732 0.037500 0.083544\nv -0.508240 0.037500 0.072285\nv -0.585274 0.037500 0.096363\nv -0.659408 0.037500 0.096279\nv -0.709221 0.037500 0.032007\nv -0.725333 0.037500 -0.058578\nv -0.701369 0.037500 -0.118128\nv -0.637096 0.037500 -0.109212\nv -0.556840 0.037500 -0.074062\nv -0.491068 0.037500 -0.074830\nv -0.462318 0.037500 -0.154404\nv -0.461418 0.037500 -0.278630\nv -0.480793 0.037500 -0.487363"""
#clover
#objtxt = """v 0.461744 0.0375 -0.277219\nv 0.457329 0.0375 -0.162697\nv 0.484049 0.0375 -0.088212\nv 0.553679 0.0375 -0.084445\nv 0.644116 0.0375 -0.110628\nv 0.724793 0.0375 -0.108135\nv 0.770059 0.0375 -0.038035\nv 0.773943 0.0375 0.059833\nv 0.735395 0.0375 0.125938\nv 0.658684 0.0375 0.121358\nv 0.569373 0.0375 0.089594\nv 0.498344 0.0375 0.094756\nv 0.468193 0.0375 0.181023\nv 0.468358 0.0375 0.312813\nv 0.491069 0.0375 0.532882\nv 0.270479 0.0375 0.556003\nv 0.138191 0.0375 0.558057\nv 0.051171 0.0375 0.532851\nv 0.045067 0.0375 0.470831\nv 0.076238 0.0375 0.393653\nv 0.081221 0.0375 0.330763\nv 0.017102 0.0375 0.305873\nv -0.076856 0.0375 0.319744\nv -0.14084 0.0375 0.367403\nv -0.13536 0.0375 0.440454\nv -0.102209 0.0375 0.516864\nv -0.103503 0.0375 0.571179\nv -0.18223 0.0375 0.585521\nv -0.51084 0.0375 0.532882\nv -0.484498 0.0375 0.171714\nv -0.507592 0.0375 0.081002\nv -0.566116 0.0375 0.071608\nv -0.64013 0.0375 0.100473\nv -0.702354 0.0375 0.104723\nv -0.730489 0.0375 0.041689\nv -0.722158 0.0375 -0.050438\nv -0.679965 0.0375 -0.113255\nv -0.610377 0.0375 -0.108154\nv -0.535315 0.0375 -0.075739\nv -0.480563 0.0375 -0.076402\nv -0.464433 0.0375 -0.15199\nv -0.51084 0.0375 -0.468816\nv -0.308215 0.0375 -0.432687\nv -0.188621 0.0375 -0.425008\nv -0.114273 0.0375 -0.451421\nv -0.1183 0.0375 -0.525167\nv -0.155031 0.0375 -0.62148\nv -0.159096 0.0375 -0.706083\nv -0.086874 0.0375 -0.750347\nv 0.018261 0.0375 -0.748215\nv 0.09119 0.0375 -0.699273\nv 0.088724 0.0375 -0.609263\nv 0.055415 0.0375 -0.508463\nv 0.057747 0.0375 -0.433294\nv 0.141831 0.0375 -0.409872\nv 0.272275 0.0375 -0.423057\nv 0.491069 0.0375 -0.468816\n"""
#man shape
#objtxt = """v 0.175484 0.037500 0.456547\nv 0.097879 0.037500 0.476452\nv 0.097034 0.037500 0.527816\nv 0.129684 0.037500 0.596258\nv 0.133469 0.037500 0.661601\nv 0.066748 0.037500 0.705410\nv -0.029264 0.037500 0.716237\nv -0.092636 0.037500 0.684378\nv -0.082933 0.037500 0.607911\nv -0.045717 0.037500 0.516041\nv -0.048040 0.037500 0.445750\nv -0.136076 0.037500 0.423855\nv -0.272467 0.037500 0.436484\nv -0.501135 0.037500 0.479934\nv -0.523069 0.037500 0.110370\nv -0.502037 0.037500 0.017918\nv -0.449112 0.037500 0.009203\nv -0.378532 0.037500 0.040776\nv -0.310349 0.037500 0.048998\nv -0.263050 0.037500 -0.009431\nv -0.248861 0.037500 -0.096437\nv -0.278435 0.037500 -0.153603\nv -0.354443 0.037500 -0.142669\nv -0.447645 0.037500 -0.105995\nv -0.520805 0.037500 -0.106098\nv -0.546724 0.037500 -0.186074\nv -0.538359 0.037500 -0.311327\nv -0.501135 0.037500 -0.521975\nv -0.136791 0.037500 -0.585270\nv -0.050192 0.037500 -0.569598\nv -0.050411 0.037500 -0.507919\nv -0.090826 0.037500 -0.423569\nv -0.103752 0.037500 -0.349210\nv -0.043049 0.037500 -0.311310\nv 0.051241 0.037500 -0.311559\nv 0.117527 0.037500 -0.345453\nv 0.114798 0.037500 -0.405541\nv 0.084358 0.037500 -0.472562\nv 0.088087 0.037500 -0.524308\nv 0.168781 0.037500 -0.544715\nv 0.500563 0.037500 -0.521975\nv 0.527290 0.037500 -0.322981\nv 0.530176 0.037500 -0.204014\nv 0.502516 0.037500 -0.126590\nv 0.433622 0.037500 -0.122627\nv 0.348223 0.037500 -0.150108\nv 0.279913 0.037500 -0.148535\nv 0.255398 0.037500 -0.077891\nv 0.273802 0.037500 0.019925\nv 0.327366 0.037500 0.082533\nv 0.405361 0.037500 0.069446\nv 0.485195 0.037500 0.027746\nv 0.541300 0.037500 0.026409\nv 0.555819 0.037500 0.113029\nv 0.500563 0.037500 0.479934"""
#innies
#objtxt = """v -0.264999 0.037500 -0.527983\nv -0.132645 0.037500 -0.533144\nv -0.047627 0.037500 -0.508778\nv -0.046169 0.037500 -0.444016\nv -0.082371 0.037500 -0.362431\nv -0.089787 0.037500 -0.296156\nv -0.023399 0.037500 -0.270626\nv 0.076126 0.037500 -0.284496\nv 0.146702 0.037500 -0.329721\nv 0.146824 0.037500 -0.396118\nv 0.117302 0.037500 -0.464901\nv 0.119530 0.037500 -0.515150\nv 0.196201 0.037500 -0.532087\nv 0.514690 0.037500 -0.498785\nv 0.535744 0.037500 -0.138386\nv 0.510014 0.037500 -0.050657\nv 0.448322 0.037500 -0.046673\nv 0.368698 0.037500 -0.081051\nv 0.296070 0.037500 -0.087910\nv 0.252155 0.037500 -0.022484\nv 0.245876 0.037500 0.075544\nv 0.282948 0.037500 0.145370\nv 0.362309 0.037500 0.146284\nv 0.455856 0.037500 0.117947\nv 0.528713 0.037500 0.120117\nv 0.555504 0.037500 0.194376\nv 0.548863 0.037500 0.309612\nv 0.514690 0.037500 0.502912\nv 0.319908 0.037500 0.526966\nv 0.203796 0.037500 0.528925\nv 0.128994 0.037500 0.502163\nv 0.126896 0.037500 0.436178\nv 0.155872 0.037500 0.351324\nv 0.156025 0.037500 0.275684\nv 0.087540 0.037500 0.233082\nv -0.009087 0.037500 0.230303\nv -0.073288 0.037500 0.269875\nv -0.065590 0.037500 0.348545\nv -0.030880 0.037500 0.439611\nv -0.035145 0.037500 0.510565\nv -0.123768 0.037500 0.537767\nv -0.259785 0.037500 0.533093\nv -0.487217 0.037500 0.502913\nv -0.531223 0.037500 0.311646\nv -0.545128 0.037500 0.196779\nv -0.526192 0.037500 0.120854\nv -0.460361 0.037500 0.114401\nv -0.370422 0.037500 0.138334\nv -0.288349 0.037500 0.136148\nv -0.241306 0.037500 0.070278\nv -0.237156 0.037500 -0.021114\nv -0.278931 0.037500 -0.080936\nv -0.362991 0.037500 -0.072300\nv -0.459194 0.037500 -0.039099\nv -0.530743 0.037500 -0.045435\nv -0.551212 0.037500 -0.135216\nv -0.535744 0.037500 -0.271538\nv -0.487217 0.037500 -0.498785"""
#test_vertices = [(float(x.split(" ")[1]),float(x.split(" ")[3])) for x in objtxt.replace("\r","").strip("\n").split("\n")]

def getPieceVerticesFromFile(f):
    verts = []
    with f.open('rb') as fin:
        for l in fin.readlines():
            if l[0] == "v":
                v = l.strip("\n").split(" ")
                if float(v[2]) < 0:
                    break
                verts += [(float(v[1]),float(v[3]))]
    return verts

def getConvexDecomposition(verts, method = 2):
    if method == 1:
        return pd.polygonQuickDecomp(verts)
    elif method == 2:
        return py2d.Polygon.convex_decompose(py2d.Polygon.from_tuples(verts))
    elif method == 3:
        a = pd.polygonQuickDecomp(verts)
        b = py2d.Polygon.convex_decompose(py2d.Polygon.from_tuples(verts))
        if len(a) < len(b) and len(a) != 0:
            return a
        return b
        

def displayDecompFromFile(f):
    if isPyGameStarted:
        gameDisplay.fill(black)
    verts = getPieceVerticesFromFile(f)
    decomp = getConvexDecomposition(verts)
    printDecomp(decomp)
            
    
def printDecomp(decomp):
    min_x = 999999999
    min_y = 999999999
    max_x = -999999999
    max_y = -999999999
    for g in decomp:
        for p in g:
            min_x, min_y = min(min_x, p[0]), min(min_y, p[1])
            max_x, max_y = max(max_x, p[0]), max(max_y, p[1])
    dx = max(1, max_x - min_x)/(16/9.0)
    dy = max(1, max_y - min_y)
    dd = 1.0 * max(dx,dy)
    for g in decomp:
        clr = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        for i,p in enumerate(g):
            #print(str(p[0])+"\t"+str(p[1]))
            drawLine(((p[0]-min_x)/dd,(p[1]-min_y)/dd),((g[i+1 if i+1 < len(g) else 0][0]-min_x)/dd,(g[i+1 if i+1 < len(g) else 0][1]-min_y)/dd), clr)
        #print(str(g[0][0])+"\t"+str(g[0][1]))
        print("")
#printDecomp(decomp2)
#displayDecompFromFile(r"E:\Virtual Drives\Tabletop Simulator\Tabletop Simulator\Mods\Models\New folder\httpsdrivebrainsickcomttsjigsawtemplatesjigsaw48x273piece859obj.obj")
H1 = 0.0375

def generateObjBoard(width, height):
    # add 8 vertices
    obj_text = ""
    obj_text += f"v {-width/2.0:.2f} 0.07 {height/2.0:.2f}\n"
    obj_text += f"v {width/2.0:.2f} 0.07 {height/2.0:.2f}\n"
    obj_text += f"v {width/2.0:.2f} 0.07 {-height/2.0:.2f}\n"
    obj_text += f"v {-width/2.0:.2f} 0.07 {-height/2.0:.2f}\n"

    obj_text += f"v {-width/2.0:.2f} 0 {height/2.0:.2f}\n"
    obj_text += f"v {width/2.0:.2f} 0 {height/2.0:.2f}\n"
    obj_text += f"v {width/2.0:.2f} 0 {-height/2.0:.2f}\n"
    obj_text += f"v {-width/2.0:.2f} 0 {-height/2.0:.2f}\n"

    obj_text += "vt 0 0\n"
    obj_text += "vt 1 0\n"
    obj_text += "vt 1 1\n"
    obj_text += "vt 0 1\n"

    obj_text += "f 1/1 2/2 3/3 4/4\n"
    obj_text += "f 8 7 6 5\n"
    obj_text += "f 1 5 6 2\n"
    obj_text += "f 2 6 7 3\n"
    obj_text += "f 3 7 8 4\n"
    obj_text += "f 4 8 5 1\n"
    
    return obj_text
    
    

def generateObjFromVertices(verts, rot, wi, hi, nw, nh):
    # generate a clockwise array(which is ccw in video-display land)
    verts = py2d.Polygon.from_tuples(verts).clone_ccw()
    
    # find extremes
    min_x = verts.get_left()
    min_y = verts.get_top()
    d_x = verts.width
    d_y = verts.height

    #standardize decimal representation of numbers
    def fl(x, sig = 3):
        if abs(x) < 10**-sig / 2.0: return "0"
        s = "%."+str(sig)+"f"
        s = (s%x).rstrip('0').rstrip('.').lstrip('0')
        return '0' if len(s) == 0 else s

    file_text = ""
    # make a reverse lookup for vertices
    index_dict = {}
    # make top v rows
    for i, v in enumerate(verts):
        index_dict[(v[0],v[1])] = i
        if rot == 1:
            v = [v[1],-v[0]]
        elif rot == 2:
            v = [-v[0],-v[1]]
        elif rot == 3:
            v = [-v[1],v[0]]
        file_text += f"v {fl(v[0])} 0.07 {fl(v[1])}\n"

    # make bottom v rows
    for v in verts:
        if rot == 1:
            v = [v[1],-v[0]]
        elif rot == 2:
            v = [-v[0],-v[1]]
        elif rot == 3:
            v = [-v[1],v[0]]
        file_text += f"v {fl(v[0])} 0 {fl(v[1])}\n"
    
    # make vt rows
    file_text += "vt 0 0\n"
    for v in verts:
        scale_x = 1.0 / nw
        scale_y = 1.0 / nh
        offset_x = scale_x * (wi + 0.5)
        offset_y = scale_y * (hi + 0.5)
        file_text += f"vt {fl(offset_x + v[0] * scale_x, 2 + int(math.ceil(math.log10(nw)-0.5)))} {fl(1 - (offset_y + v[1] * scale_y), 2 + int(math.ceil(math.log10(nh)-0.5)))}\n"

    #file_text += "s off\n"

    decomp = getConvexDecomposition(verts.as_tuple_list())
    if len(decomp) == 0:
        print(wi, hi, nw, nh)
        Exception("no decomp")
    # make top faces
    for group in decomp:
        if len(group) > 4:
            print(wi, hi, nw, nh)
            Exception("group > 4")
        txt = "f"
        group = py2d.Polygon.from_tuples(group).clone_ccw()
        for v in group:
            ind = index_dict[(v[0],v[1])] + 1
            txt += f" {ind}/{ind + 1}"
        file_text += txt + "\n"

    n = len(verts)
    # make bottom faces
    for group in decomp:
        txt = "f"
        group = py2d.Polygon.from_tuples(group).clone_cw()
        for v in group:
            ind = index_dict[(v[0],v[1])] + 1 + n
            txt += f" {ind}"
        file_text += txt + "\n"

    # make the side faces
    for i in range(1, n + 1):
        i2 = 1 if i == n else i + 1
        file_text += f"f {i} {n+i} {n+i2} {i2}\n"

    return(file_text[:-1])

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

def generateFunkyPuzzle(width, height, POINT_COUNT):
    OUTSIDE_CORNER_MAX_SLOPE = 0.4
    CORNER_VARIANCE = 0.2
    CORNER_ANGLE_VARIANCE = 0.5 * math.pi/4
    CORNER_INSIDE_MIN = (CORNER_VARIANCE**2/10.0*2)**0.5 # if the centre edge of the corner would be less than this length, then make the length 0. Current equation works out to about 10%
    OPENING_MID_VARIANCE = 0.2
    OPENING_MIN = 0.15/2
    OPENING_MAX = 0.25
    OPENING_ANGLE = 0.3 * math.pi/4
    OPENING_HEIGHT_VARIANCE = 0.05
    BEZIER_DISTANCE_MIN = 0.1
    BEZIER_DISTANCE_MULTIPLIER = 1.8
    NUB_POS_VARIANCE = 0.15
    NUB_HEIGHT_MIN = 0.15
    NUB_HEIGHT_MAX = 0.35
    NUB_TIP_ANGLE_AVERAGE = 0.5 * math.pi/4

    # average angles based on POINT_COUNT: 3=100  4=134  5=139  6=145  7=149  8=153  9=155  10=159  11=160  12=161  13=164  14=164 15=166 16=166 17=167 18=167 19=168
    NUB_TIP_ANGLE_ADJUSTMENT = 0.5 * math.pi/2 * POINT_COUNT**-0.9 # this is approximately the angle that we can adjust the tip by so that it blends in with the resolution of the curve
    
    SHIFT_VARIANCE = 0.1


    def genNub():
        
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
            ropen_mid = random.uniform(-OPENING_MID_VARIANCE, OPENING_MID_VARIANCE)

            #The nub tip has a point and an angle that we want to use
            rtip = Vector(ropen_mid + random.uniform(-NUB_POS_VARIANCE, NUB_POS_VARIANCE),
                    random.uniform(NUB_HEIGHT_MIN, NUB_HEIGHT_MAX))
            rtip_angle = random.uniform(-NUB_TIP_ANGLE_AVERAGE, NUB_TIP_ANGLE_AVERAGE)
            rtip_angle_left = rtip_angle + random.uniform(0,NUB_TIP_ANGLE_ADJUSTMENT)
            rtip_angle_right = rtip_angle - random.uniform(0,NUB_TIP_ANGLE_ADJUSTMENT)

            # The left anchor point of the nub is specified
            ropen1 = Vector(ropen_mid - random.uniform(OPENING_MIN, OPENING_MAX),
                      random.uniform(-OPENING_HEIGHT_VARIANCE, OPENING_HEIGHT_VARIANCE))
            ropen1_angle = random.uniform(-OPENING_ANGLE, OPENING_ANGLE)
            # The bézier curve needs additional control points. If the x-distance between the anchor point
            # and the control point is > the x-distance between the anchor point and the tip point,
            # we get a curve that loops back on itself a bit to give us pretty loopy nubs.
            ropen1_bottom_dist = random.uniform(1.1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen1.x), BEZIER_DISTANCE_MIN) / math.cos(ropen1_angle)
            # Again, make the x-distance between the tip point and the second control point > between the anchor point and the tip
            ropen1_top_dist = random.uniform(1.1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen1.x), BEZIER_DISTANCE_MIN) / math.cos(rtip_angle_left)

            #the right anchor point of the nub is specified
            ropen2 = Vector(ropen_mid + random.uniform(OPENING_MIN, OPENING_MAX),
                      random.uniform(-OPENING_HEIGHT_VARIANCE, OPENING_HEIGHT_VARIANCE))
            ropen2_angle = random.uniform(-OPENING_ANGLE, OPENING_ANGLE)
            ropen2_bottom_dist = random.uniform(1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen2.x), BEZIER_DISTANCE_MIN) / math.cos(ropen2_angle)
            ropen2_top_dist = random.uniform(1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen2.x), BEZIER_DISTANCE_MIN) / math.cos(rtip_angle_right)

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

                #if the turn radius of the tip is more than 3x pointier, or the tip turn radius  then reject this nub
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
            bez1_points = [bez1.point_t(1.0*t/POINT_COUNT) for t in range(POINT_COUNT)]
            bez2_points = [bez2.point_t(1.0*t/POINT_COUNT) for t in range(POINT_COUNT + 1)]
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

    def genVertNub(i_row, i_column):
        t1 = py2d.Transform.move(i_column + 0.5, i_row + 1)
        return [t1 * p for p in genNub()]

    def genHorizNub(i_row, i_column):
        t1 = py2d.Transform.move(i_column + 1, i_row + 0.5)
        t2 = py2d.Transform.rotate(math.pi/2)
        t3 = py2d.Transform.mirror_y()
        return [t1 * t2 * t3 * p for p in genNub()]

    def genShiftedCorner(hi, wi, horiz_nubs, vert_nubs):
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
            rc1 = random.uniform(max(-CORNER_VARIANCE, (W_point[0] - wi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(CORNER_VARIANCE, (E_point[0] - wi - 1)*closeness))
        else:
            max_dist = min(abs(W_point[0] - wi - 1), abs(E_point[0] - wi - 1))*closeness2
            rc1 = random.uniform(max(-CORNER_VARIANCE, (S_point[1] - hi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(CORNER_VARIANCE, (N_point[1] - hi - 1)*closeness))
        # ropening == "down" means the corners connect to N & W edges and S & E edges. Likewise "up" means corners connect to SW and NE.
        ropening = ['down','up'][random.randint(0,1)]

        t1 = py2d.Transform.move(wi + 1, hi + 1)
        if abs(rc2 - rc1) < CORNER_INSIDE_MIN:
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

            rrotation = random.uniform(-CORNER_ANGLE_VARIANCE, CORNER_ANGLE_VARIANCE)

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

    def genVertOutside(hi, wi):
        rx, ry = wi, hi
        if hi != 0 and hi != height:
            nub_point = vert_nubs[hi-1][0 if wi == 0 else -1][0 if wi == 0 else -1]
            nub_dist = abs(nub_point.x - wi)
            ry = nub_point.y + OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    def genHorizOutside(hi, wi):
        rx, ry = wi, hi
        if wi != 0 and wi != width:
            nub_point = horiz_nubs[0 if hi == 0 else -1][wi-1][0 if hi == 0 else -1]
            nub_dist = abs(nub_point.y - hi)
            rx = nub_point.x + OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    vert_nubs = []
    for hi in range(height - 1):
        o = []
        for wi in range(width):
            o.append(genVertNub(hi, wi))
        vert_nubs += [o]
    
    horiz_nubs = []
    for hi in range(height):
        o = []
        for wi in range(width - 1):
            o.append(genHorizNub(hi, wi))
        horiz_nubs += [o]

    outside_corners = {'vert':[[],[]], 'horiz':[[],[]]}
    for i in range(2):
        for hi in range(height + 1):
            outside_corners['vert'][i].append(genVertOutside(hi, i*width))
    for i in range(2):
        for wi in range(width + 1):
            outside_corners['horiz'][i].append(genHorizOutside(i*height, wi))

    inside_corners = []
    for hi in range(height - 1):
        o = []
        for wi in range(width - 1):
            o.append(genShiftedCorner(hi, wi, horiz_nubs, vert_nubs))
        inside_corners.append(o)

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
            p.add_points(horiz_nubs[hi][wi - 1])
            
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
            p.add_points(vert_nubs[hi][wi])

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
            p.add_points(list(reversed(horiz_nubs[hi][wi])))
            
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
            p.add_points(list(reversed(vert_nubs[hi - 1][wi])))

        # check if piece is self-intersecting
        if rejig_bad_pieces and (p.is_self_intersecting() or p.get_closest_distance_to_self() < 0.07):
            #print(f"regen {width}x{height} {wi} {hi}")
            has_self_intersecting = 1
            # regenerate nubs and continue looking for more conflicts
            if wi != 0:
                horiz_nubs[hi][wi - 1] = genHorizNub(hi, wi-1)
            if hi != height - 1:
                vert_nubs[hi][wi] = genVertNub(hi, wi)
            if wi != width - 1:
                horiz_nubs[hi][wi] = genHorizNub(hi, wi)
            if hi != 0:
                vert_nubs[hi - 1][wi] = genVertNub(hi-1, wi)
            #Then since the corners rely on the placement of the nubs, regenerate those
            #First outside corners
            if hi == 0:
                outside_corners['horiz'][0][wi] = genHorizOutside(0, wi)
                outside_corners['horiz'][0][wi+1] = genHorizOutside(0, wi+1)
            if hi == height - 1:
                outside_corners['horiz'][1][wi] = genHorizOutside(height, wi)
                outside_corners['horiz'][1][wi+1] = genHorizOutside(height, wi+1)
            if wi == 0:
                outside_corners['vert'][0][hi] = genVertOutside(hi, 0)
                outside_corners['vert'][0][hi+1] = genVertOutside(hi+1, 0)
            if wi == width - 1:
                outside_corners['vert'][1][hi] = genVertOutside(hi, width)
                outside_corners['vert'][1][hi+1] = genVertOutside(hi+1, width)
            
            #Then inside corners
            if hi != 0 and wi != 0:
                inside_corners[hi-1][wi-1] = genShiftedCorner(hi-1, wi-1, horiz_nubs, vert_nubs)
            if hi != height - 1 and wi != 0:
                inside_corners[hi][wi-1] = genShiftedCorner(hi, wi-1, horiz_nubs, vert_nubs)
            if hi != height - 1 and wi != width - 1:
                inside_corners[hi][wi] = genShiftedCorner(hi, wi, horiz_nubs, vert_nubs)
            if hi != 0 and wi != width - 1:
                inside_corners[hi-1][wi] = genShiftedCorner(hi-1, wi, horiz_nubs, vert_nubs)

                
        if has_self_intersecting:
            piece_list.add_around(hi, wi)
            continue
        piece_dict[(hi,wi)] = py2d.Polygon.from_tuples([Vector(round(q[0],3), round(q[1],3)) for q in p])
    pieces = []
    for hi in range(height):
        for wi in range(width):
            pieces.append(piece_dict[(hi, wi)])
    return pieces

def generateCasualPuzzle(width, height, POINT_COUNT):
    OUTSIDE_CORNER_MAX_SLOPE = 0.2
    CORNER_VARIANCE = 0
    CORNER_ANGLE_VARIANCE = 0 * math.pi/4
    CORNER_INSIDE_MIN = (CORNER_VARIANCE**2/10.0*2)**0.5 # if the centre edge of the corner would be less than this length, then make the length 0. Current equation works out to about 10%
    OPENING_MID_VARIANCE = 0
    OPENING_MIN = 0.2
    OPENING_MAX = 0.2
    OPENING_ANGLE = 0 * math.pi/4
    OPENING_HEIGHT_VARIANCE = 0.05
    BEZIER_DISTANCE_MIN = .15
    BEZIER_DISTANCE_MULTIPLIER = 2.2
    NUB_POS_VARIANCE = 0
    NUB_HEIGHT_MIN = 0.3
    NUB_HEIGHT_MAX = 0.35
    NUB_TIP_ANGLE_AVERAGE = 0.2 * math.pi/4

    # average angles based on POINT_COUNT: 3=100  4=134  5=139  6=145  7=149  8=153  9=155  10=159  11=160  12=161  13=164  14=164 15=166 16=166 17=167 18=167 19=168
    NUB_TIP_ANGLE_ADJUSTMENT = 0.5 * math.pi/2 * POINT_COUNT**-0.9 # this is approximately the angle that we can adjust the tip by so that it blends in with the resolution of the curve
    
    SHIFT_VARIANCE = 0.3


    def genNub():
        
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
            ropen_mid = random.uniform(-OPENING_MID_VARIANCE, OPENING_MID_VARIANCE)

            #The nub tip has a point and an angle that we want to use
            rtip = Vector(ropen_mid + random.uniform(-NUB_POS_VARIANCE, NUB_POS_VARIANCE),
                    random.uniform(NUB_HEIGHT_MIN, NUB_HEIGHT_MAX))
            rtip_angle = random.uniform(-NUB_TIP_ANGLE_AVERAGE, NUB_TIP_ANGLE_AVERAGE)
            rtip_angle_left = rtip_angle + random.uniform(0,NUB_TIP_ANGLE_ADJUSTMENT)
            rtip_angle_right = rtip_angle - random.uniform(0,NUB_TIP_ANGLE_ADJUSTMENT)

            # The left anchor point of the nub is specified
            ropen1 = Vector(ropen_mid - random.uniform(OPENING_MIN, OPENING_MAX),
                      random.uniform(-OPENING_HEIGHT_VARIANCE, OPENING_HEIGHT_VARIANCE))
            ropen1_angle = random.uniform(-OPENING_ANGLE, OPENING_ANGLE)
            # The bézier curve needs additional control points. If the x-distance between the anchor point
            # and the control point is > the x-distance between the anchor point and the tip point,
            # we get a curve that loops back on itself a bit to give us pretty loopy nubs.
            ropen1_bottom_dist = random.uniform(1.1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen1.x), BEZIER_DISTANCE_MIN) / math.cos(ropen1_angle)
            # Again, make the x-distance between the tip point and the second control point > between the anchor point and the tip
            ropen1_top_dist = random.uniform(1.1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen1.x), BEZIER_DISTANCE_MIN) / math.cos(rtip_angle_left)

            #the right anchor point of the nub is specified
            ropen2 = Vector(ropen_mid + random.uniform(OPENING_MIN, OPENING_MAX),
                      random.uniform(-OPENING_HEIGHT_VARIANCE, OPENING_HEIGHT_VARIANCE))
            ropen2_angle = random.uniform(-OPENING_ANGLE, OPENING_ANGLE)
            ropen2_bottom_dist = random.uniform(1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen2.x), BEZIER_DISTANCE_MIN) / math.cos(ropen2_angle)
            ropen2_top_dist = random.uniform(1, BEZIER_DISTANCE_MULTIPLIER) * max(abs(rtip.x - ropen2.x), BEZIER_DISTANCE_MIN) / math.cos(rtip_angle_right)

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
            bez1_points = [bez1.point_t(1.0*t/POINT_COUNT) for t in range(POINT_COUNT)]
            bez2_points = [bez2.point_t(1.0*t/POINT_COUNT) for t in range(POINT_COUNT + 1)]
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

    def genVertNub(i_row, i_column):
        t1 = py2d.Transform.move(i_column + 0.5, i_row + 1)
        return [t1 * p for p in genNub()]

    def genHorizNub(i_row, i_column):
        t1 = py2d.Transform.move(i_column + 1, i_row + 0.5)
        t2 = py2d.Transform.rotate(math.pi/2)
        t3 = py2d.Transform.mirror_y()
        return [t1 * t2 * t3 * p for p in genNub()]

    def genShiftedCorner(hi, wi, horiz_nubs, vert_nubs):
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
            rc1 = random.uniform(max(-CORNER_VARIANCE, (W_point[0] - wi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(CORNER_VARIANCE, (E_point[0] - wi - 1)*closeness))
        else:
            max_dist = min(abs(W_point[0] - wi - 1), abs(E_point[0] - wi - 1))*closeness2
            rc1 = random.uniform(max(-CORNER_VARIANCE, (S_point[1] - hi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(CORNER_VARIANCE, (N_point[1] - hi - 1)*closeness))
        # ropening == "down" means the corners connect to N & W edges and S & E edges. Likewise "up" means corners connect to SW and NE.
        ropening = ['down','up'][random.randint(0,1)]

        t1 = py2d.Transform.move(wi + 1, hi + 1)
        if 1:
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

            rrotation = random.uniform(-CORNER_ANGLE_VARIANCE, CORNER_ANGLE_VARIANCE)

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

    def genVertOutside(hi, wi):
        rx, ry = wi, hi
        if hi != 0 and hi != height:
            nub_point = vert_nubs[hi-1][0 if wi == 0 else -1][0 if wi == 0 else -1]
            nub_dist = abs(nub_point.x - wi)
            ry = nub_point.y + OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    def genHorizOutside(hi, wi):
        rx, ry = wi, hi
        if wi != 0 and wi != width:
            nub_point = horiz_nubs[0 if hi == 0 else -1][wi-1][0 if hi == 0 else -1]
            nub_dist = abs(nub_point.y - hi)
            rx = nub_point.x + OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    vert_nubs = []
    for hi in range(height - 1):
        o = []
        for wi in range(width):
            o.append(genVertNub(hi, wi))
        vert_nubs += [o]
    
    horiz_nubs = []
    for hi in range(height):
        o = []
        for wi in range(width - 1):
            o.append(genHorizNub(hi, wi))
        horiz_nubs += [o]

    outside_corners = {'vert':[[],[]], 'horiz':[[],[]]}
    for i in range(2):
        for hi in range(height + 1):
            outside_corners['vert'][i].append(genVertOutside(hi, i*width))
    for i in range(2):
        for wi in range(width + 1):
            outside_corners['horiz'][i].append(genHorizOutside(i*height, wi))

    inside_corners = []
    for hi in range(height - 1):
        o = []
        for wi in range(width - 1):
            o.append(genShiftedCorner(hi, wi, horiz_nubs, vert_nubs))
        inside_corners.append(o)

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
            p.add_points(horiz_nubs[hi][wi - 1])
            
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
            p.add_points(vert_nubs[hi][wi])

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
            p.add_points(list(reversed(horiz_nubs[hi][wi])))
            
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
            p.add_points(list(reversed(vert_nubs[hi - 1][wi])))

        # check if piece is self-intersecting
        if rejig_bad_pieces and (p.is_self_intersecting() or p.get_closest_distance_to_self() < 0.07):
            #print(f"regen {width}x{height} {wi} {hi}")
            has_self_intersecting = 1
            # regenerate nubs and continue looking for more conflicts
            if wi != 0:
                horiz_nubs[hi][wi - 1] = genHorizNub(hi, wi-1)
            if hi != height - 1:
                vert_nubs[hi][wi] = genVertNub(hi, wi)
            if wi != width - 1:
                horiz_nubs[hi][wi] = genHorizNub(hi, wi)
            if hi != 0:
                vert_nubs[hi - 1][wi] = genVertNub(hi-1, wi)
            #Then since the corners rely on the placement of the nubs, regenerate those
            #First outside corners
            if hi == 0:
                outside_corners['horiz'][0][wi] = genHorizOutside(0, wi)
                outside_corners['horiz'][0][wi+1] = genHorizOutside(0, wi+1)
            if hi == height - 1:
                outside_corners['horiz'][1][wi] = genHorizOutside(height, wi)
                outside_corners['horiz'][1][wi+1] = genHorizOutside(height, wi+1)
            if wi == 0:
                outside_corners['vert'][0][hi] = genVertOutside(hi, 0)
                outside_corners['vert'][0][hi+1] = genVertOutside(hi+1, 0)
            if wi == width - 1:
                outside_corners['vert'][1][hi] = genVertOutside(hi, width)
                outside_corners['vert'][1][hi+1] = genVertOutside(hi+1, width)
            
            #Then inside corners
            if hi != 0 and wi != 0:
                inside_corners[hi-1][wi-1] = genShiftedCorner(hi-1, wi-1, horiz_nubs, vert_nubs)
            if hi != height - 1 and wi != 0:
                inside_corners[hi][wi-1] = genShiftedCorner(hi, wi-1, horiz_nubs, vert_nubs)
            if hi != height - 1 and wi != width - 1:
                inside_corners[hi][wi] = genShiftedCorner(hi, wi, horiz_nubs, vert_nubs)
            if hi != 0 and wi != width - 1:
                inside_corners[hi-1][wi] = genShiftedCorner(hi-1, wi, horiz_nubs, vert_nubs)

                
        if has_self_intersecting:
            piece_list.add_around(hi, wi)
            continue
        piece_dict[(hi,wi)] = py2d.Polygon.from_tuples([Vector(round(q[0],3), round(q[1],3)) for q in p])
    pieces = []
    for hi in range(height):
        for wi in range(width):
            pieces.append(piece_dict[(hi, wi)])
    return pieces

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

def generateTraditionalPuzzle(width, height):
    OUTSIDE_CORNER_MAX_SLOPE = 0.2
    CORNER_VARIANCE = 0
    CORNER_ANGLE_VARIANCE = 0 * math.pi/4

    NUB_HEIGHT_VARIANCE = 0.05
    NUB_SIDEWAYS_VARIANCE = 0.08

    def genNub():
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
        
        t = py2d.Transform.move(rx*NUB_SIDEWAYS_VARIANCE,ry*NUB_HEIGHT_VARIANCE)
        nub = [t * p for p in nub]
        isInnie = random.random() > 0.5 # Decide whether nub is an innie or an outie
        if isInnie:
            return py2d.Polygon.from_tuples([(x, -y) for x,y in nub])
        else:
            return py2d.Polygon.from_tuples(nub)

    def genVertNub(i_row, i_column):
        t1 = py2d.Transform.move(i_column + 0.5, i_row + 1)
        return [t1 * p for p in genNub()]

    def genHorizNub(i_row, i_column):
        t1 = py2d.Transform.move(i_column + 1, i_row + 0.5)
        t2 = py2d.Transform.rotate(math.pi/2)
        t3 = py2d.Transform.mirror_y()
        return [t1 * t2 * t3 * p for p in genNub()]

    def genShiftedCorner(hi, wi, horiz_nubs, vert_nubs):
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
            rc1 = random.uniform(max(-CORNER_VARIANCE, (W_point[0] - wi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(CORNER_VARIANCE, (E_point[0] - wi - 1)*closeness))
        else:
            max_dist = min(abs(W_point[0] - wi - 1), abs(E_point[0] - wi - 1))*closeness2
            rc1 = random.uniform(max(-CORNER_VARIANCE, (S_point[1] - hi - 1)*closeness, -max_dist), 0)
            rc2 = random.uniform(0, min(CORNER_VARIANCE, (N_point[1] - hi - 1)*closeness))
        # ropening == "down" means the corners connect to N & W edges and S & E edges. Likewise "up" means corners connect to SW and NE.
        ropening = ['down','up'][random.randint(0,1)]

        t1 = py2d.Transform.move(wi + 1, hi + 1)
        if 1:
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

            rrotation = random.uniform(-CORNER_ANGLE_VARIANCE, CORNER_ANGLE_VARIANCE)

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

    def genVertOutside(hi, wi):
        rx, ry = wi, hi
        if hi != 0 and hi != height:
            nub_point = vert_nubs[hi-1][0 if wi == 0 else -1][0 if wi == 0 else -1]
            nub_dist = abs(nub_point.x - wi)
            ry = nub_point.y + OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    def genHorizOutside(hi, wi):
        rx, ry = wi, hi
        if wi != 0 and wi != width:
            nub_point = horiz_nubs[0 if hi == 0 else -1][wi-1][0 if hi == 0 else -1]
            nub_dist = abs(nub_point.y - hi)
            rx = nub_point.x + OUTSIDE_CORNER_MAX_SLOPE*random.uniform(-nub_dist, nub_dist)
        return Vector(rx,ry)

    vert_nubs = []
    for hi in range(height - 1):
        o = []
        for wi in range(width):
            o.append(genVertNub(hi, wi))
        vert_nubs += [o]
    
    horiz_nubs = []
    for hi in range(height):
        o = []
        for wi in range(width - 1):
            o.append(genHorizNub(hi, wi))
        horiz_nubs += [o]

    outside_corners = {'vert':[[],[]], 'horiz':[[],[]]}
    for i in range(2):
        for hi in range(height + 1):
            outside_corners['vert'][i].append(genVertOutside(hi, i*width))
    for i in range(2):
        for wi in range(width + 1):
            outside_corners['horiz'][i].append(genHorizOutside(i*height, wi))

    inside_corners = []
    for hi in range(height - 1):
        o = []
        for wi in range(width - 1):
            o.append(genShiftedCorner(hi, wi, horiz_nubs, vert_nubs))
        inside_corners.append(o)

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
            p.add_points(horiz_nubs[hi][wi - 1])
            
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
            p.add_points(vert_nubs[hi][wi])

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
            p.add_points(list(reversed(horiz_nubs[hi][wi])))
            
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
            p.add_points(list(reversed(vert_nubs[hi - 1][wi])))

        # check if piece is self-intersecting
        if rejig_bad_pieces and (p.is_self_intersecting() or p.get_closest_distance_to_self() < 0.07):
            #print(f"regen {width}x{height} {wi} {hi}")
            has_self_intersecting = 1
            # regenerate nubs and continue looking for more conflicts
            if wi != 0:
                horiz_nubs[hi][wi - 1] = genHorizNub(hi, wi-1)
            if hi != height - 1:
                vert_nubs[hi][wi] = genVertNub(hi, wi)
            if wi != width - 1:
                horiz_nubs[hi][wi] = genHorizNub(hi, wi)
            if hi != 0:
                vert_nubs[hi - 1][wi] = genVertNub(hi-1, wi)
            #Then since the corners rely on the placement of the nubs, regenerate those
            #First outside corners
            if hi == 0:
                outside_corners['horiz'][0][wi] = genHorizOutside(0, wi)
                outside_corners['horiz'][0][wi+1] = genHorizOutside(0, wi+1)
            if hi == height - 1:
                outside_corners['horiz'][1][wi] = genHorizOutside(height, wi)
                outside_corners['horiz'][1][wi+1] = genHorizOutside(height, wi+1)
            if wi == 0:
                outside_corners['vert'][0][hi] = genVertOutside(hi, 0)
                outside_corners['vert'][0][hi+1] = genVertOutside(hi+1, 0)
            if wi == width - 1:
                outside_corners['vert'][1][hi] = genVertOutside(hi, width)
                outside_corners['vert'][1][hi+1] = genVertOutside(hi+1, width)
            
            #Then inside corners
            if hi != 0 and wi != 0:
                inside_corners[hi-1][wi-1] = genShiftedCorner(hi-1, wi-1, horiz_nubs, vert_nubs)
            if hi != height - 1 and wi != 0:
                inside_corners[hi][wi-1] = genShiftedCorner(hi, wi-1, horiz_nubs, vert_nubs)
            if hi != height - 1 and wi != width - 1:
                inside_corners[hi][wi] = genShiftedCorner(hi, wi, horiz_nubs, vert_nubs)
            if hi != 0 and wi != width - 1:
                inside_corners[hi-1][wi] = genShiftedCorner(hi-1, wi, horiz_nubs, vert_nubs)

                
        if has_self_intersecting:
            piece_list.add_around(hi, wi)
            continue
        piece_dict[(hi,wi)] = py2d.Polygon.from_tuples([Vector(round(q[0],3), round(q[1],3)) for q in p])
    pieces = []
    for hi in range(height):
        for wi in range(width):
            pieces.append(piece_dict[(hi, wi)])
    return pieces

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

#def generateOutlinedPuzzleHexagons(txtPath):
    

class RNG:
    # A poor but adequate random sequence generator
    seed = None
    m = 33554393
    a = 25612572
    def __init__(self, seed):
        self.seed = (seed + 1) % self.m
    def randbetween(self, v1, v2):
        self.seed = (self.seed * self.a) % self.m
        return self.seed * (v2 - v1 + 1) // self.m + v1
    def rand(self):
        self.seed = (self.seed * self.a) % self.m
        return 1.0 * self.seed / self.m
        

def generateFiles(puzz_func, prefix):
    save_path = Path(r"D:\Pieces")
    save_path.mkdir(parents = True, exist_ok=True)
    (save_path / "data.txt").unlink()

    puzzles_to_do = [("4:3",[
                        [16,9]])]

    
    puzzles_to_do = [("16:9",[
                        [8,5],
                        [16,9],
                        [23,13],
                        [16*2,9*2],
                        [16*3,9*3],
                        [16*4,9*4],
                        [16*5,9*5],
                        [16*6,9*6]
                        ]),
                     ("3:2",[
                         [6,4],
                         [12,8],
                         [21,14],
                         [36,24],
                         [48,32],
                         [57,38],
                         [66,44],
                         [78,52]
                         ]),
                     ("4:3",[
                         [4,3],
                         [12,9],
                         [16,12],
                         [24,18],
                         [36,27],
                         [48,36],
                         [60,45],
                         [72,54]
                         ]),
                    ( "5:4",[
                         [5,4],
                         [10,8],
                         [20,16],
                         [30,24],
                         [40,32],
                         [50,40],
                         [60,48],
                         [70,56]
                         ]),
                     ("4:4",[
                         [4,4],
                         [8,8],
                         [12,12],
                         [20,20],
                         [30,30],
                         [40,40],
                         [50,50],
                         [70,70]
                         ]),
                     ("-4:5",[
                         [5,4],
                         [10,8],
                         [20,16],
                         [30,24],
                         [40,32],
                         [50,40],
                         [60,48],
                         [70,56]
                         ]),
                     ("-3:4",[
                         [4,3],
                         [12,9],
                         [16,12],
                         [24,18],
                         [36,27],
                         [48,36],
                         [60,45],
                         [72,54]
                         ]),
                     ("-2:3",[
                         [6,4],
                         [12,8],
                         [21,14],
                         [36,24],
                         [48,32],
                         [57,38],
                         [66,44],
                         [78,52]
                         ]),
                     ("-9:16",[
                        [8,5],
                        [16,9],
                        [23,13],
                        [16*2,9*2],
                        [16*3,9*3],
                        [16*4,9*4],
                        [16*5,9*5],
                        [16*6,9*6]
                        ])
                     ]

    found = 1
    seed_inc = 0
    for lbl, dims_list in puzzles_to_do:
        for nw, nh in dims_list:
            seed_inc += 1
            rng = RNG(seed_inc)
            new_label = lbl
            if lbl[0] == "-":
                new_label = lbl[1:]
                nw, nh = nh, nw

            folder_name = prefix + new_label.replace(":","x") + f"-{nw}x{nh}"
            
            if "peanuts" in folder_name:
                found = 1
                continue
            if not found:
                continue
            
            folder_path = save_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)

            with (folder_path / "board.obj").open('w') as fout:
                obj_text = generateObjBoard(nw, nh)
                fout.write(obj_text)
            
            
            puzz = puzz_func(nw, nh)
            
            #fout_piece_outlines = (folder_path / "piece_outlines.txt").open('w')

            # steps to get pieces ready
            for i, piece in enumerate(puzz):
                wi = i % nw
                hi = i // nw

                # save outline of piece
                fout_piece_outlines.write(f"{i+1}: " + ', '.join([f"({x:.10f},{y:.10f})" for x,y in piece.as_tuple_list()])+'\n')
                
                # center the piece on 0,0
                piece = [py2d.Transform.move(-wi-0.5, -hi-0.5) * p for p in piece]

                # randomly orient the pieces
                rot = rng.randbetween(0, 3)

                # generate obj text
                obj_text = generateObjFromVertices(piece, rot, wi, hi, nw, nh)
                
                # save pieces in appropriate folder jg9x16-
                with (folder_path / f"piece.{i + 1}.obj").open('w') as fout:
                    fout.write(obj_text)

            #fout_piece_outlines.close()
                    
            total_size= 0
            for f in folder_path.iterdir():
                total_size += f.lstat.st_size
            with (save_path / "data.txt").open("a") as fout:
                fout.write(f"{folder_name} width={nw} height={nh} size={total_size} seed={seed_inc}\n")
            del puzz
            # Checking the size clears away the deleted variables and frees memory
            for obj in locals().keys():
                print(obj,sys.getsizeof(locals()[obj]))
                
            
#print(generateObjFromVertices(test_vertices))
#puzz = generateFunkyPuzzle(15, 8, 5)
#puzz = generateCasualPuzzle(7, 7, 38)
#puzz = generateJaggedPuzzle(60, 60)
puzz = generateTraditionalPuzzle(6, 6)
#print(puzz)
#generateFiles(lambda w, h: generateFunkyPuzzle(w,h,5),"fk")
#generateFiles(lambda w, h: generateCasualPuzzle(w,h,7),"ca")
#generateFiles(lambda w, h: generateTraditionalPuzzle(w,h),"tr")
#generateFiles(generateJaggedPuzzle,"jg")

#sys.exit()
startPyGame()
printDecomp(puzz)
while isPyGameStarted:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            try:
                do = 2
                if do == 1:
                    f = obj_pieces_files.pop()
                    displayDecompFromFile(path_of_obj_pieces / f)
                elif do == 2:
                    if isPyGameStarted:
                        gameDisplay.fill(black)
                    p = puzz.pop(0)
                    decomp = getConvexDecomposition(p)
                    #printDecomp(decomp)
                    printDecomp([p.points])
                elif do == 3:
                    if isPyGameStarted:
                        gameDisplay.fill(black)
                    #printDecomp(genVertNub())
                    printDecomp([py2d.Polygon.from_tuples([v_get_cubic_bezier_point(Vector(0,0),Vector(1,0),Vector(0,1),Vector(1,-1),1.0*t/20) for t in range(21)])])
                elif do == 4:
                    if isPyGameStarted:
                        gameDisplay.fill(black)
                    printDecomp(generateFunkyPuzzle(6, 6, 5))
                    
            except Exception as e:
                print(e)

    pygame.display.update()
    pygame.time.wait(10)
    if 0:
        pygame.quit()
        quit()
    


#np.array([[1,H1],[

