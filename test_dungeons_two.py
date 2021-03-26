#
# test_dungeons_two.py: creates various dungeon configurations and provides
#   tests that allow a rat to explore those dungeons. Also provides a
#   main that runs all or some subset of tests.
#
# Author: Robert W. Hasker, 2020
#

from dungeon import Dungeon, Room, Direction
from rat import Rat
from typing import *


def directions_for_rat(r: Rat, algorithm: str, target: Room) -> List[str]:
    if algorithm == 'd':
        return r.directions_to(target)
    elif algorithm == 'b':
        return r.bfs_directions_to(target)
    elif algorithm == 'i':
        return r.id_directions_to(target)
    else:
        print("Invalid algorithm code: " + algorithm)
        return []


def check_paths_match(computed_path: List[str], expected_path: List[str]) -> None:
    if computed_path != expected_path:
        print("Computed path, " + str(computed_path))
        print("... fails to match expected path, " + str(expected_path))
    assert computed_path == expected_path

def rat_in_three_room_dungeon() -> Rat:
    """Return a rat object ready to explore a dungeon with three rooms in a row."""
    r0 = Room('start here', 1)
    d = Dungeon(r0)
    r1 = Room('one', 1)
    r2 = Room('two', 2)
    r0.add_neighbor(r1, Direction.NORTH)
    r1.add_neighbor(r2, Direction.NORTH)
    d.add_room(r1)
    d.add_room(r2)
    rat = Rat(d, r0)
    return rat


def test_rat_1(algorithm, debug: bool = False) -> str:
    """Test a rat going from the start to the end of the rat/dungeon constructed
    by rat_in_three_room_dungeon. When debug is true, makes the rat echo rooms
    as they are searched.
    """
    rat = rat_in_three_room_dungeon()
    if debug:
        rat.set_echo_rooms_searched()
    last = rat.dungeon.find('two')
    path = directions_for_rat(rat, algorithm, last)
    check_paths_match(path, ['start here', 'one', 'two'])
    return "path for rat 1: " + str(path)


def rat_in_square_dungeon() -> Rat:
    """Return a rat object ready to explore a dungeon with 4 rooms in a square."""
    top_left_room = Room('top left', 1)
    bottom_left_room = Room('bottom left', 1)
    top_right_room = Room('top right', 1)
    bottom_right_room = Room('bottom right', 1)
    d = Dungeon(top_left_room)
    d.add_room(bottom_left_room)
    d.add_room(top_right_room)
    d.add_room(bottom_right_room)
    top_left_room.add_neighbor(top_right_room, Direction.EAST)
    top_left_room.add_neighbor(bottom_left_room, Direction.SOUTH)
    bottom_right_room.add_neighbor(bottom_left_room, Direction.WEST)
    bottom_right_room.add_neighbor(top_right_room, Direction.NORTH)
    rat = Rat(d, top_left_room)
    return rat


def test_rat_2(algorithm, debug: bool = False) -> str:
    """Test a rat going from the start to the end of the rat/dungeon constructed
    by rat_in_square_dungeon. When debug is true, makes the rat echo rooms as
    they are searched.
    """
    rat = rat_in_square_dungeon()
    if debug:
        rat.set_echo_rooms_searched()
    target = rat.dungeon.find('bottom right')
    path = directions_for_rat(rat, algorithm, target)
    expected_route = ['top left', 'top right', 'bottom right']
    check_paths_match(path, expected_route)
    return "path for rat 2: " + str(path)


def rat_in_looped_dungeon() -> Rat:
    """Return a rat object ready to explore a dungeon with 6 rooms where there
    are two paths from the start to the finish.
    """
    r0 = Room('start', 0)
    d = Dungeon(r0)
    r1 = Room('one', 1)
    r2 = Room('two', 1)
    r3 = Room('three', 1)
    r4 = Room('four', 1)
    r5 = Room('five', 1)
    unconnected = Room('unconnected', 1)
    # r0 -> r1, r1 -> r2, r3; r2 -> r0, r3 -> r4, r4 -> r5
    r0.add_neighbor(r1, Direction.DOWN)
    r1.add_neighbor(r2, Direction.NORTH)
    r1.add_neighbor(r3, Direction.SOUTH)
    r2.add_neighbor(r0, Direction.UP)
    r3.add_neighbor(r4, Direction.EAST)
    r4.add_neighbor(r5, Direction.SOUTH)
    d.add_room(r1)
    d.add_room(r2)
    d.add_room(r3)
    d.add_room(r4)
    d.add_room(r5)
    d.add_room(unconnected)
    rat = Rat(d, r0)
    return rat


