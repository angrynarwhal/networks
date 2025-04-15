from graphviz import Digraph

def create_directed_network():
    dot = Digraph(comment='Directed Network')
    #dot.attr(rankdir='LR')
    dot.attr(rankdir='LR', size="10,4!")
    nodes = list("ABCDEFGHIJKL")
    for node in nodes:
        dot.node(node)
    # Create a circular structure plus additional edges for complexity
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'),
        ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'K'),
        ('K', 'L'), ('L', 'A'), ('A', 'D'), ('C', 'F'), ('G', 'J'), ('I', 'L')
    ]
    for start, end in edges:
        dot.edge(start, end)
    dot.render('directed_network_12nodes', format='png', cleanup=True)

if __name__ == '__main__':
    create_directed_network()
    
from graphviz import Graph

def create_undirected_network():
    dot = Graph('Undirected Network', filename='undirected_network_12nodes')
    nodes = list("ABCDEFGHIJKL")
    dot.attr(rankdir='LR', size="10,4!")
    for node in nodes:
        dot.node(node)
    # Create a circular structure plus additional edges
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'),
        ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'K'),
        ('K', 'L'), ('L', 'A'), ('A', 'D'), ('C', 'F'), ('G', 'J'), ('I', 'L')
    ]
    for n1, n2 in edges:
        dot.edge(n1, n2)
    dot.render(format='png', cleanup=True)

if __name__ == '__main__':
    create_undirected_network()

  
from graphviz import Graph

#acitivites/undirected_network_12nodes.png

def create_unweighted_network():
    dot = Graph('Unweighted Network', filename='unweighted_network_12nodes')
    dot.attr(rankdir='LR', size="10,4!")
    nodes = list("ABCDEFGHIJKL")
    for node in nodes:
        dot.node(node)
    # Create a circular structure plus additional edges
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'),
        ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'K'),
        ('K', 'L'), ('L', 'A'), ('A', 'D'), ('C', 'F'), ('G', 'J'), ('I', 'L')
    ]
    for n1, n2 in edges:
        dot.edge(n1, n2)
    dot.render(format='png', cleanup=True)

if __name__ == '__main__':
    create_unweighted_network()


from graphviz import Graph

def create_weighted_network():
    dot = Graph('Weighted Network', filename='weighted_network_12nodes')
    nodes = list("ABCDEFGHIJKL")
    dot.attr(rankdir='LR', size="10,4!")
    for node in nodes:
        dot.node(node)
    # Define edges with weights (labels)
    weighted_edges = [
        ('A', 'B', '3'), ('B', 'C', '5'), ('C', 'D', '2'), ('D', 'E', '7'),
        ('E', 'F', '4'), ('F', 'G', '1'), ('G', 'H', '6'), ('H', 'I', '8'),
        ('I', 'J', '2'), ('J', 'K', '3'), ('K', 'L', '4'), ('L', 'A', '5'),
        ('A', 'D', '2'), ('C', 'F', '3'), ('G', 'J', '4'), ('I', 'L', '6')
    ]
    for n1, n2, label in weighted_edges:
        dot.edge(n1, n2, label=label)
    dot.render(format='png', cleanup=True)

if __name__ == '__main__':
    create_weighted_network()
    
from graphviz import Graph

def create_triadic_closure_diagram():
    dot = Graph('Triadic Closure', filename='triadic_closure_12nodes')
    dot.attr(rankdir='LR', size="10,4!")
    nodes = list("ABCDEFGHIJKL")
    for node in nodes:
        dot.node(node)
    # Highlighted triangle among A, B, C using red edges
    triadic_edges = [
        ('A', 'B', {'color': 'red', 'penwidth': '2'}),
        ('B', 'C', {'color': 'red', 'penwidth': '2'}),
        ('A', 'C', {'color': 'red', 'penwidth': '2'}),
    ]
    for n1, n2, attrs in triadic_edges:
        dot.edge(n1, n2, **attrs)
    # Additional connections
    extra_edges = [
        ('D', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'H'),
        ('H', 'I'), ('I', 'J'), ('J', 'K'), ('K', 'L'),
        ('A', 'D'), ('B', 'F'), ('C', 'I')
    ]
    for n1, n2 in extra_edges:
        dot.edge(n1, n2)
    dot.render(format='png', cleanup=True)

if __name__ == '__main__':
    create_triadic_closure_diagram()
    
from graphviz import Graph

def create_sparse_network():
    dot = Graph('Sparse Network', filename='sparse_network_12nodes')
    dot.attr(rankdir='LR', size="10,4!")
    nodes = list("ABCDEFGHIJKL")
    for node in nodes:
        dot.node(node)
    # Create a simple ring and only add a few extra edges for connectivity
    ring_edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'),
        ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'I'),
        ('I', 'J'), ('J', 'K'), ('K', 'L'), ('L', 'A')
    ]
    extra_edges = [
        ('A', 'D'), ('B', 'E'), ('C', 'F'),
        ('G', 'J'), ('H', 'K')
    ]
    for n1, n2 in ring_edges + extra_edges:
        dot.edge(n1, n2)
    dot.render(format='png', cleanup=True)

if __name__ == '__main__':
    create_sparse_network()
    
from graphviz import Graph

def create_dense_network():
    dot = Graph('Dense Network', filename='dense_network_12nodes')
    dot.attr(rankdir='LR', size="10,4!")
    nodes = list("ABCDEFGHIJKL")
    for node in nodes:
        dot.node(node)
    # Add multiple connections among nodes to create a dense network.
    # (This example adds many edges manually; feel free to adjust as needed.)
    dense_edges = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'), ('A', 'E'), ('A', 'F'), ('A', 'G'),
        ('B', 'C'), ('B', 'D'), ('B', 'E'), ('B', 'F'), ('B', 'H'),
        ('C', 'D'), ('C', 'E'), ('C', 'F'), ('C', 'I'),
        ('D', 'E'), ('D', 'F'), ('D', 'J'),
        ('E', 'F'), ('E', 'G'), ('E', 'H'), ('E', 'I'),
        ('F', 'G'), ('F', 'H'), ('F', 'J'), ('F', 'K'),
        ('G', 'H'), ('G', 'I'), ('G', 'J'), ('G', 'L'),
        ('H', 'I'), ('H', 'J'), ('H', 'K'), ('H', 'L'),
        ('I', 'J'), ('I', 'K'),
        ('J', 'K'), ('J', 'L'),
        ('K', 'L')
    ]
    for n1, n2 in dense_edges:
        dot.edge(n1, n2)
    dot.render(format='png', cleanup=True)

if __name__ == '__main__':
    create_dense_network()