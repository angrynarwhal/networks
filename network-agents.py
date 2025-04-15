import json, sys, random
import networkx as nx
import matplotlib.pyplot as plt

def generate_random_graph(num_nodes, dynamic, time_steps, p=0.1, edge_weights=False):
    """Generate a directed graph using random linking (Erdős–Rényi model)."""
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))
    if dynamic:
        # Dynamic: add edges over time_steps iterations
        for t in range(1, time_steps+1):
            edges_added = 0
            for i in range(num_nodes):
                if random.random() < p:
                    j = random.randrange(num_nodes)
                    if j == i:
                        continue  # no self-loop
                    if G.has_edge(i, j):
                        if edge_weights:
                            # If edge already exists, increment its weight
                            G[i][j]['weight'] += 1
                    else:
                        # Add new edge (weight=1 if weighted, else no weight)
                        if edge_weights:
                            G.add_edge(i, j, weight=1)
                        else:
                            G.add_edge(i, j)
                        edges_added += 1
            print(f"Step {t}: added {edges_added} random edges")
    else:
        # Static: one-time creation of edges with probability p
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i == j: 
                    continue
                if random.random() < p:
                    if edge_weights:
                        G.add_edge(i, j, weight=random.random())
                    else:
                        G.add_edge(i, j)
        print(f"Generated random graph with probability p={p}")
    return G

def generate_preferential_attachment_graph(num_nodes, dynamic, time_steps, edges_per_step=1, edge_weights=False):
    """Generate a directed graph using preferential attachment."""
    G = nx.DiGraph()
    if dynamic:
        # Start with a small initial fully-connected core network
        initial_nodes = edges_per_step + 1
        G.add_nodes_from(range(initial_nodes))
        for u in range(initial_nodes):
            for v in range(initial_nodes):
                if u != v:
                    G.add_edge(u, v, weight=(1 if edge_weights else None))
        # Iteratively add new nodes with preferential attachment
        for t in range(initial_nodes, num_nodes):
            G.add_node(t)
            # Choose targets for the new node t based on degree probabilities
            targets = set()
            degrees = dict(G.degree())  # total degree for each node (in+out for directed)
            total_degree = sum(degrees.values())
            # Preferentially select 'edges_per_step' target nodes
            while len(targets) < edges_per_step:
                r = random.uniform(0, total_degree)
                cum = 0
                for node, deg in degrees.items():
                    cum += deg
                    if cum >= r:
                        if node != t:
                            targets.add(node)
                        break
            # Add directed edges from new node t to each chosen target
            for target in targets:
                if edge_weights:
                    G.add_edge(t, target, weight=1)
                else:
                    G.add_edge(t, target)
            print(f"Step {t - initial_nodes + 1}: added node {t} with {len(targets)} edge(s) (preferential attachment)")
    else:
        # Static: use NetworkX Barabási–Albert generator, then convert to directed graph
        BA = nx.barabasi_albert_graph(num_nodes, edges_per_step)
        G.add_nodes_from(BA.nodes())
        for u, v in BA.edges():
            # For simplicity, add both directions for each undirected edge
            G.add_edge(u, v, weight=(random.random() if edge_weights else None))
            G.add_edge(v, u, weight=(random.random() if edge_weights else None))
        print(f"Generated preferential attachment graph with {num_nodes} nodes (m={edges_per_step})")
    return G

def generate_homophily_graph(num_nodes, dynamic, time_steps, homophily_groups=2, p_in=0.1, p_out=0.01, edge_weights=False):
    """Generate a directed graph using homophily (assortative linking by group)."""
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))
    # Assign each node to a group (e.g., 0,1,... homophily_groups-1)
    groups = {i: i % homophily_groups for i in range(num_nodes)}
    nx.set_node_attributes(G, groups, "group")
    if dynamic:
        # Dynamic: attempt connections at each time step
        for t in range(1, time_steps+1):
            edges_added = 0
            for i in range(num_nodes):
                j = random.randrange(num_nodes)
                if j == i:
                    continue
                # Determine probability based on group similarity
                if groups[i] == groups[j]:
                    if random.random() < p_in:
                        if G.has_edge(i, j):
                            if edge_weights:
                                G[i][j]['weight'] += 1
                        else:
                            G.add_edge(i, j, weight=(1 if edge_weights else None))
                            edges_added += 1
                else:
                    if random.random() < p_out:
                        if G.has_edge(i, j):
                            if edge_weights:
                                G[i][j]['weight'] += 1
                        else:
                            G.add_edge(i, j, weight=(1 if edge_weights else None))
                            edges_added += 1
            print(f"Step {t}: added {edges_added} homophily-based edges")
    else:
        # Static: go through all pairs once with probabilities
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i == j: 
                    continue
                if groups[i] == groups[j]:
                    if random.random() < p_in:
                        G.add_edge(i, j, weight=(random.random() if edge_weights else None))
                else:
                    if random.random() < p_out:
                        G.add_edge(i, j, weight=(random.random() if edge_weights else None))
        print(f"Generated homophily graph with {homophily_groups} groups (p_in={p_in}, p_out={p_out})")
    return G

def main(config):
    # Parse configuration parameters
    num_nodes = config.get("num_agents", 100)
    strategy = config.get("linking_strategy", config.get("strategy", "random"))
    time_steps = config.get("time_steps", 1)
    dynamic = config.get("dynamic", False)
    edge_weights = config.get("edge_weights", False)
    output_format = config.get("output_format", "graphml").lower()
    # Generate graph based on strategy
    if strategy == "random":
        p = config.get("p", 0.1)
        G = generate_random_graph(num_nodes, dynamic, time_steps, p, edge_weights)
    elif strategy in ("preferential_attachment", "preferential"):
        m = config.get("edges_per_step", 1)
        G = generate_preferential_attachment_graph(num_nodes, dynamic, time_steps, m, edge_weights)
    elif strategy == "homophily":
        groups = config.get("homophily_groups", 2)
        p_in = config.get("p_in", 0.1)
        p_out = config.get("p_out", 0.01)
        G = generate_homophily_graph(num_nodes, dynamic, time_steps, groups, p_in, p_out, edge_weights)
    else:
        raise ValueError(f"Unknown linking_strategy: {strategy}")
    # Save the final network to the desired format
    outfile = f"network.{output_format}"
    if output_format == "graphml":
        nx.write_graphml(G, outfile)
    elif output_format == "gexf":
        nx.write_gexf(G, outfile)
    elif output_format == "png":
        plt.figure(figsize=(6,6))
        nx.draw_networkx(G, node_size=30, with_labels=False)
        plt.savefig(outfile)
    else:
        nx.write_graphml(G, "network.graphml")
        outfile = "network.graphml"
    print(f"Network saved to {outfile}")
    print(f"Final network has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    if edge_weights:
        print("Edge weights have been included in the graph attributes.")

# Entry point: load config and run
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_network.py <config.json>")
        sys.exit(1)
    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)
    main(config)