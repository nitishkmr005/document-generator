// frontend/src/lib/mindmap/treeToFlow.ts

import { Node, Edge } from "@xyflow/react";
import { MindMapNode } from "@/lib/types/mindmap";

export interface FlowData {
  nodes: Node[];
  edges: Edge[];
}

const HORIZONTAL_SPACING = 280;
const VERTICAL_SPACING = 80;

// Calculate the height of a subtree (number of leaf nodes)
function getSubtreeHeight(node: MindMapNode): number {
  if (!node.children || node.children.length === 0) {
    return 1;
  }
  return node.children.reduce((sum, child) => sum + getSubtreeHeight(child), 0);
}

// Get color based on depth level (app theme: cyan/violet gradient)
export function getNodeColor(depth: number): { bg: string; border: string } {
  const colors = [
    { bg: "rgb(6, 182, 212)", border: "rgb(8, 145, 178)" },      // cyan-500/600 (root)
    { bg: "rgb(20, 184, 166)", border: "rgb(13, 148, 136)" },    // teal-500/600
    { bg: "rgb(34, 197, 94)", border: "rgb(22, 163, 74)" },      // green-500/600
    { bg: "rgb(132, 204, 22)", border: "rgb(101, 163, 13)" },    // lime-500/600
    { bg: "rgb(139, 92, 246)", border: "rgb(124, 58, 237)" },    // violet-500/600
  ];
  return colors[Math.min(depth, colors.length - 1)];
}

export function treeToFlow(
  root: MindMapNode,
  expandedNodes: Set<string> = new Set()
): FlowData {
  const nodes: Node[] = [];
  const edges: Edge[] = [];

  function traverse(
    node: MindMapNode,
    x: number,
    y: number,
    depth: number,
    parentId: string | null
  ): number {
    const nodeId = node.id;
    const isExpanded = expandedNodes.size === 0 || expandedNodes.has(nodeId);
    const hasChildren = node.children && node.children.length > 0;
    const colors = getNodeColor(depth);

    nodes.push({
      id: nodeId,
      type: "mindMapNode",
      position: { x, y },
      data: {
        label: node.label,
        depth,
        hasChildren,
        isExpanded,
        childCount: node.children?.length || 0,
        colors,
      },
    });

    if (parentId) {
      edges.push({
        id: `${parentId}-${nodeId}`,
        source: parentId,
        target: nodeId,
        type: "smoothstep",
        style: { stroke: "rgb(100, 116, 139)", strokeWidth: 2 },
        animated: false,
      });
    }

    // If collapsed or no children, return height of 1
    if (!isExpanded || !hasChildren) {
      return VERTICAL_SPACING;
    }

    // Process children
    const totalHeight = node.children!.reduce((acc, child) => {
      return acc + getSubtreeHeight(child) * VERTICAL_SPACING;
    }, 0);

    // Center children vertically around parent
    let childY = y - totalHeight / 2 + VERTICAL_SPACING / 2;

    for (const child of node.children!) {
      const childHeight = getSubtreeHeight(child) * VERTICAL_SPACING;
      const childCenterY = childY + childHeight / 2 - VERTICAL_SPACING / 2;

      traverse(child, x + HORIZONTAL_SPACING, childCenterY, depth + 1, nodeId);
      childY += childHeight;
    }

    return totalHeight;
  }

  traverse(root, 0, 0, 0, null);

  return { nodes, edges };
}

// Get all node IDs in a tree
export function getAllNodeIds(node: MindMapNode): string[] {
  const ids = [node.id];
  if (node.children) {
    for (const child of node.children) {
      ids.push(...getAllNodeIds(child));
    }
  }
  return ids;
}
