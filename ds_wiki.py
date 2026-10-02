"""
Data Structures Wiki - Final Laboratory Exercise
Modules: Array, LinkedList, Stack, Queue, Trees, Binary Trees
Each module explains: Definition, How it works, Insertion, Deletion, Search
(plus complexity and sample code).
"""

import textwrap

WIDTH = 78

TOPICS = {
    "Array": {
        "Definition": """
An array is a collection of elements stored in CONTIGUOUS memory locations.
Every element is identified by an index, and (in most languages) all elements
share the same type. In Python, the built-in list behaves like a dynamic array.
""",
        "How it works": """
Because elements sit side by side in memory, the computer can compute the
address of any element directly:

    address(i) = base_address + i * element_size

This is why reading or writing arr[i] takes constant time, O(1).
The trade-off: the size is fixed (or must be resized by copying), and moving
elements around is costly.

    Index:   0    1    2    3    4
           [ 10 | 20 | 30 | 40 | 50 ]
""",
        "Insertion": """
1. At the END (append): place the value in the next free slot -> O(1).
2. At a POSITION i (middle/front):
   a. Shift every element from index i onward one step to the right.
   b. Put the new value at index i.
   -> O(n) because of the shifting.

Example: insert 25 at index 2 in [10, 20, 30, 40]
   shift 40 and 30 right -> [10, 20, _, 30, 40]
   place 25              -> [10, 20, 25, 30, 40]
""",
        "Deletion": """
1. Find the index i of the element to remove.
2. Shift every element after i one step to the left to close the gap.
3. Reduce the logical size by 1.
-> O(n) in general, O(1) when removing the last element.

Example: delete index 1 from [10, 20, 25, 30, 40]
   shift left -> [10, 25, 30, 40]
""",
        "Search": """
LINEAR SEARCH: check each element from the start until the target is found
or the end is reached -> O(n). Works on any array.

BINARY SEARCH (array must be SORTED):
   1. Look at the middle element.
   2. If it equals the target, done.
   3. If target is smaller, repeat on the left half; otherwise on the right half.
   -> O(log n)

Access by index (arr[i]) is O(1).
""",
        "Complexity": """
Access by index : O(1)
Search (linear) : O(n)     Search (binary, sorted): O(log n)
Insert at end   : O(1)*    Insert at front/middle  : O(n)
Delete at end   : O(1)     Delete at front/middle  : O(n)
(* amortized for dynamic arrays)
""",
        "Sample code": '''
arr = [10, 20, 30, 40]

arr.append(50)          # insert at end
arr.insert(2, 25)       # insert 25 at index 2
arr.pop(1)              # delete element at index 1
arr.remove(40)          # delete first occurrence of value 40

print(30 in arr)        # linear search -> True
print(arr.index(30))    # position of 30
''',
    },

    "LinkedList": {
        "Definition": """
A linked list is a linear collection of NODES. Each node stores a value and a
reference (pointer) to the next node. Unlike arrays, nodes can be scattered
anywhere in memory; the links keep them connected.
Variants: singly linked, doubly linked (prev + next), circular.
""",
        "How it works": """
The list keeps a reference to the first node, called HEAD. To reach any node
you start at the head and follow the 'next' links until you arrive.
The last node points to None (null).

    HEAD
     |
    [10 | * ]-->[20 | * ]-->[30 | * ]-->None

There is no index arithmetic, so access by position is O(n), but inserting and
deleting only requires re-wiring pointers (no shifting of elements).
""",
        "Insertion": """
At the HEAD:
   1. Create a new node.
   2. new.next = head
   3. head = new                                  -> O(1)

At the TAIL:
   1. Walk to the last node (O(n), or O(1) with a tail pointer).
   2. last.next = new node

After a given node 'prev':
   1. new.next = prev.next
   2. prev.next = new                             -> O(1) once prev is known

Order of steps matters: link the new node FIRST, then redirect prev,
otherwise the rest of the list is lost.
""",
        "Deletion": """
Delete the HEAD:
   head = head.next                               -> O(1)

Delete a node with a given value:
   1. Walk the list while remembering the previous node (prev).
   2. When current.value == target:  prev.next = current.next
   3. The skipped node is no longer referenced and gets garbage collected.
   -> O(n) to find, O(1) to unlink

Example: remove 20 from 10 -> 20 -> 30
   10.next now points to 30:   10 -> 30
""",
        "Search": """
Sequential search only:
   1. Start at head.
   2. Compare current.value with the target.
   3. If equal -> found; else move to current.next.
   4. Reaching None means the value is not in the list.
-> O(n). Binary search is NOT practical because there is no random access.
""",
        "Complexity": """
Access by position : O(n)
Search             : O(n)
Insert at head     : O(1)     Insert at tail : O(n) (O(1) with tail pointer)
Delete at head     : O(1)     Delete by value: O(n)
""",
        "Sample code": '''
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_front(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def insert_end(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def delete(self, data):
        cur, prev = self.head, None
        while cur and cur.data != data:
            prev, cur = cur, cur.next
        if not cur:
            return False              # not found
        if prev:
            prev.next = cur.next
        else:
            self.head = cur.next      # deleting the head
        return True

    def search(self, data):
        cur = self.head
        while cur:
            if cur.data == data:
                return True
            cur = cur.next
        return False
''',
    },

    "Stack": {
        "Definition": """
A stack is a linear data structure that follows LIFO: Last In, First Out.
The most recently added element is the first one removed - like a stack of
plates where you only touch the top plate.
""",
        "How it works": """
All activity happens at one end, called the TOP.
Core operations:
   push(x)  - add x on top
   pop()    - remove and return the top element
   peek()   - look at the top without removing it
   is_empty() / size()

        |  30  | <- top
        |  20  |
        |  10  |
        +------+

Common uses: undo/redo, browser back button, function call stack,
expression evaluation, balancing parentheses, backtracking.
""",
        "Insertion": """
PUSH:
   1. Check for overflow (only if the stack has a fixed capacity).
   2. Place the new element on top.
   3. Increase top by 1.
-> O(1)

push(40) on [10, 20, 30]  ->  [10, 20, 30, 40]
""",
        "Deletion": """
POP:
   1. Check for underflow (stack is empty -> error).
   2. Take the element at top.
   3. Decrease top by 1 and return the element.
-> O(1)

pop() on [10, 20, 30, 40]  ->  returns 40, stack becomes [10, 20, 30]
Only the top can be deleted; elements beneath cannot be removed directly.
""",
        "Search": """
Stacks are not designed for searching. To find a value you must pop elements
one by one (using a temporary stack to restore them), checking each one.
-> O(n)
The only O(1) lookup is PEEK, which shows the top element.
""",
        "Complexity": """
push : O(1)     pop : O(1)     peek : O(1)     search : O(n)
""",
        "Sample code": '''
stack = []

stack.append(10)       # push
stack.append(20)
stack.append(30)

print(stack[-1])       # peek -> 30
print(stack.pop())     # pop  -> 30
print(stack)           # [10, 20]

def search(stack, target):
    temp, found = [], False
    while stack:
        item = stack.pop()
        temp.append(item)
        if item == target:
            found = True
            break
    while temp:                      # restore the stack
        stack.append(temp.pop())
    return found
''',
    },

    "Queue": {
        "Definition": """
A queue is a linear data structure that follows FIFO: First In, First Out.
The element added first is the first one removed - like people waiting in
line at a cashier.
""",
        "How it works": """
Elements are added at the REAR (back) and removed from the FRONT.
Core operations:
   enqueue(x) - add x at the rear
   dequeue()  - remove and return the front element
   peek()     - view the front element
   is_empty() / size()

   front                          rear
     v                              v
   [ 10 | 20 | 30 | 40 ]  <- enqueue here
   dequeue from here

Variants: circular queue, double-ended queue (deque), priority queue.
Common uses: printer jobs, CPU scheduling, BFS traversal, request buffering.
""",
        "Insertion": """
ENQUEUE:
   1. Check if the queue is full (fixed-size implementations).
   2. Move rear forward.
   3. Store the new element at rear.
-> O(1)

enqueue(50) on [10, 20, 30]  ->  [10, 20, 30, 50]
""",
        "Deletion": """
DEQUEUE:
   1. Check if the queue is empty (underflow).
   2. Take the element at front.
   3. Move front forward and return the element.
-> O(1) with collections.deque or a linked list.
   (list.pop(0) in Python is O(n) because everything shifts.)

dequeue() on [10, 20, 30, 50] -> returns 10, queue becomes [20, 30, 50]
""",
        "Search": """
Like stacks, queues don't support direct search. Dequeue each element, compare
it with the target, and re-enqueue it so the original order is preserved
(one full rotation).
-> O(n)
""",
        "Complexity": """
enqueue : O(1)    dequeue : O(1)    peek : O(1)    search : O(n)
""",
        "Sample code": '''
from collections import deque

q = deque()

q.append(10)            # enqueue
q.append(20)
q.append(30)

print(q[0])             # peek    -> 10
print(q.popleft())      # dequeue -> 10
print(q)                # deque([20, 30])

print(20 in q)          # search  -> True
''',
    },

    "Trees": {
        "Definition": """
A tree is a NON-LINEAR, hierarchical data structure made of nodes connected by
edges, with no cycles. One node is the ROOT; every other node has exactly one
parent. A node may have any number of children (a general tree).
""",
        "How it works": """
Terminology:
   Root     - the top node (no parent)
   Parent / Child - a node and the nodes directly below it
   Leaf     - a node with no children
   Sibling  - nodes with the same parent
   Depth    - number of edges from the root to a node
   Height   - longest path from a node down to a leaf
   Subtree  - a node together with all its descendants

            A            <- root
          / | \\
         B  C  D         <- children of A
        / \\     \\
       E   F     G       <- leaves: E, F, C, G

Traversals: Pre-order, Post-order (depth-first) and Level-order (breadth-first).
Uses: file systems, organization charts, HTML/DOM, decision making.
""",
        "Insertion": """
1. Choose the PARENT node that will receive the new node
   (found by searching the tree).
2. Create the new node.
3. Add it to the parent's list of children.
-> O(n) to locate the parent, O(1) to attach.

Example: insert H under B  ->  B now has children E, F, H
""",
        "Deletion": """
Deleting a node X:
   - LEAF: simply remove it from its parent's children list.
   - NODE WITH CHILDREN, option A: delete X together with its whole subtree.
   - NODE WITH CHILDREN, option B: re-attach X's children to X's parent
     (promote them), then remove X.
The root can only be deleted by choosing a new root.
-> O(n) to find the node.
""",
        "Search": """
Because a general tree has no ordering rule, you must traverse it:

DEPTH-FIRST (DFS): visit a node, then fully explore each child before moving
to the next child (uses recursion or a stack).

BREADTH-FIRST (BFS): visit the root, then all nodes at depth 1, then depth 2,
and so on (uses a queue).

-> O(n): in the worst case every node is visited.
""",
        "Complexity": """
Search : O(n)    Insert : O(n) (find parent) + O(1)    Delete : O(n)
""",
        "Sample code": '''
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, node):            # insertion
        self.children.append(node)

def search(node, target):                 # DFS search
    if node.data == target:
        return node
    for child in node.children:
        found = search(child, target)
        if found:
            return found
    return None

def delete(parent, target):               # delete a child (and its subtree)
    for child in parent.children:
        if child.data == target:
            parent.children.remove(child)
            return True
        if delete(child, target):
            return True
    return False
''',
    },

    "Binary Trees": {
        "Definition": """
A binary tree is a tree in which every node has AT MOST TWO children, called
the left child and the right child.

A Binary SEARCH Tree (BST) is a binary tree with an ordering rule:
   left subtree values  <  node value  <  right subtree values
This rule makes searching, inserting and deleting efficient.
(The operations below describe a BST.)
""",
        "How it works": """
Each node stores: data, left pointer, right pointer.

            50
          /    \\
        30      70
       /  \\    /  \\
     20   40  60   80

Traversals:
   In-order   (Left, Root, Right) -> 20 30 40 50 60 70 80  (sorted in a BST!)
   Pre-order  (Root, Left, Right) -> 50 30 20 40 70 60 80
   Post-order (Left, Right, Root) -> 20 40 30 60 80 70 50
   Level-order (breadth-first)    -> 50 30 70 20 40 60 80

If the tree stays balanced its height is about log2(n); if values are inserted
in sorted order it degrades into a linked list (height n).
""",
        "Insertion": """
1. Start at the root.
2. If the new value < current node, go LEFT; if greater, go RIGHT.
   (Duplicates are usually ignored or placed consistently on one side.)
3. Repeat until you reach an empty spot (None).
4. Place the new node there.
-> O(log n) average, O(n) worst case

Example: insert 65 into the tree above
   50 -> right (70) -> left (60) -> right (empty)  => 65 becomes 60's right child
""",
        "Deletion": """
First search for the node, then handle 3 cases:

Case 1 - LEAF (no children): remove it.

Case 2 - ONE child: replace the node with its child.

Case 3 - TWO children:
   a. Find the in-order successor (smallest value in the right subtree)
      [or the in-order predecessor].
   b. Copy the successor's value into the node being deleted.
   c. Delete the successor from the right subtree (it has 0 or 1 child).

Example: delete 50 (root, two children)
   successor = 60 -> root becomes 60, then the old 60 node is removed.
-> O(log n) average, O(n) worst case
""",
        "Search": """
1. Start at the root.
2. If target == node value -> found.
3. If target < node value -> continue in the LEFT subtree.
4. If target > node value -> continue in the RIGHT subtree.
5. Reaching None means the value is not in the tree.
Each step discards half of the remaining nodes (when balanced).
-> O(log n) average, O(n) worst case (skewed tree)
""",
        "Complexity": """
              Average     Worst (skewed)
Search        O(log n)    O(n)
Insert        O(log n)    O(n)
Delete        O(log n)    O(n)
Traversal     O(n)        O(n)
""",
        "Sample code": '''
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insert(root.left, data)
    elif data > root.data:
        root.right = insert(root.right, data)
    return root

def search(root, data):
    if root is None or root.data == data:
        return root
    if data < root.data:
        return search(root.left, data)
    return search(root.right, data)

def min_node(node):
    while node.left:
        node = node.left
    return node

def delete(root, data):
    if root is None:
        return None
    if data < root.data:
        root.left = delete(root.left, data)
    elif data > root.data:
        root.right = delete(root.right, data)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = min_node(root.right)
        root.data = succ.data
        root.right = delete(root.right, succ.data)
    return root

def inorder(root):
    return inorder(root.left) + [root.data] + inorder(root.right) if root else []
''',
    },
}

