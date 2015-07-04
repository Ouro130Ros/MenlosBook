import random
import copy
import Common

class BasicGenerator:
    def __init__(self, config):
        self.Map = None
        self.Config = config
        self.XSize = config["XSize"]
        self.YSize = config["YSize"]
        self.ZSize = config["ZSize"]
        self.RoomBuffer = 3

        self.Wall = -1
        self.Ground = -1
        self.Player = -1
        self.Rat = -1
        for entity in config["Entities"]:
            if entity["Name"] == "Ground": self.Ground = config["Entities"].index(entity)
            if entity["Name"] == "Wall": self.Wall = config["Entities"].index(entity)
            if entity["Name"] == "Player": self.Player = config["Entities"].index(entity)
            if entity["Name"] == "Rat": self.Rat = config["Entities"].index(entity)
        self.RoomDensity = config["RoomDensity"]
        self.MinRoomWidth = config["MinRoomWidth"]
        self.MaxRoomWidth = config["MaxRoomWidth"]
        self.MinRoomHeight = config["MinRoomHeight"]
        self.MaxRoomHeight = config["MaxRoomHeight"]

    def generate(self):
        self.Map = Common.GenerationMap(self.XSize, self.YSize, self.ZSize)
        self._populate_rooms()
        self._fill_maze()
        self._connect_regions()
        self._trim_ends()
        self._build_walls()
        self._place_player()
        self._place_rat()
        self.Map.print_map()
        return self.Map.Map

    def _place_player(self):
        is_not_placed = True
        while is_not_placed:
            x = random.randint(1, self.XSize-1)
            y = random.randint(1, self.YSize-1)
            if self.Map.get_value(x,y,0) == self.Ground:
                print "Player Placed " + str((x, y, self.Player))
                is_not_placed = False
                self.Map.set_value(x, y, 1, self.Player)

    def _place_rat(self):
        is_not_placed = True
        while is_not_placed:
            x = random.randint(1, self.XSize-1)
            y = random.randint(1, self.YSize-1)
            if self.Map.get_value(x,y,0) == self.Ground and self.Map.get_value(x, y, 1) == -1:
                is_not_placed = False
                print "Rat Placed"
                self.Map.set_value(x, y, 1, self.Rat)

    def _build_walls(self):
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                if self.Map.get_value(x, y, 0) == -1 and self.Map.get_ordinal_values(x, y, 0).get(self.Ground,0) > 0:
                    self.Map.set_value(x, y, 0, self.Wall)

    def _trim_ends(self):
        are_trimmed = True
        while are_trimmed:
            are_trimmed = False
            for x in range(0, self.XSize):
                for y in range(0, self.YSize):
                    if self.Map.get_value(x, y, 0) == self.Ground:
                        if self.Map.get_cardinal_values(x, y, 0).get(self.Ground, 0) == 1:
                            self.Map.set_value(x, y, 0, -1)
                            are_trimmed = True

    def _fill_maze(self):
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                ordinal_values = self.Map.get_ordinal_values(x,y,0)
                if ordinal_values.get(self.Ground, 0) > 0 and self.Map.get_value(x, y, 0) == -1:
                    self.Map.set_value(x, y, 1, 1)
        maze_regions = []
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                if self.Map.get_value(x, y, 0) == -1 and self.Map.get_value(x, y, 1) == -1:
                    is_in_region = False
                    for region in maze_regions:
                        if region.contains((x, y)):
                            is_in_region = True
                    if not is_in_region:
                        r = self.Map.build_cardinal_region_on_point(x, y, 1, [-1])
                        maze_regions.append(r)
        self.Map.clear_layer(1)

        for region in maze_regions:
            region_points = copy.deepcopy(region.Points)
            while len(region_points) > 0:
                eligible_points = []
                start_point = Common.pop_random(region_points)

                if self.Map.get_cardinal_values(start_point[0], start_point[1], 1).get(self.Ground, 0) <= 1 and 0 < \
                        start_point[0] > self.XSize - 1 and 0 < start_point[1] > self.YSize - 1:
                    self.Map.set_value(start_point[0], start_point[1], 1, self.Ground)
                    eligible_points += region.get_cardinal_points(start_point)
                    while len(eligible_points) > 0:
                        candidate = Common.pop_random(eligible_points)
                        if self.Map.get_cardinal_values(candidate[0], candidate[1], 1).get(self.Ground, 0) == 1:
                            if 0 < candidate[0] > self.XSize-1 and 0 < candidate[1] > self.YSize-1:
                                self.Map.set_value(candidate[0], candidate[1], 1, self.Ground)
                                cards_in_region = region.get_cardinal_points(candidate)
                                for cardPoint in cards_in_region:
                                    if self.Map.get_value(cardPoint[0], cardPoint[1], 1) == -1 and \
                                       self.Map.get_cardinal_values(cardPoint[0], cardPoint[1], 1).get(self.Ground, 0) == 1:
                                        eligible_points.append(cardPoint)

                        if candidate in region_points: region_points.remove(candidate)

    def _connect_regions(self):
        connectors = []
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                if self.Map.get_value(x,y,0) == -1:
                    roomCard = self.Map.get_cardinal_values(x, y, 0)
                    mazeCard = self.Map.get_cardinal_values(x, y, 1)
                    if roomCard.get(self.Ground, 0) > 0 and mazeCard.get(self.Ground, 0) > 0 and mazeCard.get(1, 0) == 0:
                        connectors.append((x, y))
        
        self.Map.merge_layers(1,0)
        self.Map.clear_layer(1)

        regions = []
        for x in range(0, self.XSize):
            for y in range(0, self.YSize):
                if self.Map.get_value(x,y,0) == self.Ground and not Common.PointInRegions(regions, (x, y)):
                    regions.append(self.Map.build_cardinal_region_on_point(x,y,0,[self.Ground]))
        deleteRegions = list()
        for region in regions:
            if not region.touches_points(connectors):
                deleteRegions.append(region)
                for point in region.Points:
                    self.Map.set_value(point[0], point[1], 0, -1)
        
        for toDelete in deleteRegions:
            regions.remove(toDelete)

        while len(connectors) > 0:
            candidate = Common.PopRandom(connectors)
            self.Map.set_value(candidate[0], candidate[1], 0, self.Ground)
            connectedRegions = list()
            for region in regions:
                if region.touches(candidate):
                    connectedRegions.append(region)
            newRegion = Common.Region()
            for region in connectedRegions:
                newRegion.merge(region)
                regions.remove(region)
            regions.append(newRegion)
            connnectorsToRemove = list()
            for connector in connectors:
                if Common.regions_touching_point(regions, connector) < 2:
                    connnectorsToRemove.append(connector)
            for rem in connnectorsToRemove:
                connectors.remove(rem)

    def _populate_rooms(self):
        failures = 0
        while failures < self.RoomDensity:
            rW = random.randint(self.MinRoomWidth, self.MaxRoomWidth)
            rH = random.randint(self.MinRoomHeight, self.MaxRoomHeight)
            rX = random.randint(1, self.XSize-rW)
            rY = random.randint(1, self.YSize-rH)

            if not self.Map.rect_overlaps_existing_values(rX, rY, rW, rH, 0, self.RoomBuffer, [self.Ground]):
                self.Map.fill_rect_with_value(rX, rY, rW, rH, 0, self.Ground)
            else:
                failures += 1
