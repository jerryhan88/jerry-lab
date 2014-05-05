from __future__ import division

from math import sqrt

STATION_DIAMETER = 16
STATION_DIAMETER_2 = STATION_DIAMETER / 2

class Node(object):
    '''
    out_lanes: dic of next node --> lane
    '''
    def __init__(self, nid, x, y, capa):
        self.nid = nid
        self.x, self.y = x, y
        self.capa = capa
        self.out_lanes = {}
    def __repr__(self):
        return str(self.id)
    def draw(self, gc):
        gc.DrawRectangle(-STATION_DIAMETER_2, -STATION_DIAMETER_2, STATION_DIAMETER, STATION_DIAMETER)

class Lane(object):
    '''
    points: all points that specifies lane
    vehicles: in the ordered of closest to node_to
    '''
    def __init__(self, node_from, node_to, intermediate_points, max_speed):
        self.node_from, self.node_to = node_from, node_to
        self.points = [(node_from.x, node_from.y)] + intermediate_points + [(node_to.x, node_to.y)]
        self.max_speed = max_speed
        self.vehicles = []
        node_from.out_lanes[node_to] = self
        # prepare.
        self.length, self.segments, self.seg_break_distance = 0, [], []
        x0, y0 = node_from.x, node_from.y
        for i in xrange(1, len(self.points)):
            x1, y1 = self.points[i]
            dx, dy = x1 - x0, y1 - y0
            self.length += sqrt(dx * dx + dy * dy)
            self.seg_break_distance.append(self.length)
            x0, y0 = x1, y1
        self.seg_break_distance.pop()  # for degenerate case
    def __repr__(self):
        return str(self.node_from) + '-' + str(self.node_to)
    def insert_vehicle(self, new_vehicle):
        '''
        NOTE used only for initializing!!
        '''
        assert new_vehicle.located_lane == self
        self.vehicles.append(new_vehicle)
        self.vehicles.sort(key=lambda v: v.offset_on_lane, reverse=True)
    def draw(self, gc):
        gc.DrawLines(self.points)

class Vehicle(object):
    '''
    ASSUME initial speed is zero.
    '''
    def __init__(self, vid, length, safety_distance, max_speed, located_lane, offset_on_lane):
        self.vid = vid
        self.length, self.safety_distance = length, safety_distance
        self.located_lane, self.offset_on_lane = located_lane, offset_on_lane
        self.max_speed = max_speed
        self.speed = 0
        self.located_lane.insert_vehicle(self)
    def __repr__(self):
        return str(self.vid)