SECTIONS = ["Definition", "How it works", "Insertion", "Deletion",
            "Search", "Complexity", "Sample code"]


# ----------------------------------------------------------------- display --
def line(char="="):
    print(char * WIDTH)


def header(title):
    print()
    line()
    print(title.center(WIDTH))
    line()


def show_section(topic, section):
    header(f"{topic.upper()}  -  {section}")
    print(TOPICS[topic][section].strip("\n"))
    print()
    input("Press Enter to continue...")


def show_all(topic):
    header(f"{topic.upper()}  -  FULL ARTICLE")
    for section in SECTIONS:
        print(f"\n--- {section} ---")
        print(TOPICS[topic][section].strip("\n"))
    print()
    input("Press Enter to continue...")


def topic_menu(topic):
    while True:
        header(f"{topic.upper()}")
        for i, section in enumerate(SECTIONS, 1):
            print(f"  [{i}] {section}")
        print("  [8] Show full article")
        print("  [0] Back to main menu")
        line("-")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            return
        if choice == "8":
            show_all(topic)
        elif choice.isdigit() and 1 <= int(choice) <= len(SECTIONS):
            show_section(topic, SECTIONS[int(choice) - 1])
        else:
            print("Invalid choice, try again.")


def search_wiki():
    term = input("Search keyword: ").strip().lower()
    if not term:
        return
    header(f"SEARCH RESULTS FOR '{term}'")
    hits = 0
    for topic, sections in TOPICS.items():
        for section, text in sections.items():
            if term in text.lower() or term in topic.lower():
                print(f"  - {topic} > {section}")
                hits += 1
    if not hits:
        print("  No matches found.")
    print()
    input("Press Enter to continue...")


