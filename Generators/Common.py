import Constants
import random

def pop_random(l):
    return l.pop(random.randrange(0, len(l)))


def regions_touching_point(regions, p):
    count = 0
    for region in regions:
        if region.touches(p): count += 1
    return count


def point_in_regions(regions, p):
    for region in regions:
        if region.contains(p): return True
    return False


class GenerationMap:
    def __init__(self, x, y, z):
        self.XSize = x
        self.YSize = y
        self.ZSize = z
        self.Map = []
        for mX in range(0, x):
            layer = []
            for mY in range(0, y):
                column = []
                for mZ in range(0, z):
                    column.append(-1)
                layer.append(column)
            self.Map.append(layer)

    def rect_overlaps_existing_values(self, x, y, w, h, z, room_buffer, range_of_values):
        for rX in range(x - room_buffer, x + w + room_buffer):
            for rY in range(y - room_buffer, y + h + room_buffer):
                if rX >= self.XSize or rY >= self.YSize or rX < 0 or rY < 0: return True
                if self.Map[rX][rY][z] in range_of_values: return True
        return False

    def fill_rect_with_value(self, x, y, w, h, z, value):
        for rX in range(x, x + w):
            for rY in range(y, y + h):
                self.Map[rX][rY][z] = value

    def clear_layer(self, z):
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                self.Map[x][y][z] = -1

    def _add_to_count_dict(self, d, val):
        if val not in d.keys():
            d[val] = 1
        else:
            d[val] += 1

    def get_cardinal_values(self, x, y, z):
        values = {"Locations": [None, None, None, None], "Points": []}
        if x > 0:
            self._add_to_count_dict(values, self.Map[x - 1][y][z])
            values["Points"].append((x - 1, y))
            values["Locations"][Constants.DIRECTION_W] = self.Map[x - 1][y][z]
        if x < self.XSize - 1:
            self._add_to_count_dict(values, self.Map[x + 1][y][z])
            values["Points"].append((x + 1, y))
            values["Locations"][Constants.DIRECTION_E] = self.Map[x + 1][y][z]
        if y > 0:
            self._add_to_count_dict(values, self.Map[x][y - 1][z])
            values["Points"].append((x, y - 1))
            values["Locations"][Constants.DIRECTION_N] = self.Map[x][y - 1][z]
        if y < self.YSize - 1:
            self._add_to_count_dict(values, self.Map[x][y + 1][z])
            values["Points"].append((x, y + 1))
            values["Locations"][Constants.DIRECTION_S] = self.Map[x][y + 1][z]
        return values

    def merge_layers(self, source_layer, target_layer):
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                if self.Map[x][y][source_layer] >= 0:
                    self.Map[x][y][target_layer] = self.Map[x][y][source_layer]

    def set_value(self, x, y, z, val):
        self.Map[x][y][z] = val

    def get_value(self, x, y, z):
        return self.Map[x][y][z]

    def get_ordinal_values(self, x, y, z):
        values = self.get_cardinal_values(x, y, z)
        values["Locations"] += [None, None, None, None]
        if x > 0 and y > 0:
            self._add_to_count_dict(values, self.Map[x - 1][y - 1][z])
            values["Points"].append((x - 1, y - 1))
            values["Locations"][Constants.DIRECTION_NW] = self.Map[x - 1][y - 1][z]
        if x > 0 and y < self.YSize - 1:
            self._add_to_count_dict(values, self.Map[x - 1][y + 1][z])
            values["Points"].append((x - 1, y + 1))
            values["Locations"][Constants.DIRECTION_SW] = self.Map[x - 1][y + 1][z]
        if x < self.XSize - 1 and y > 0:
            self._add_to_count_dict(values, self.Map[x + 1][y - 1][z])
            values["Points"].append((x + 1, y - 1))
            values["Locations"][Constants.DIRECTION_NE] = self.Map[x + 1][y - 1][z]
        if x < self.XSize - 1 and y < self.YSize - 1:
            self._add_to_count_dict(values, self.Map[x + 1][y + 1][z])
            values["Points"].append((x + 1, y + 1))
            values["Locations"][Constants.DIRECTION_SE] = self.Map[x + 1][y + 1][z]
        return values

    def build_cardinal_region_on_point(self, x, y, z, accepted_values):
        region = Region()
        queue = list()
        queue.append((x, y))
        while len(queue) > 0:
            nextPoint = queue.pop()
            region.add(nextPoint)
            nextX = nextPoint[0]
            nextY = nextPoint[1]

            if nextX > 0 and \
               self.Map[nextX - 1][nextY][z] in accepted_values and \
               not region.contains((nextX - 1, nextY)): queue.append((nextX - 1, nextY))

            if nextX < self.XSize - 1 and \
               self.Map[nextX + 1][nextY][z] in accepted_values and \
               not region.contains((nextX + 1, nextY)): queue.append((nextX + 1, nextY))

            if nextY > 0 and \
               self.Map[nextX][nextY - 1][z] in accepted_values and \
               not region.contains((nextX, nextY - 1)): queue.append((nextX, nextY - 1))

            if nextY < self.YSize - 1 and \
               self.Map[nextX][nextY + 1][z] in accepted_values and \
               not region.contains((nextX, nextY + 1)): queue.append((nextX, nextY + 1))
        return region

    def region_touches_cardinal_values(self, region, z, values):
        for point in region.Points:
            cardinalValues = self.get_cardinal_values(point[0], point[1], z)
            for value in values:
                if cardinalValues.get(value, 0) > 0: return True
        return False

    def print_map(self):
        for z in range(0, self.ZSize):
            print '--------------------------'
            for y in range(0, self.YSize):
                line = ''
                for x in range(0, self.XSize):
                    line += "{0} ".format('-' if self.Map[x][y][z] == -1 else self.Map[x][y][z])
                print line

    def print_layer(self, z):
        print '-------------------'
        for y in range(0, self.YSize):
            line = ''
            for x in range(0, self.XSize):
                line += "{0} ".format('-' if self.Map[x][y][z] == -1 else self.Map[x][y][z])
            print line


class Region:
    def __init__(self):
        self.Points = []

    def add(self, point):
        self.Points.append(point)

    def get_cardinal_points(self, point):
        cardinals = []
        if (point[0] + 1, point[1]) in self.Points: cardinals.append((point[0] + 1, point[1]))
        if (point[0] - 1, point[1]) in self.Points: cardinals.append((point[0] - 1, point[1]))
        if (point[0], point[1] + 1) in self.Points: cardinals.append((point[0], point[1] + 1))
        if (point[0], point[1] - 1) in self.Points: cardinals.append((point[0], point[1] - 1))
        return cardinals

    def touches(self, point):
        if (point[0] + 1, point[1]) in self.Points: return True
        if (point[0] - 1, point[1]) in self.Points: return True
        if (point[0], point[1] + 1) in self.Points: return True
        if (point[0], point[1] - 1) in self.Points: return True
        return False

    def touches_points(self, points):
        for point in points:
            if (point[0] + 1, point[1]) in self.Points: return True
            if (point[0] - 1, point[1]) in self.Points: return True
            if (point[0], point[1] + 1) in self.Points: return True
            if (point[0], point[1] - 1) in self.Points: return True
        return False

    def contains(self, point):
        for p in self.Points:
            if p == point:
                return True
        return False

    def merge(self, region):
        self.Points += region.Points

    # def TouchesCardinally(self, point):
    #    for p in self.Points:
    #        if abs(p[0] - point[0]) <= 1 and \
    #           abs(p[0] - point[1]) <= 1 and \
    #           abs(p[0] - x) + abs(p[1] - y) != 2: return True
    #    return False
