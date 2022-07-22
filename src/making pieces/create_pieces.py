#!/usr/bin/env python3.7
import math
import random
import itertools
import pathlib
import py2d
from gzip import GzipFile

# This hex piece creation script was created by Cashew
# This script produces hexagonal boards and pieces given the dimensions of two side-lengths of the board
# Calling the make_puzzle function with all these parameters creates a final puzzle that can be used in Tabletop Simulator

# Efficiently iterate over overlapping pairs including (last, first), e.g.:
#   list(ring_pairs([1,2,3])) -> [(1,2),(2,3),(3,1)]
def ring_pairs(i):
    return zip(i, itertools.chain(itertools.islice(i, 1, None), itertools.islice(i, None, 1)))

def plot_polygon(poly):
    import matplotlib.pyplot as plt
    poly_closed = poly + poly[:1]
    plt.plot([p[0] for p in poly_closed], [p[1] for p in poly_closed])
    plt.show()

# Transform each 2D point from the coordinate system defined by directed line segment ((0, 0), (1, 0)) to the coordinate
# system defined by the given directed line segment:
#   transform_x_to_line_seg([(1, 1)], ((2, -1), (4, 1))) -> [(2, 3)]
def transform_x_to_line_seg(points, seg):
    x1, y1 = seg[0]
    x2, y2 = seg[1]
    dx, dy = x2 - x1, y2 - y1
    return [(p[0] * dx - p[1] * dy + x1, p[0] * dy + p[1] * dx + y1) for p in points]


# Intersection point of two infinite lines each defined by two points: ((x1,y1),(x2,y2)) and ((x3,y3),(x4,y4)).
def intersect_lines(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]
    x12, y12 = x1 - x2, y1 - y2
    x34, y34 = x3 - x4, y3 - y4
    xy12 = x1 * y2 - y1 * x2
    xy34 = x3 * y4 - y3 * x4
    d = x12 * y34 - y12 * x34
    return (xy12 * x34 - x12 * xy34) / d, (xy12 * y34 - y12 * xy34) / d


class KnobSelector:
    def __init__(self, filepath):
        self.knobs = []
        with (GzipFile(filepath, 'r') if '.gz' in filepath else open(filepath, 'rb')) as f:
            for line in f:
                self.knobs.append([tuple(float(c) for c in p.split(b',')) for p in line.split(b' ')])

    def random_selector(self):
        knob = random.choice(self.knobs)
        if random.randrange(2) == 1:
            return [(p[0], -p[1]) for p in knob]
        else:
            return knob


