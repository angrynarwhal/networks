package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"time"
)

// Config holds all simulation parameters from config.json.
type Config struct {
	NumAgents       int     `json:"num_agents"`
	LinkingStrategy string  `json:"linking_strategy"` // “random”, “preferential_attachment”, and “homophily”
	TimeSteps       int     `json:"time_steps"`
	Dynamic         bool    `json:"dynamic"`
	EdgeWeights     bool    `json:"edge_weights"`
	OutputFormat    string  `json:"output_format"`
	P               float64 `json:"p"`                // Used for random linking.
	EdgesPerStep    int     `json:"edges_per_step"`   // Used for preferential attachment.
	HomophilyGroups int     `json:"homophily_groups"` // Number of groups for homophily.
	PIn             float64 `json:"p_in"`             // Probability to link if same group.
	POut            float64 `json:"p_out"`            // Probability to link if different groups.
}

// Edge represents a directed edge in the network.
type Edge struct {
	Source int `json:"source"`
	Target int `json:"target"`
	Weight int `json:"weight"`
}

// Graph represents the network: nodes, edges, and (optionally) node groups.
type Graph struct {
	NumAgents int              `json:"num_agents"`
	Edges     map[string]*Edge `json:"edges"`
	Groups    map[int]int      `json:"groups,omitempty"` // Optional: group membership for homophily.
}

// randomSimulation generates a network using a random linking strategy.
func randomSimulation(numAgents, timeSteps int, p float64, edgeWeights bool) *Graph {
	G := &Graph{
		NumAgents: numAgents,
		Edges:     make(map[string]*Edge),
	}
	for t := 0; t < timeSteps; t++ {
		edgesAdded := 0
		for i := 0; i < numAgents; i++ {
			if rand.Float64() < p {
				j := rand.Intn(numAgents)
				if i == j {
					continue // avoid self-loops
				}
				key := fmt.Sprintf("%d_%d", i, j)
				if edge, exists := G.Edges[key]; exists {
					if edgeWeights {
						edge.Weight++
					}
				} else {
					weight := 0
					if edgeWeights {
						weight = 1
					}
					G.Edges[key] = &Edge{
						Source: i,
						Target: j,
						Weight: weight,
					}
					edgesAdded++
				}
			}
		}
		fmt.Printf("Random Strategy - Time step %d: %d edges added\n", t+1, edgesAdded)
	}
	return G
}

// preferentialAttachmentSimulation generates a network using a simple preferential attachment process.
func preferentialAttachmentSimulation(numAgents, timeSteps, edgesPerStep int, edgeWeights bool) *Graph {
	G := &Graph{
		NumAgents: numAgents,
		Edges:     make(map[string]*Edge),
	}
	// We'll start with an initial network of (edgesPerStep+1) nodes.
	initialNodes := edgesPerStep + 1
	degree := make([]int, numAgents)
	// Initially, no edges exist. In a more refined implementation, you might initialize with a complete graph.
	for newNode := initialNodes; newNode < numAgents; newNode++ {
		totalDegree := 0
		for i := 0; i < newNode; i++ {
			totalDegree += degree[i]
		}
		if totalDegree == 0 {
			totalDegree = newNode
		}
		targets := make(map[int]bool)
		for len(targets) < edgesPerStep {
			r := rand.Intn(totalDegree)
			cum := 0
			for i := 0; i < newNode; i++ {
				cum += degree[i]
				if cum >= r {
					targets[i] = true
					break
				}
			}
		}
		for target := range targets {
			key := fmt.Sprintf("%d_%d", newNode, target)
			weight := 0
			if edgeWeights {
				weight = 1
			}
			G.Edges[key] = &Edge{
				Source: newNode,
				Target: target,
				Weight: weight,
			}
			degree[target]++  // Increase target degree.
			degree[newNode]++ // Increase new node degree.
		}
		fmt.Printf("Preferential Attachment - Added node %d with %d edges\n", newNode, len(targets))
	}
	return G
}

