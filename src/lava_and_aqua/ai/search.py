from .problem import Problem


class SearchAlgorithm:
    def __init__(self, problem: Problem) -> None:
        self.problem = problem
        self.solution = None
        self.num_of_visited_nodes = 0
        self.visited = set()

    def dfs(self, node, depth_limit=80):
        
        if self.solution or depth_limit <= 0:
            return
        
        if self.problem.is_over(node.state):
            if node.state.is_won():
                self.solution = node
            return
        
        hashed_state = node.state.__hash__()
        if hashed_state in self.visited or node.is_cycle(k=4):
            return
        
        self.visited.add(hashed_state)
        self.num_of_visited_nodes += 1
    
        depth_limit -= 1

        for child in node.expand(self.problem):
            self.dfs(child, depth_limit)

        return