# Width and height are not quite that, but refer to the short and long sides. Example for width=4, height=3:
#   O O O O
#  O O O O O
# O O O O O O
#  O O O O O
#   O O O O
# The O's are hexagon pieces, oriented with points at top and bottom and vertical edges to the sides.
def create_hexagon_pieces(width, height, knob_func, edge_len=1.0, trim=True):
    assert width >= 2 and height >= 2
    # the corners are ordered in the array in a brick-wall pattern as if the hexagon's upper/lower points were squashed:
    #  \   / \   /
    #   \ /   \ /                     *--*--*--*--*
    #    |     |                         |     |
    #    |     |                         |     |
    #   / \   / \          --->       *--*--*--*--*
    #  /   \ /   \                    |     |     |
    # |     |     |                   |     |     |
    # |     |     |                   *--*--*--*--*
    #  \   / \   /
    #   \ /   \ /
    # col/row and x/y are both right/down
    pieces_cols_mid = width + height - 1
    pieces_rows = height * 2 - 1
    corners_cols = pieces_cols_mid * 2 + 1
    corners_rows = pieces_rows + 1

    # lattice point coords
    corners: list[list] = [[None for _ in range(corners_rows)] for _ in range(corners_cols)]  # [col][row]
    for row in range(corners_rows):
        for col in range(corners_cols):
            x = edge_len * (col - pieces_cols_mid) * math.sqrt(3) / 2
            y = edge_len * ((row - height) * 1.5 + 0.5 + (col + row + height) % 2 * 0.5)
            corners[col][row] = (x, y)

    # pieces
    pieces = []  # [[(c0, c1), (c1, c2), (c2, c3), (c3, c4), (c4, c5), (c5, c0)], ...]
    piece_centers = []
    board_polygon = [(0, 0)] * 6  # to be replaced as we go
    # col/row here is the index pair for the hexagon's upper-left corner
    for row in range(pieces_rows):
        col_from = height - row - 1 if row < height else row - height + 1
        col_to = corners_cols - col_from - 2  # exclusive
        for col in range(col_from, col_to, 2):
            piece_corners = [corners[col][row], corners[col+1][row], corners[col+2][row],
                             corners[col+2][row+1], corners[col+1][row+1], corners[col][row+1]]
            piece_centers.append((corners[col+1][row][0], (corners[col+1][row][1] + corners[col+1][row+1][1]) / 2))
            # trim puzzle boundary
            if trim:
                trim_points = []  # clockwise list of piece_corners indices
                if row == 0 and col == col_to - 1:
                    trim_points = [0, 1, 2, 3]
                elif row == height - 1 and col == col_to - 1:
                    trim_points = [1, 2, 3, 4]
                elif row == pieces_rows - 1 and col == col_to - 1:
                    trim_points = [2, 3, 4, 5]
                elif row == pieces_rows - 1 and col == col_from:
                    trim_points = [3, 4, 5, 0]
                elif row == height - 1 and col == col_from:
                    trim_points = [4, 5, 0, 1]
                elif row == 0 and col == col_from:
                    trim_points = [5, 0, 1, 2]
                elif row == 0:
                    trim_points = [0, 1, 2]
                elif row < height and col == col_to - 1:
                    trim_points = [1, 2, 3]
                elif row >= height and col == col_to - 1:
                    trim_points = [2, 3, 4]
                elif row == pieces_rows - 1:
                    trim_points = [3, 4, 5]
                elif row >= height and col == col_from:
                    trim_points = [4, 5, 0]
                elif row < height and col == col_from:
                    trim_points = [5, 0, 1]
                if len(trim_points) == 3:
                    piece_corners.pop(trim_points[1])
                elif len(trim_points) == 4:
                    new_corner = intersect_lines((piece_corners[trim_points[0]], piece_corners[trim_points[2]]),
                                                 (piece_corners[trim_points[1]], piece_corners[trim_points[3]]))
                    piece_corners[trim_points[1]] = new_corner
                    piece_corners.pop(trim_points[2])
                    board_polygon[trim_points[0]] = new_corner
            # store corner pairs
            piece_edges = list(ring_pairs(piece_corners))
            pieces.append(piece_edges)

    # assign knobs to shared edges, and assign neighbors based on that
    edges = {}
    edge_to_piece = {}
    neighbors = [[] for _ in pieces]
    # populate empty values at first just so we can lookup existence when assigning knobs
    for i, p in enumerate(pieces):
        for e in p:
            assert e not in edges
            edges[e] = None
            edge_to_piece[e] = i
    # assign knobs when an edge exists in both directions (thus shared by neighboring pieces)
    for e in edges:
        if edges[e] is None:
            er = tuple(reversed(e))
            if er in edges:
                knob = transform_x_to_line_seg(knob_func(), e)
                edges[e] = knob
                edges[er] = list(reversed(knob))
                neighbors[edge_to_piece[e]].append(edge_to_piece[er])
                neighbors[edge_to_piece[er]].append(edge_to_piece[e])

    # assemble piece polygons
    piece_polygons = []
    for p in pieces:
        polygon = []
        for e in p:
            polygon.append(e[0])
            knob = edges[e]
            if knob is not None:
                polygon.extend(knob)
        piece_polygons.append(polygon)

    # make the board polygon
    assert trim  # untrimmed board not yet implemented
    board_center = (0, 0)

    return board_polygon, board_center, piece_polygons, piece_centers, neighbors

def spiralizer(max_dist):
    # returns an iterator of x,y values that spiral around (0,0) starting at (0,0)
    # up to a maximum integer distance of max_dist
    dist = 0
    direc = 4
    count = 0
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    x = y = 0
    while dist <= max_dist:
        yield x, y
        if direc >= 4:
            dist += 1
            count = 0
            direc = 0
            x = y = -dist
        x += directions[direc][0]
        y += directions[direc][1]
        count += 1
        if count == dist * 2:
            direc += 1
            count = 0


