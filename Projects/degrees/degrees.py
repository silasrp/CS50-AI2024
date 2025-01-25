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

    # Frontier is a list of nodes (initialization)
    frontier = deque(neighbors_for_person(source))
    print ("Added to the Frontier:")
    for i in frontier:
        print ({i})

    # Explored Nodes is a list of explored nodes (initialization)
    exploredPaths = deque()
    
    isSolution = False

    while (isSolution == False):
        currentNode = tuple(frontier.popleft())
        exploredPaths.append(currentNode)
        print ("Explored Nodes:")
        for i in exploredPaths:
            print (str({i}))
        isSolution = check_for_solution(currentNode, target)
        print ("Added to the Frontier:")
        add_new_nodes_to_frontier(frontier, currentNode, exploredPaths)


    
    # temp code so the program doesnt break
    print("#################################")
    source_pairs = neighbors_for_person(source)
    return list(source_pairs)


def add_new_nodes_to_frontier(frontier, currentNode, exploredNodes):
    # add to the frontier only if element is not already on the list
    for i in neighbors_for_person(currentNode[1]):
        if (i in frontier) or (i in exploredNodes):
            pass
        else:
            frontier.append(i)            
            print ({i})


def check_for_solution(currentNode, target):
    """    
    """
    print ("Current Node = " + str(currentNode[1]))
    if (currentNode[1] == target):
        return True
    else:
        return False



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