def test_rat_3(algorithm, debug: bool = False) -> str:
    """Test a rat going from the start to the end of the rat/dungeon constructed
    by rat_in_looped_dungeon. When debug is true, makes the rat echo rooms as
    they are searched.
    """
    rat = rat_in_looped_dungeon()
    if debug:
        rat.set_echo_rooms_searched()
    last = rat.dungeon.find('five')
    path = directions_for_rat(rat, algorithm, last)
    expected_path = ['start', 'two', 'one', 'three', 'four', 'five']
    check_paths_match(path, expected_path)
    return "path for rat 3: " + str(path)


def test_rat_4(algorithm, debug: bool = False) -> str:
    """Test a rat attempting to reach an unreachable point in the rat/dungeon
    constructed by rat_in_looped_dungeon.
    """
    rat = rat_in_looped_dungeon()
    if debug:
        rat.set_echo_rooms_searched()
    impossible_goal = rat.dungeon.find('unconnected')
    path = directions_for_rat(rat, algorithm, impossible_goal)
    assert len(path) == 0
    return "path for rat 4: " + str(path)


def rat_in_dungeon_x() -> Rat:
    """Return a rat in a dungeon with several long paths and one loop."""
    # The following pseudo-map describes the basic structure of the
    # dungeon, where rooms next to each other and dashed lines indicate
    # neighbors.
    #                  north2
    #                  north1
    # west1 downstairs center east1
    #  |               south1
    # sw2              south2 stair1 upstairs-east1
    # sw3 -----------------------------> food
    #
    center = Room("center", 1)
    d = Dungeon(center)
    north1 = Room("north1", 1)
    north2 = Room("north2", 1)
    east1 = Room("east1", 1)
    down = Room("downstairs", 0)
    west1 = Room("west1", 0)
    sw2 = Room("sw2", 0)
    sw3 = Room("sw3", 0)
    south1 = Room("south1", 1)
    south2 = Room("south2", 1)
    stair1 = Room("stair1", 2)
    upstairs_east1 = Room("upstairs-east1", 2)
    food_room = Room("food", 1)
    d.add_room(north1)
    d.add_room(north2)
    d.add_room(east1)
    d.add_room(down)
    d.add_room(west1)
    d.add_room(sw2)
    d.add_room(sw3)
    d.add_room(south1)
    d.add_room(south2)
    d.add_room(stair1)
    d.add_room(upstairs_east1)
    d.add_room(food_room)

    center.add_neighbor(north1, Direction.NORTH)
    north1.add_neighbor(north2, Direction.NORTH)
    center.add_neighbor(down, Direction.DOWN)
    down.add_neighbor(west1, Direction.WEST)
    west1.add_neighbor(sw2, Direction.SOUTH)
    sw2.add_neighbor(sw3, Direction.SOUTH)
    sw3.add_neighbor(food_room, Direction.UP)
    center.add_neighbor(east1, Direction.EAST)
    center.add_neighbor(south1, Direction.SOUTH)
    south1.add_neighbor(south2, Direction.SOUTH)
    south2.add_neighbor(stair1, Direction.UP)
    stair1.add_neighbor(upstairs_east1, Direction.EAST)
    upstairs_east1.add_neighbor(food_room, Direction.DOWN)
    rat = Rat(d, center)
    return rat


def test_rat_5(algorithm, debug: bool = False) -> str:
    """Test a rat traveling from center to a room with food in it. When debug is
    true, makes the rat echo rooms as they are searched.
    """
    rat = rat_in_dungeon_x()
    if debug:
        rat.set_echo_rooms_searched()
    goal = rat.dungeon.find("food")
    path = directions_for_rat(rat, algorithm, goal)
    expected_path = ['center', 'south1', 'south2', 'stair1', 'upstairs-east1',
        'food']
    check_paths_match(path, expected_path)
    return str(path)