#   Takes a polygon as a list of 2D vertex tuples, tesselates it into faces, then
# texture-maps a picture onto the resulting vertices and transforms them by shifting them from the given center to the
# origin, rotating them around that origin, and scaling them.
#   The input polygon must be non-self-intersecting and with no duplicate points, but may be clockwise or
# counterclockwise. Each output face (and the perimeter) will be counterclockwise (by screen convention: +X right, +Y
# down), and will have between 3 and face_max_verts vertices. All outputs will contain 2D vertex tuples.
#  The sig value is the number of decimal places the vertices need to be rounded to. The algorithm must pick rounded
# vertices that create a new shape that can completely contain the old shape(this guarantees that pieces when put
# together will overlap instead of having gaps. It looks nicer that way.)
# Outputs:
#   faces: list of faces each as a list of vertex tuples
#   perimeter: list of just the outer vertex tuples in clockwise order (excluding any added interior points)
#   all_vertices: set of all vertices used in the faces and perimeter
#   vertex_to_texture: dict mapping only the face vertex tuples to texture U/V tuples
def tesselate_transform_and_texture(vertices: [(float, float)], center: (float, float),
                                           picture_rect: ((float, float), (float, float)), rotate_deg, scale,
                                           face_max_verts, sig):
    # Implementation notes:
    #   * We need to convert Vector objects to plain tuples when using them as dict indexes, because the Vector object
    #     hashing/equality functions use proximity within an epsilon instead of exact equality.
    #   * While py2d.Polygon.convex_decompose appears to not merge vertices or add interior/perimeter vertices, we act
    #     as if it might, in case we ever replace it with some other decomposer.


    # make a counterclockwise polygon from the vertex list
    polygon = py2d.Polygon.from_tuples(vertices).clone_ccw()

    # move polygon from the given center to the origin, and scale/rotate it as requested
    polygon_transform = py2d.Transform.move(-center[0], -center[1])
    polygon_transform = py2d.Transform.scale(scale, scale) * polygon_transform
    polygon_transform = py2d.Transform.rotate(math.radians(rotate_deg)) * polygon_transform
    polygon_transformed = py2d.Polygon.from_tuples([polygon_transform * v for v in polygon])

    # round all vertices to locations that can completely contain the original shape
    # for each vertex, find a rounded vertex coord that lies outside the original shape and that also has lines
    # to its neighbours that are outside the original shape
    for i, v in enumerate(polygon_transformed):
        v_start = py2d.Vector(round(v.x, sig), round(v.y, sig))
        delta = 10**(-sig)
        v_next = polygon_transformed[(i+1)%len(polygon_transformed)]
        v_prev = polygon_transformed[i-1]
        # search in a spiral around v_start for a valid point
        found_replacement = 0
        for ix, iy in spiralizer(4):
            v_new = v_start + py2d.Vector(ix * delta, iy * delta)
            # a rounded point v_new that will create lines lying outside the current shape satisfies the following
            if py2d.Polygon.is_clockwise_s([v, v_next, v_new]) \
                    and py2d.Polygon.is_clockwise_s([v, v_new, v_prev]):
                polygon_transformed[i] = v_new
                break

    # create the original polygon with the new vertices
    polygon_transform = py2d.Transform.rotate(math.radians(-rotate_deg))
    polygon_transform = py2d.Transform.scale(1/scale, 1/scale) * polygon_transform
    polygon_transform = py2d.Transform.move(center[0], center[1]) * polygon_transform
    polygon_offset_vertices = py2d.Polygon.from_tuples([polygon_transform * v for v in polygon_transformed])

    # make a reverse index lookup for vertices so we can convert the face decomposition back into indexes
    vertex_index = {(v[0],v[1]):i for i, v in enumerate(polygon_transformed)}

    # tessellate the polygon into low-count faces
    # note that py2d.Polygon.convex_decompose accepts cw or ccw and emits cw components
    face_polygons = py2d.Polygon.convex_decompose(polygon_transformed, max_vertices=face_max_verts)
    if len(face_polygons) == 0:
        raise ValueError('py2d.Polygon.convex_decompose failed to tessellate the given polygon')
    faces = []
    for fp in face_polygons:
        if not fp.is_clockwise:
            raise ValueError("py2d.Polygon.convex_decompose normally returns clockwise faces but didn't, so the input "
                             "or offset polygons might be self-intersecting")
        if not 3 <= len(fp) <= face_max_verts:
            raise ValueError('py2d.Polygon.convex_decompose returned a face with too few/many vertices')
        fp_tuples = list(reversed(fp.as_tuple_list())) # make ccw tuples
        faces.append([vertex_index[x] for x in fp_tuples])

    # map face vertices to texture coords
    picture_width = picture_rect[1][0] - picture_rect[0][0]
    picture_height = picture_rect[1][1] - picture_rect[0][1]
    texture_transform = py2d.Transform.move(-picture_rect[0][0], -picture_rect[1][1])
    texture_transform = py2d.Transform.scale(1/picture_width, -1/picture_height) * texture_transform
    texture_polygon = [texture_transform * v for v in polygon_offset_vertices]

    return faces, polygon_transformed, texture_polygon


