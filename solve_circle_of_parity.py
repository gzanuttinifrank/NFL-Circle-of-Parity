from pysat.solvers import Glucose3
import sys
import time
from scrape_game_results import get_results
from create_visualization import create_circle_viz


def print_clauses(clauses):
    for c in clauses:
        cvars = []
        for v in c:
            cvars.append('{}x{}'.format('¬' if v < 0 else '', abs(v)))
        print('(' + ' OR '.join(cvars) + ')')


# Turn list of SAT assignments into list of team names in the order they appear in the solution
def get_hamiltonian_path(n_vertices, assignments):
    positive_assignments = [a for a in assignments if a > 0]
    node_names = [num_to_team[(a-1)%n_vertices+1] for a in positive_assignments]
    return node_names


def reduce_hamiltonian_path_to_SAT_and_solve(n, edges):

    def index(i, j):
        return n_vertices*i + j + 1

    n_vertices = n-1
    clauses = []

    # Each node j must appear in the path
    for j in range(n_vertices):
        clause = []
        for i in range(n):
            clause.append(index(i,j))
        clauses.append(clause)
        
    # No node j appears twice in the path
    for j in range(n_vertices):
        for i in range(n):
            for k in range(i+1, n):
                if ((i>0) or (k<n-1)) and (i!=k):
                    clauses.append((-index(i,j), -index(k,j)))
        
    # Every position i on the path must be occupied
    for i in range(n):
        clause = []
        for j in range(n_vertices):
            clause.append(index(i,j)) 
        clauses.append(clause)
        
    # No two nodes j and k occupy the same position in the path
    for j in range(n_vertices):
        for k in range(j+1, n_vertices):
            for i in range(n):
                if j!=k:
                    clauses.append((-index(i,j), -index(i,k)))

    # Nonadjacent nodes i and j cannot be adjacent in the path
    for i in range(n_vertices):
        for j in range(n_vertices):
            if i == j: 
                continue
            if (i, j) not in edges:
                for k in range(n-1):
                    clauses.append((-index(k,i), -index(k+1,j)))
                    
    # The value of each node (T/F) in the first and final (nth) position must be equal
    for j in range(n_vertices):
        clauses.append((-index(0,j),index(n-1,j)))
        clauses.append((index(0,j),-index(n-1,j)))
        
    # Add the clauses for the above 6 restrictions and solve for a path
    g = Glucose3()
    for c in clauses:
        g.add_clause(c)
        status = g.solve()
        assignments = g.get_model()
    if status:
        path = get_hamiltonian_path(n_vertices, assignments)
        # print(path)
        print('Found a valid circle!')
        return path
    else:
        print('The + ' + str(year) + ' cycle is not yet complete!')
        return None



if __name__ == '__main__':

	# Enter the current year and the last completed week below
	year = 2020
	last_completed_week = 17

	# Call get_results to scrape the above season's results and store in two dicts
	nfl_graph, score_graph = get_results(year, last_completed_week)
	nteams = len(nfl_graph.keys())

	# If every team did not or has not yet lost in the current season, a circle of parity cannot possibly be created
	beaten_teams = set([item for subl in list(nfl_graph.values()) for item in subl])
	if len(beaten_teams) < nteams:
		print('Not every team lost in ' + str(year) + ' so the circle of parity cannot exist.')
		sys.exit()

	# Similarly, if every team does not win a game a circle of parity cannot be found
	team_to_num = {}
	for tm in range(nteams):
		tm_name = list(nfl_graph.keys())[tm]
		team_to_num[tm_name] = tm + 1

		if len(nfl_graph[tm_name]) == 0:
			print('The ' + tm_name + ' were winless in ' + str(year) + ' so the circle of parity cannot exist.')
			sys.exit()

	num_to_team = {v: k for k, v in team_to_num.items()}

	# Create list of directed edges, with the winning team pointing to the team it beat in a given week
	edges = []
	cycle_length = nteams + 1
	for k in list(nfl_graph.keys()):
	    for v in nfl_graph[k]:
	        edges.append((team_to_num[k]-1,team_to_num[v]-1))

	# Call the solver function and return the final path to be drawn
	starttime = time.time()
	final_path = reduce_hamiltonian_path_to_SAT_and_solve(cycle_length, edges)
	endtime = time.time()
	print(str(year) + ': ' + str(endtime-starttime))

	if final_path:
		create_circle_viz(final_path, score_graph, year, True)