def test_rat_6(algorithm, debug: bool = False) -> str:
    """Test a rat traveling from center to a room with food in it. In this case,
    there's been a cave-in in stair1 and south2 now goes to a new room,
    forcing a path through downstairs. When debug is true, makes the rat echo
    rooms as they are searched.
    """
    rat = rat_in_dungeon_x()
    south2 = rat.dungeon.find('south2')
    new_stairs = Room("hidden stairway", 3)
    rat.dungeon.add_room(new_stairs)
    south2.add_neighbor(new_stairs, Direction.UP)
    if debug:
        rat.set_echo_rooms_searched()
    goal = rat.dungeon.find("food")
    path = directions_for_rat(rat, algorithm, goal)
    expected_path = ['center', 'downstairs', 'west1', 'sw2', 'sw3', 'food']
    check_paths_match(path, expected_path)
    return str(path)


def connect_neighbors(dungeon: Dungeon, row: int, col: int) -> None:
    """Connects the room at the given row, col to all neighbors"""
    current_room = dungeon.find(str(row) + "," + str(col))
    if row != 0:
        room = dungeon.find(str(row - 1) + "," + str(col))
        current_room.add_neighbor(room, Direction.NORTH)
    if col != 0:
        room = dungeon.find(str(row) + "," + str(col - 1))
        current_room.add_neighbor(room, Direction.WEST)


def rat_in_fully_connected_grid() -> Rat:
    """Return a rat in a fully connected dungeon of 20 by 20 rooms"""
    start = Room("0,0", 1)
    d = Dungeon(start)
    for row in range(0, 20):
        for col in range(0, 20):
            if row > 0 or col > 0:
                d.add_room(Room(str(row) + "," + str(col), 1))
    for row in range(0, 20):
        for col in range(0, 20):
            connect_neighbors(d, row, col)
    rat = Rat(d, start)
    return rat


def test_rat_7(algorithm, debug: bool = False) -> str:
    """Test a rat traveling from 0,0 to 19,19. When debug is true, makes the rat
    echo rooms as they are searched.
    """
    rat = rat_in_fully_connected_grid()
    if debug:
        rat.set_echo_rooms_searched()
    goal = rat.dungeon.find("19,19")
    path = directions_for_rat(rat, algorithm, goal)
    #print("path 6: " + str(path))
    assert len(path) > 19 and path[-1] == '19,19'
    return str(path)


def run_first_six(algorithm, debug: bool = False) -> None:
    """Runs test cases 1-6, the ones that work for all algorithms.
    When debug is true, makes the rat echo rooms as they are searched.
    """
    test_rat_1(algorithm, debug)
    test_rat_2(algorithm, debug)
    test_rat_3(algorithm, debug)
    test_rat_4(algorithm, debug)
    test_rat_5(algorithm, debug)
    test_rat_6(algorithm, debug)
    print("Tests 1-6 pass.")


def main() -> int:
    """Main test program which prompts user for tests to run and displays any
    result.
    """
    n = int(input("Enter test number (1-7; 0 = run 1-6): "))
    response = input("Debug (y/n)? ")
    debug = response == 'y' or response == 'Y'
    response = input("Search algorithm: (d)epth-first, (b)readth-first, (i)terative deepening: ")
    algorithm = response.casefold()[0]
    if n == 0:
        run_first_six(algorithm, debug)
        return 0
    elif n == 1:
        result = test_rat_1(algorithm, debug)
    elif n == 2:
        result = test_rat_2(algorithm, debug)
    elif n == 3:
        result = test_rat_3(algorithm, debug)
    elif n == 4:
        result = test_rat_4(algorithm, debug)
    elif n == 5:
        result = test_rat_5(algorithm, debug)
    elif n == 6:
        result = test_rat_6(algorithm, debug)
    elif n == 7:
        result = test_rat_7(algorithm, debug)
    else:
        print("Error: unrecognized test number " + str(n))
    print("Test passes with result " + str(result))
    return 0


if __name__ == "__main__":
    exit(main())