#   Creates an extruded 3D model of a 2D polygon in Wavefront OBJ format as a string, with the 2D X/Y coordinates
# becoming 3D X/Z coordinates with extrusion along the Y axis, and a picture texture-mapped to only the top (+Y) face.
# Faces with up to face_max_verts are used, e.g. 4 to use only tris and quads.
#   The input polygon (list of vertices) may be clockwise or counterclockwise, as it will be flipped as needed. And it
# need not be convex. But it must be a single non-self-intersecting polygon. Vertex/picture coords are in the screen
# convention (+X right, +Y down).
#   To reduce the size of the obj file, numbers are written without leading/trailing 0's or a trailing decimal point,
# except as necessary (e.g. '.01', '.1', '1', '10', '0', '-.1') and single-char newlines are used (but it's up to the
# caller to prevent Python from converting to e.g. Windows-style newlines when writing the file).
#   All parameters are in terms of the unscaled vertex coords. The obj coords will be rounded to the minimum number of
# decimal places required to avoid more absolute rounding error than the respective parameter. The plane scaling is
# performed only in the X and Z directions (corresponding to the original X and Y), as the thickness arguments control
# the Y extrusion direction, and max_vertex_1d_error refers to the original (vertex) coords. The picture will be
# texture- mapped such that obj texture coords (0, 1) and (1, 0) correspond to picture_rect[0] and picture_rect[1]
# respectively, and max_texture_1d_error refers to the original (picture) coords. Note that the errors are only
# considered per axis independently, so the actual multi-dimensional error can be a bit greater.
#   To avoid tiny gaps between neighboring objects caused by rounding errors (particularly when objects are rotated by
# other than a multiple of 90 deg), the offset parameter can be set to some small value to extend the polygon away from
# each of its line segments so the objects overlap slightly. The offset should be set to at least max_vertex_1d_error *
# sqrt(2) to cover the worst 2D error.
#   Rounding examples:
#     * If plane_scale=1 and max_vertex_1d_error=0.005, then up to 2 decimal places will be output for vertex coords.
#     * If plane_scale=20 and max_vertex_1d_error=0.0025, then up to 1 decimal place will be output for vertex coords,
#       because rounding the final output to 1 decimal place has a max error of 0.05 in the final scaled coords,
#       corresponding to 0.0025 error in the original coords.
#     * If plane_scale=1 and max_vertex_1d_error=0.0049, then up to 3 decimal places will be output for vertex coords.
#     * If picture_rect=((-16,-9),(16,9)) and max_texture_1d_error=0.01, then up to 4 decimal places will be output
#       for the U coord and up to 3 decimal places for the V coord, because 4 and 3 decimal places on a 0-1 scale
#       correspond to errors of 0.00005*(16+16)=0.0016 and 0.0005*(9+9)=0.009 respectively in the original coords.
# Credit to Canonelis for the original version of this function.
def polygon_to_obj(vertices: [(float, float)], center: (float, float), picture_rect: ((float, float), (float, float)),
                   thickness_below=0.0, thickness_above=0.07, rotate_deg=0.0,
                   max_vertex_1d_error=0.00051, max_texture_1d_error=0.00051, plane_scale=1.0, face_max_verts=4):
    assert face_max_verts >= 3

    # determine the decimal places needed
    picture_width = picture_rect[1][0] - picture_rect[0][0]
    picture_height = picture_rect[1][1] - picture_rect[0][1]
    v_sig = math.ceil(-math.log10(max_vertex_1d_error * plane_scale * 2.0))
    vtu_sig = math.ceil(-math.log10(max_texture_1d_error / abs(picture_width) * 2.0))
    vtv_sig = math.ceil(-math.log10(max_texture_1d_error / abs(picture_height) * 2.0))

    # set a new center close to the original but that is rounded off
    center = tuple([round(x, v_sig) for x in center])

    # manipulate vertices into what we can build the obj from
    faces, polygon, texture_polygon = tesselate_transform_and_texture(
        vertices, center, picture_rect, rotate_deg, plane_scale, face_max_verts, v_sig)

    # minimize string length for decimal representation of numbers
    def fl(x, sig):
        if abs(x) < 10 ** -sig / 2.0: return "0"
        s = f'{x:.{sig}f}'.rstrip('0').rstrip('.').lstrip('0')
        return '0' if len(s) == 0 else s

    # start obj output
    lines = []

    # top vertices, mapping 2D X/Y to 3D X/Z and extruding in the +Y direction
    for v in polygon:
        lines.append(f'v {fl(v[0], v_sig)} {fl(thickness_above, v_sig)} {fl(v[1], v_sig)}')

    # bottom vertices, mapping 2D X/Y to 3D X/Z and extruding in the -Y direction
    for v in polygon:
        lines.append(f'v {fl(v[0], v_sig)} {fl(-thickness_below, v_sig)} {fl(v[1], v_sig)}')

    # first texture coords are used where not specified (sides and bottom), so use bottom-left corner of pic for those
    lines.append(f'vt 0 0')

    # texture coords for just the top face vertices
    for v in texture_polygon:
        lines.append(f'vt {fl(v[0], vtu_sig)} {fl(v[1], vtv_sig)}')

    # top faces
    for face in faces:
        lines.append(f'f {" ".join(f"{v+1}/{v+2}" for v in face)}')

    l = len(polygon)
    # bottom faces
    for face in faces:
        lines.append(f'f {" ".join(f"{l+v+1}" for v in reversed(face))}')

    # side faces
    for edge in ring_pairs(range(l)):
        quad_indexes = (edge[0]+1, l+edge[0]+1,
                        l+edge[1]+1, edge[1]+1)
        if face_max_verts >= 4:
            lines.append(f'f {" ".join(map(str, quad_indexes))}')
        else:
            lines.append(f'f {" ".join(str(quad_indexes[i]) for i in (0, 1, 2))}')
            lines.append(f'f {" ".join(str(quad_indexes[i]) for i in (2, 3, 0))}')

    # assemble lines, but omit the last newline
    return '\n'.join(lines)


