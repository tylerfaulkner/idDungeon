#
# CS2400 Introduction to AI
# rat.py
#
# Spring, 2021
#
# Author: Tyler Faulkner
#
# Stub class for Lab 2
# This class creates a Rat agent to be used to explore a Dungeon
#
# Note: Instance variables with a single preceeding underscore are intended
# to be protected, so setters and getters are included to enable this convention.
#
# Note: The -> notation in the function definition line is a type hint.  This
# will make identifying the appropriate return type easier, but they are not
# enforced by Python.
#

from dungeon import Dungeon, Room, Direction
from typing import *
from queue import Queue


class Rat:
    """Represents a Rat agent in a dungeon. It enables navigation of the
    dungeon space through searching.

    Attributes:
        dungeon (Dungeon): identifier for the dungeon to be explored
        start_location (Room): identifier for current location of the rat
    """

    _echo_rooms_searched = False

    def __init__(self, dungeon: Dungeon, start_location: Room):
        """ This constructor stores the references when the Rat is
        initialized. """
        self._dungeon = dungeon
        self._start_location = start_location

    @property
    def dungeon(self) -> Dungeon:
        """ This function returns a reference to the dungeon.  """
        return self._dungeon

    def set_echo_rooms_searched(self) -> None:
        """ The _echo_rooms_searched variable is used as a flag for whether
        the rat should display rooms as they are visited. """
        self._echo_rooms_searched = True

    def path_to(self, target_location: Room) -> List[Room]:
        """ This function finds and returns a list of rooms from
        start_location to target_location.  The list will include
        both the start and destination, and if there isn't a path
        the list will be empty. This function uses depth first search. """
        frontier = [[self._start_location]]
        visited = set()
        while len(frontier) != 0:
            path = frontier.pop()
            room = path[-1]
            if room.name not in visited:
                if self._echo_rooms_searched:
                    print("Visiting: " + room.name)
                if room.name == target_location.name:
                    return path
                visited.add(room.name)
                neighbors = room.neighbors().__reversed__()
                for x in neighbors:
                    new_path = path.copy()
                    new_path.append(x)
                    frontier.append(new_path)
        return []

    def directions_to(self, target_location: Room) -> List[str]:
        """ This function returns a list of the names of the rooms from the
        start_location to the target_location. """
        path = self.path_to(target_location)
        names = []
        for x in path:
            names.append(x.name)
        return names

    def bfs_directions_to(self, target_location: Room) -> List[str]:

        """Return the list of rooms names from the rat's current location to
        the target location. Uses breadth-first search."""
        path = self.bfs_path_to(target_location)
        names = []
        for x in path:
            names.append(x.name)
        return names

    def bfs_path_to(self, target_location: Room) -> List[Room]:

        """Returns the list of rooms from the start location to the
        target location, using breadth-first search to find the path."""
        frontier = Queue(maxsize=0)
        frontier.put([self._start_location])
        visited = set()
        while not frontier.empty():
            path = frontier.get()
            room = path[-1]
            if room.name not in visited:
                if self._echo_rooms_searched:
                    print("Visiting: " + room.name)
                if room.name == target_location.name:
                    return path
                visited.add(room.name)
                neighbors = room.neighbors()
                for x in neighbors:
                    new_path = path.copy()
                    new_path.append(x)
                    frontier.put(new_path)
        return []

    def __dfs(self, depth: int, target_location: Room):
        frontier = [[self._start_location]]
        visited = set()
        while len(frontier) != 0:
            path = frontier.pop()
            room = path[-1]
            if room.name not in visited:
                if self._echo_rooms_searched:
                    print("Visiting: " + room.name)
                if room.name == target_location.name:
                    return path
                visited.add(room.name)
                neighbors = room.neighbors().__reversed__()
                for x in neighbors:
                    new_path = path.copy()
                    new_path.append(x)
                    if len(new_path)-1 <= depth:
                        frontier.append(new_path)
        return []

    def id_directions_to(self, target_location: Room) -> List[str]:

        """Return the list of rooms names from the rat's current location to
        the target location. Uses iterative deepening."""
        path = self.id_path_to(target_location)
        names = []
        for x in path:
            names.append(x.name)
        return names

    def id_path_to(self, target_location: Room) -> List[Room]:

        """Returns the list of rooms from the start location to the
        target location, using iterative deepening."""
        size = self._dungeon.size()
        path = []
        i = 1
        while (i <= size) & (len(path) == 0):
            path = self.__dfs(i, target_location)
            i += 1
        return path