def compare_table():
    header("QUICK COMPARISON")
    rows = [
        ("Structure",    "Type",       "Order rule",        "Insert",     "Delete",     "Search"),
        ("Array",        "Linear",     "Index",             "O(n)",       "O(n)",       "O(n)/O(log n)"),
        ("LinkedList",   "Linear",     "Links",             "O(1)*",      "O(1)*",      "O(n)"),
        ("Stack",        "Linear",     "LIFO",              "O(1) push",  "O(1) pop",   "O(n)"),
        ("Queue",        "Linear",     "FIFO",              "O(1) enq",   "O(1) deq",   "O(n)"),
        ("Tree",         "Hierarchy",  "Parent-child",      "O(n)",       "O(n)",       "O(n)"),
        ("Binary Tree",  "Hierarchy",  "Left < Root < Right", "O(log n)", "O(log n)",   "O(log n)"),
    ]
    for r in rows:
        print(f"{r[0]:<13}{r[1]:<11}{r[2]:<21}{r[3]:<11}{r[4]:<11}{r[5]}")
    print("\n* when the position/node is already known (e.g., at the head)")
    print("Binary Tree row assumes a balanced Binary Search Tree.\n")
    input("Press Enter to continue...")


def main():
    names = list(TOPICS.keys())
    while True:
        header("DATA STRUCTURES WIKI")
        print("Main Menu".center(WIDTH))
        line("-")
        for i, name in enumerate(names, 1):
            print(f"  [{i}] {name}")
        print(f"  [{len(names) + 1}] Search the wiki")
        print(f"  [{len(names) + 2}] Compare all structures")
        print("  [0] Exit")
        line("-")
        choice = input("Choose a module: ").strip()
        if choice == "0":
            print("\nThank you for using the Data Structures Wiki. Goodbye!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            topic_menu(names[int(choice) - 1])
        elif choice == str(len(names) + 1):
            search_wiki()
        elif choice == str(len(names) + 2):
            compare_table()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
