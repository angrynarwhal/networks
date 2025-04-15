package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os/exec"
)

// Edge represents a directed edge in the network.
type Edge struct {
	Source int `json:"source"`
	Target int `json:"target"`
	Weight int `json:"weight"`
}

// Network represents the entire network.
type Network struct {
	NumAgents int    `json:"num_agents"`
	Edges     []Edge `json:"edges"`
}

func main() {
	// Read the network.json file
	data, err := ioutil.ReadFile("network.json")
	if err != nil {
		log.Fatalf("Error reading network.json: %v", err)
	}

	// Unmarshal JSON data into our Network struct
	var net Network
	err = json.Unmarshal(data, &net)
	if err != nil {
		log.Fatalf("Error parsing JSON: %v", err)
	}

	// Build the DOT file content for a directed graph.
	// This will include all nodes and each directed edge (with weights if applicable).
	dot := "digraph G {\n"
	// Create all nodes so that isolated nodes (without any edge) are also drawn.
	for i := 0; i < net.NumAgents; i++ {
		dot += fmt.Sprintf("  %d;\n", i)
	}
	// Add the edges.
	for _, edge := range net.Edges {
		if edge.Weight > 0 {
			dot += fmt.Sprintf("  %d -> %d [label=\"%d\"];\n", edge.Source, edge.Target, edge.Weight)
		} else {
			dot += fmt.Sprintf("  %d -> %d;\n", edge.Source, edge.Target)
		}
	}
	dot += "}\n"

	// Write the DOT content to a file.
	dotFile := "network.dot"
	err = ioutil.WriteFile(dotFile, []byte(dot), 0644)
	if err != nil {
		log.Fatalf("Error writing %s: %v", dotFile, err)
	}
	fmt.Printf("DOT file '%s' created.\n", dotFile)

	// Use Graphviz's dot tool to generate a PNG image from the DOT file.
	// Make sure Graphviz is installed and 'dot' is in the system's PATH.
	outImage := "network.png"
	cmd := exec.Command("dot", "-Tpng", dotFile, "-o", outImage)
	err = cmd.Run()
	if err != nil {
		log.Fatalf("Error running dot command: %v", err)
	}
	fmt.Printf("Network visualization created: %s\n", outImage)
}