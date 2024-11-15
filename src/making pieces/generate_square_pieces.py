#!/usr/bin/env python3.7
"""
Main generator script for rectangular puzzles.

"""
import gzip
import math
import os
from pathlib import Path
import random
import sys
import json

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

import puzz_gen

random.seed(1)

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
        

def triangulateConvexPoly(poly):
    # Quick and lazy triangulate. (Won't work with concave ngons)
    ret = []
    for i in range(1, len(poly) - 1):
        ret.append((poly[0], poly[i], poly[i + 1]))
    return ret

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
        file_text += f"vt {fl(offset_x + v[0] * scale_x, 7)} {fl(1 - (offset_y + v[1] * scale_y), 7)}\n"

    #file_text += "s off\n"

    decomp_raw = getConvexDecomposition(verts.as_tuple_list())

    if len(decomp_raw) == 0:
        print(wi, hi, nw, nh)
        raise Exception("no decomp")

    # TTS can handle quads in the .obj fine, but it doesn't support any n-gon.
    # Prefer quads when we can, since it makes the file smaller, but do further breakdown
    # on larger n-gons
    decomp = []
    for group in decomp_raw:
        if len(group) > 4:
            subdecomp = triangulateConvexPoly(group)
            decomp += subdecomp
        else:
            decomp.append(group)

    # make top faces
    for group in decomp:
        if len(group) > 4:
            print("Overlarge group", len(group), wi, hi, nw, nh)
            raise Exception("group > 4")
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
    save_path = Path(r"/home/jstephens/wtmp/Pieces")
    save_path.mkdir(parents = True, exist_ok=True)
    try:
        (save_path / "data.txt").unlink()
    except FileNotFoundError:
        pass

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



    # puzzles_to_do = [("4:3", [[16,9]])]
    # puzzles_to_do = [("4:4", [[4,4]])]
    

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
            
            folder_path = save_path / prefix / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)

            print("== Processing", folder_name, "==")

            with (folder_path / "board.obj").open('w') as fout:
                obj_text = generateObjBoard(nw, nh)
                fout.write(obj_text)
            
            
            puzz, nubinfo = puzz_func(nw, nh)
            
            #fout_piece_outlines = (folder_path / "piece_outlines.txt").open('w')

            # steps to get pieces ready
            for i, piece in enumerate(puzz):
                wi = i % nw
                hi = i // nw

                # save outline of piece
                # fout_piece_outlines.write(f"{i+1}: " + ', '.join([f"({x:.10f},{y:.10f})" for x,y in piece.as_tuple_list()])+'\n')
                
                # center the piece on 0,0
                piece = [py2d.Transform.move(-wi-0.5, -hi-0.5) * p for p in piece]

                # randomly orient the pieces
                rot = rng.randbetween(0, 3)

                # generate obj text
                obj_text = generateObjFromVertices(piece, rot, wi, hi, nw, nh)
                
                # save pieces in appropriate folder jg9x16-
                with (folder_path / f"piece.{i + 1}.obj").open('w') as fout:
                    fout.write(obj_text)

                # Update nubinfo with our new rotation so nub data matches our raw/unsolved rotation
                nubinfo[i] = ''.join(np.roll(list(nubinfo[i]), -rot))

            #fout_piece_outlines.close()
                    
            total_size= 0
            for f in folder_path.iterdir():
                total_size += f.lstat().st_size
            with (save_path / "data.txt").open("a") as fout:
                fout.write(f"{folder_name} width={nw} height={nh} size={total_size} seed={seed_inc}\n")

            with (folder_path / "nubinfo.json").open('w') as fout:
                json.dump(nubinfo, fout)

            print(f"{len(puzz)} pieces handled")
            del puzz
            # Checking the size clears away the deleted variables and frees memory
            for obj in tuple(locals().keys()):
                # print(obj,sys.getsizeof(locals()[obj]))
                sys.getsizeof(locals()[obj])



#print(generateObjFromVertices(test_vertices))
# puzz, _ = generateFunkyPuzzle(4, 4, 5)
#puzz, _ = generateCasualPuzzle(7, 7, 38)
#puzz, _ = generateJaggedPuzzle(60, 60)
# puzz, _ = generateTraditionalPuzzle(6, 6)
#print(puzz)
generateFiles(lambda w, h: puzz_gen.generateFunkyPuzzle(w,h,5),"fk")
generateFiles(lambda w, h: puzz_gen.generateCasualPuzzle(w,h,7),"ca")
generateFiles(lambda w, h: puzz_gen.generateTraditionalPuzzle(w,h),"tr")
generateFiles(puzz_gen.generateJaggedPuzzle,"jg")

sys.exit()

startPyGame()
# printDecomp(puzz)
while isPyGameStarted:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            try:
                do = 3
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

