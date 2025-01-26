import csv
import sys

from util import Node, StackFrontier, QueueFrontier
from collections import deque

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    ## source = person_id_for_name(input("Name: "))
    source = person_id_for_name("Tom Cruise")
    if source is None:
        sys.exit("Person not found.")
    ## target = person_id_for_name(input("Name: "))
    target = person_id_for_name("Tom Hanks")
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    """ test python
    source_pairs = neighbors_for_person(source)
    target_pairs = neighbors_for_person(target)

    for i in source_pairs:
        print({i})
    
    return list(source_pairs)
    raise NotImplementedError
    """
    print ("Source = " + source)
    print ("Target = " + target)

    # Node for search (movie_id, person_id)
    currentNode = ()

    # Explored Nodes is a list of explored nodes each one assigned to a path (initialization)
    exploredPaths = {}

    # parentChild is a list of relationship between the tuples
    parentChild = []

    # Frontier is a list of nodes (initialization)
    frontier = deque(neighbors_for_person(source))
    print("#######   INITIALIZATION  ######")
    for i in frontier:
        parentChild.append((('0',str(source)), (tuple(i))))

    print_frontier(frontier)
    print_paths(exploredPaths)
    print_parents(parentChild)

    isSolution = False

    print("#######   ALGORITHM  ######")
    while (isSolution == False):
        currentNode = tuple(frontier.popleft())
        print ("Exploring node: " + str(currentNode))
        isSolution = check_for_solution(currentNode, target)
        if (isSolution):
            break
        print_frontier(frontier)
        add_current_node_to_explored(currentNode, exploredPaths, parentChild)
        add_new_nodes_to_frontier(frontier, currentNode, exploredPaths, parentChild)


    # temp code so the program doesnt break
    print("#################################")
    source_pairs = neighbors_for_person(source)
    return list(source_pairs)

def check_value_in_paths(currentNode, exploredPaths):
    # Searching the currentNode in the existing paths
    value_exists = False

    for key, my_deque in exploredPaths.items():
        if currentNode in my_deque:
            #print(f"Value {currentNode} already exists in Explored Paths for key {key}.")
            value_exists = True
        break  # Stop searching if the value is found
    
    return value_exists

def add_current_node_to_explored(currentNode, exploredPaths, parentChild):
    """
    new_paths = {}
    path_to_copy = deque()
    key = 0

    # Get path to copy
    if (len(exploredPaths) > 0):
        key = find_key_of_path(currentNode, exploredPaths)
        path_to_copy = deque(exploredPaths[key])

    for i in neighbors_for_person(currentNode[1]):
        if (check_value_in_paths(i, exploredPaths)):
            pass
        else:
            path_to_copy.append(i)
            new_paths[len(exploredPaths)] = path_to_copy
    
    exploredPaths.update(new_paths)
    if key > 0: del exploredPaths[key]
    print ("Explored Nodes:")
    print(exploredPaths)
    """
    if (len(exploredPaths) == 0):
        exploredPaths[0] = deque([tuple(currentNode)])
    else:
        # Get Parent
        parent = find_parent(currentNode, parentChild)
        print(parent)
        key = find_key_of_path(parent, exploredPaths)
        print(key)
        if (key == -1):
            exploredPaths[len(exploredPaths)] = deque([currentNode])
        else:    
            exploredPaths[key].append(currentNode)

    print_paths(exploredPaths)

def find_parent(currentNode, parentChild):
    
    found_index = None
    for i, tup in enumerate(parentChild):
        if currentNode in tup:
            pair = parentChild[i]
            if (pair[1] == currentNode):
                return pair[0]
            break
            
    if found_index == None:
        raise  RuntimeError
      
def add_new_nodes_to_frontier(frontier, currentNode, exploredPaths, parentChild):
    
    for i in neighbors_for_person(currentNode[1]):
        if (i in frontier) or (check_value_in_paths(i, exploredPaths)):
            print ("Not added to the Frontier:", end=" ")
            print (str({i}))
            pass
        else:
            print ("Added to the Frontier:", end=" ")
            print (str({i}))
            frontier.append(i)
            parentChild.append([currentNode, tuple(i)])
    
    print_frontier(frontier)
    print_parents(parentChild)
    
def find_key_of_path(currentNode, exploredPaths):
    
    found = False
    for key, my_deque in exploredPaths.items():
        print (str(key))
        if currentNode in my_deque:
            found = True
            return key
            
    if not found:
        return -1

def check_for_solution(currentNode, target):
    """    
    """
    if (currentNode[1] == target):
        print("Solution Found!")
        return True
    else:
        print("Solution Not Found!")
        return False

def print_parents(parentChild):
    print ("\033[34mParent/Child:\033[0m", end = " ")
    print ("\033[34m", parentChild, "\033[0m")

def print_paths(exploredPaths):
    print ("\033[32mExplored Paths:\033[0m", end = " ")
    print ("\033[32m", exploredPaths, "\033[0m")

def print_frontier(frontier):
    print ("\033[31mFrontier:\033[0m", end = " ")
    print ("\033[31m", frontier, "\033[0m")

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