# texture bounds based solely on board, as pieces should fit within that
def create_objs(obj_dir, board_polygon, board_center, piece_polygons, piece_centers, piece_rotations):
    total_size = 0
    board_min_x = min(p[0] for p in board_polygon)
    board_min_y = min(p[1] for p in board_polygon)
    board_max_x = max(p[0] for p in board_polygon)
    board_max_y = max(p[1] for p in board_polygon)
    picture_rect = ((board_min_x, board_min_y), (board_max_x, board_max_y))
    for i, (poly, center) in enumerate(zip([board_polygon] + piece_polygons, [board_center] + piece_centers)):
        rotate_deg = piece_rotations[i-1] if i > 0 else 0
        obj = polygon_to_obj(poly, center, picture_rect, rotate_deg=-rotate_deg)
        total_size += len(obj)
        path = obj_dir / ('board.obj' if i == 0 else f'piece.{i}.obj')
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', newline='\n') as f:
            f.write(obj)
    return total_size


# Simple RNG that can be used in the TTS Lua script as well to achieve the same pseudo-random sequence.
# Credit to Canonelis
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


def make_puzzle(width, height, ratio, seed, knob_func, save_path, host_url, show_plot=False):
    rng = RNG(seed)
    edge_len = 1 / math.sqrt(3)  # make hexagon have unit area
    board_polygon, board_center, piece_polygons, piece_centers, neighbors = create_hexagon_pieces(
        width, height, knob_func, edge_len)
    rotations = [rng.randbetween(0, 5) * 60.0 for _ in piece_polygons]

    folder_name = 'hc' + ratio.replace(":", "x") + f"-{width + height - 1}x{height * 2 - 1}"
    with (save_path / (folder_name+'.txt')).open('w') as f:
        for poly in piece_polygons:
            f.write(str([str(p) for p in poly])+'\n')

    total_size = create_objs(save_path / folder_name, board_polygon, board_center, piece_polygons,
                             piece_centers, rotations)

    if show_plot:
        import matplotlib.pyplot as plt
        for polygon in piece_polygons + [board_polygon]:
            polygon_closed = polygon + polygon[:1]
            plt.plot([p[0] for p in polygon_closed], [p[1] for p in polygon_closed])
        for center in piece_centers + [board_center]:
            plt.plot(center[0], center[1], marker='o')
        for i, ns in enumerate(neighbors):
            for n in ns:
                c2c = (piece_centers[i], piece_centers[n])
                connection = transform_x_to_line_seg([(0.35, 0.15), (0.65, 0.15)], c2c)
                plt.plot([connection[0][0], connection[1][0]], [connection[0][1], connection[1][1]])
        plt.show()

    piece_data_entries = (
        f'{{solutionPosition={{x={c[0]:.6f},y=1,z={-c[1]:.6f}}},'  # TODO: this assumes plane_scale=1 for polygon_to_obj
        f'solutionRotation={{x=0,y={r},z=0}},'
        f'neighbors={{{",".join(str(i+1) for i in n)}}}}}'
        for c, n, r in zip(piece_centers, neighbors, rotations)
    )
    piece_data = f'local pieceDataHex{width}x{height} = {{\n  ' + ',\n  '.join(piece_data_entries) + '\n}'
    #print(piece_data)

    board_width = max(p[0] for p in board_polygon) - min(p[0] for p in board_polygon)
    board_height = max(p[1] for p in board_polygon) - min(p[1] for p in board_polygon)
    template_data = f"""templateData['{folder_name}'] = {{dimensions = {{width={width + height - 1}, height={height * 2 - 1}}}, size={total_size}, seed={seed}, ratio='{ratio.replace(":", "x")}', shape='honeycomb'}}"""
    print(template_data)


