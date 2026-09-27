import networkx as nx
import matplotlib.pyplot as plt


def draw_robdd(root, var_order, out_file="robdd.png"):
    nodes = root.dfs()
    rank = {n.id: (len(var_order) if n.left is None else var_order.index(n.literal))
            for n in nodes}

    by_rank = {}
    for n in nodes:
        by_rank.setdefault(rank[n.id], []).append(n)

    pos, labels, var_nodes, term_nodes = {}, {}, [], []
    G = nx.DiGraph()
    for r, ns in by_rank.items():
        w = len(ns)
        for i, n in enumerate(ns):
            pos[n.id] = (i - (w - 1) / 2, -r)
            G.add_node(n.id)
            labels[n.id] = n.literal
            if n.left is None:
                term_nodes.append(n.id)
            else:
                var_nodes.append(n.id)
                G.add_edge(n.id, n.left.id, kind="low")
                G.add_edge(n.id, n.right.id, kind="high")

    low_edges  = [(u, v) for u, v, d in G.edges(data=True) if d["kind"] == "low"]
    high_edges = [(u, v) for u, v, d in G.edges(data=True) if d["kind"] == "high"]

    plt.figure(figsize=(1.6 * max(len(v) for v in by_rank.values()) + 2,
                         1.4 * len(by_rank) + 1))
    nx.draw_networkx_nodes(G, pos, nodelist=var_nodes, node_shape="o",
                            node_color="white", edgecolors="black", node_size=900)
    nx.draw_networkx_nodes(G, pos, nodelist=term_nodes, node_shape="s",
                            node_color="white", edgecolors="black", node_size=900)
    nx.draw_networkx_labels(G, pos, labels)
    nx.draw_networkx_edges(G, pos, edgelist=low_edges,  style="dashed",
                            connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G, pos, edgelist=high_edges, style="solid",
                            connectionstyle="arc3,rad=0.1")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight")
    print(f"ROBDD written to {out_file}")