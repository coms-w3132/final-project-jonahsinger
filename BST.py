"""
Binary search tree class for use in the median regression algorithm
In the average case the BST has O(logn) for each insertion and there are
n insertions. The median method with inorder traversal is O(n) so the total average
case run time complexity is O(nlogn) however the worst case is O(n^2)
if all the values are increasing or decreasing when building the BST
then the insertions will each be O(n) and the total runtime will be O(n^2).
Using a binary tree however is still better than using some other naive algorithms
that are always O(n^2).
"""


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def insert(self, node, key):
        """Inserts a key into the BST."""
        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        return node

    def inorder_traversal(self, node, array):
        """Performs an in-order traversal of the BST and stores the result in array."""
        self.inorder_traversal(node.left, array)
        array.append(node.key)
        self.inorder_traversal(node.right, array)

    def find_median(self, root):
        """Finds the median of the BST by in-order traversal."""
        elements = []
        self.inorder_traversal(root, elements)
        n = len(elements)
        if n == 0:
            return None
        if n % 2 == 1:
            return elements[n // 2]
        else:
            return (elements[n // 2 - 1] + elements[n // 2]) / 2.0