def main():
    knob_func = KnobSelector('knobs.gz').random_selector
    save_path = pathlib.Path(r"D:\Pieces")
    host_url = 'https://raw.githubusercontent.com/CashewTTS/ttsjiggyshex/as/'

    puzzles_to_do = [("16:9",[
                        [6,3],
                        [10,5],
                        [16,8],
                        [27,13],
                        [39,19],
                        [50,24]
                        ]),
                     ("3:2",[
                         [3,2],
                         [11,7],
                         [17,11],
                         [25,16],
                         [33,21],
                         [41,26]
                         ]),
                     ("4:3",[
                         [4,3],
                         [8,6],
                         [12,9],
                         [18,14],
                         [27,21],
                         [38,29]
                         ]),
                    ( "5:4",[
                         [5,4],
                         [8,7],
                         [13,11],
                         [18,16],
                         [26,22],
                         [34,29]
                         ]),
                     ("4:4",[
                         [2,3],
                         [4,5],
                         [7,9],
                         [11,15],
                         [18,24],
                         [25,34]
                         ]),
                     ("4:5",[
                         [2,4],
                         [3,7],
                         [7,16],
                         [9,22],
                         [12,30],
                         [16,40]
                         ]),
                     ("3:4",[
                         [2,5],
                         [3,9],
                         [4,12],
                         [6,19],
                         [9,28],
                         [13,42]
                         ]),
                     ("2:3",[
                         [2,6],
                         [2,9],
                         [3,16],
                         [4,22],
                         [6,35],
                         [8,48]
                         ]),
                     ("9:16",[
                        [2,7],
                        [2,11],
                        [2,17],
                        [2,25],
                        [2,36],
                        [2,52]
                        ])
                     ]
    seed_inc = 0
    #make_puzzle(2, 2, "16:9", 11, knob_func, save_path, host_url)
    for lbl, dims_list in puzzles_to_do:
        for nw, nh in dims_list:
            seed_inc += 1
            make_puzzle(nw, nh, lbl, seed_inc, knob_func, save_path, host_url)

if __name__ == '__main__':
    main()