// homophilySimulation generates a network based on homophily.
// Each node is assigned to one of 'homophilyGroups' and edge creation probability depends on group similarity.
func homophilySimulation(numAgents, timeSteps, homophilyGroups int, pIn, pOut float64, edgeWeights bool) *Graph {
	G := &Graph{
		NumAgents: numAgents,
		Edges:     make(map[string]*Edge),
		Groups:    make(map[int]int),
	}
	// Assign each node to a group (using modulo to distribute evenly).
	for i := 0; i < numAgents; i++ {
		G.Groups[i] = i % homophilyGroups
	}
	for t := 0; t < timeSteps; t++ {
		edgesAdded := 0
		for i := 0; i < numAgents; i++ {
			j := rand.Intn(numAgents)
			if i == j {
				continue
			}
			key := fmt.Sprintf("%d_%d", i, j)
			// Use pIn if nodes are in the same group; otherwise use pOut.
			var prob float64
			if G.Groups[i] == G.Groups[j] {
				prob = pIn
			} else {
				prob = pOut
			}
			if rand.Float64() < prob {
				if edge, exists := G.Edges[key]; exists {
					if edgeWeights {
						edge.Weight++
					}
				} else {
					weight := 0
					if edgeWeights {
						weight = 1
					}
					G.Edges[key] = &Edge{
						Source: i,
						Target: j,
						Weight: weight,
					}
					edgesAdded++
				}
			}
		}
		fmt.Printf("Homophily Strategy - Time step %d: %d edges added\n", t+1, edgesAdded)
	}
	return G
}

// loadConfig reads the configuration from a JSON file.
func loadConfig(configPath string) (*Config, error) {
	file, err := os.Open(configPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	bytes, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}
	var config Config
	if err = json.Unmarshal(bytes, &config); err != nil {
		return nil, err
	}
	// Set defaults for unspecified parameters.
	if config.NumAgents == 0 {
		config.NumAgents = 100
	}
	if config.TimeSteps == 0 {
		config.TimeSteps = 10
	}
	if config.P == 0 {
		config.P = 0.05
	}
	if config.EdgesPerStep == 0 {
		config.EdgesPerStep = 1
	}
	if config.HomophilyGroups == 0 {
		config.HomophilyGroups = 2
	}
	if config.PIn == 0 {
		config.PIn = 0.1
	}
	if config.POut == 0 {
		config.POut = 0.01
	}
	return &config, nil
}

func main() {
	rand.Seed(time.Now().UnixNano())

	config, err := loadConfig("config.json")
	if err != nil {
		fmt.Println("Error loading config:", err)
		os.Exit(1)
	}

	fmt.Printf("Running simulation with the following parameters:\n")
	fmt.Printf("Agents: %d, Time Steps: %d, Dynamic: %t, Edge Weights: %t\n",
		config.NumAgents, config.TimeSteps, config.Dynamic, config.EdgeWeights)
	fmt.Printf("Linking Strategy: %s\n", config.LinkingStrategy)

	var graph *Graph
	switch config.LinkingStrategy {
	case "random":
		graph = randomSimulation(config.NumAgents, config.TimeSteps, config.P, config.EdgeWeights)
	case "preferential_attachment":
		graph = preferentialAttachmentSimulation(config.NumAgents, config.TimeSteps, config.EdgesPerStep, config.EdgeWeights)
	case "homophily":
		graph = homophilySimulation(config.NumAgents, config.TimeSteps, config.HomophilyGroups, config.PIn, config.POut, config.EdgeWeights)
	default:
		fmt.Printf("Unknown linking strategy '%s'. Using random strategy as default.\n", config.LinkingStrategy)
		graph = randomSimulation(config.NumAgents, config.TimeSteps, config.P, config.EdgeWeights)
	}

	fmt.Printf("Simulation complete. Network has %d nodes and %d edges.\n", graph.NumAgents, len(graph.Edges))

	// Save the final network to network.json.
	edgesList := make([]Edge, 0, len(graph.Edges))
	for _, edge := range graph.Edges {
		edgesList = append(edgesList, *edge)
	}
	output := struct {
		NumAgents int         `json:"num_agents"`
		Edges     []Edge      `json:"edges"`
		Groups    map[int]int `json:"groups,omitempty"`
	}{
		NumAgents: graph.NumAgents,
		Edges:     edgesList,
		Groups:    graph.Groups,
	}
	outputBytes, err := json.MarshalIndent(output, "", "  ")
	if err != nil {
		fmt.Println("Error marshalling final graph:", err)
		os.Exit(1)
	}
	err = ioutil.WriteFile("network.json", outputBytes, 0644)
	if err != nil {
		fmt.Println("Error writing network.json:", err)
		os.Exit(1)
	}
	fmt.Println("Final network saved to network.json")
}
