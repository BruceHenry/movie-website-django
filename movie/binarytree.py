"""
    Binary tree (Python)

    Copyright (c) 2007 Wj. All rights reserved.

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

    original source found at:
    http://wj32.wordpress.com/2007/10/08/binary-search-tree-with-heaps-more-features/
"""

"""
    CHANGELOG:

    Version 1.1:
        * Added changelog.
        * Moved all non-modifying functions to the node class and replaced the code in binary_tree with wrappers.
        * Added a few more list functions and statistical functions.
"""

import math

class node:
    """A node in a tree. Note that all functions which do not modify anything are in this class, while modifying functions are in the binary_tree class."""

    def __init__(self, key = None, data = None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

    def follow(self, key):
        """Try to find the specified key in the tree, leaving a "trail" behind of which nodes it has visited. Used to avoid duplicate code."""
        current = self
        trail = []
        value = isinstance(key, node) and key.key or key

        while True:
            if current is None:
                break

            trail.append(current)

            if value == current.key:
                break
            elif value < current.key:
                current = current.left
            elif value > current.key:
                current = current.right
            else:
                # this isn't meant to happen
                break

        return trail

    def find(self, key):
        """Find a node in the tree."""

        value = isinstance(key, node) and key.key or key
        trail = self.follow(value)

        if trail == []:
            return

        if trail[-1].key == value:
            return trail[-1]

    def depth(self):
        """Return the how deep the tree is."""

        if not self.left is None:
            leftdepth = self.left.depth()
        else:
            leftdepth = 0

        if not self.right is None:
            rightdepth = self.right.depth()
        else:
            rightdepth = 0

        return max(leftdepth, rightdepth) + 1

    def min(self):
        """Return the smallest node in the tree."""

        node = self

        while not node.left is None:
            node = node.left

        return node

    def max(self):
        """Return the biggest node in the tree."""

        node = self

        while not node.right is None:
            node = node.right

        return node

    def dict(self):
        """Return a dictionary version of the tree"""

        d = {}

        for key in self.listkeys():
            d[key] = self[key]

        return d

    def listrecursive(self):
        """Return a list of lists of lists (and so on) where each node is represented by [left data right]. So, a simple tree might look like:
    [[None 1 [None 2 None]] 3 [None 4 None]]

The numbers in the example are actually meant to be node objects.
"""
        l = []

        if not self.left is None:
            l.append(self.left.listrecursive())
        else:
            l.append(None)

        l.append(self)

        if not self.right is None:
            l.append(self.right.listrecursive())
        else:
            l.append(None)

        return l

    def listlayer(self, node, n):
        """List a layer (used by listlayers())"""

        l = []

        if node is None:
            return None

        if n == 0:
            l.append(node.left)
        else:
            r = self.listlayer(node.left, n - 1)
            l.extend(r is None and [None, None] or r)

        if n == 0:
            l.append(node.right)
        else:
            r = self.listlayer(node.right, n - 1)
            l.extend(r is None and [None, None] or r)

        return l

    def listlayers(self):
        """Return a list of lists where each list in the list represents a different layer of the tree. An example list of this kind:
    [[3] [1 4] [None 2 None None]
In this example, 1 is the left child of 3 and 4 is the right child of 3. 2 is the right child of 1.
"""
        l = []

        l.append([self])

        for i in range(self.depth() - 1):
            l.append(self.listlayer(self, i))

        return l

    def listkeys(self):
        """Return a list of keys in the tree."""

        l = []

        if not self.left is None:
            l.extend(self.left.listkeys())

        l.append(self.key)

        if not self.right is None:
            l.extend(self.right.listkeys())

        return l

    def listdata(self):
        """Return a list of data in the tree."""

        l = []

        if not self.left is None:
            l.extend(self.left.listdata())

        l.append(self.data)

        if not self.right is None:
            l.extend(self.right.listdata())

        return l

    def listnodes(self):
        """Return a list of nodes in the tree."""

        l = []

        if not self.left is None:
            l.extend(self.left.listnodes())

        l.append(self)

        if not self.right is None:
            l.extend(self.right.listnodes())

        return l

    def formattree(self, indentsize = 2, indent = 0, side = "T"):
        """Return a string with a formatted version of all the nodes in the tree."""

        string = "%s%s:%s: %s\n" % ((indent * " "), side, repr(self.key), repr(self.data))

        if not self.left is None:
            string += self.left.formattree(indentsize, indent + indentsize, "L")

        if not self.right is None:
            string += self.right.formattree(indentsize, indent + indentsize, "R")

        return string

    def formattreemiddle(self, indentsize = 2, indent = 0):
        """Return a string with a formatted version of all the nodes in the tree."""

        string = ""

        if not self.left is None:
            string += self.left.formattreemiddle(indentsize, indent + indentsize)

        string += "%s%s: %s\n" % ((indent * " "), repr(self.key), repr(self.data))

        if not self.right is None:
            string += self.right.formattreemiddle(indentsize, indent + indentsize)

        return string

    def __getitem__(self, key):
        """Get an item from the tree. Raises KeyError if the key doesn't exist."""

        item = self.find(key)

        if not item is None:
            return item.data
        else:
            raise KeyError from key

    def __setitem__(self, key, data):
        """Set an item. RAISES KeyError IF the key doesn't exist (unlike in binary_tree)."""

        item = self.find(key)

        if item is None:
            raise KeyError from key
        else:
            item.data = data

    def __contains__(self, key):
        """Check if a key is present in the tree."""

        item = self.find(key)

        return not item is None

    def __repr__(self):
        return "%s: %s" % (repr(self.key), repr(self.data))

    def __iter__(self):
        """Generator function"""

        if not self.left is None:
            for node in self.left:
                yield node

        yield self

        if not self.right is None:
            for node in self.right:
                yield node

    def __eq__(self, other):
        """Compare this node with another node."""

        if not isinstance(other, node):
            return False

        selfkeylist = self.listkeys()
        selfdatalist = self.listdata()
        otherkeylist = other.listkeys()
        otherdatalist = other.listdata()

        return (selfkeylist == otherkeylist) and (selfdatalist == otherdatalist)

    def __ne__(self, other):
        """Compare this node with another node."""

        return not (self == other)

class binary_tree:
    """A simple binary search tree.

    Nodes can have keys of any type, as long as they can be compared with each other.

Objects can be easily added:
    tree["key"] = "value"
Or deleted:
    del tree["key"]
Or tested for membership:
    "key" in tree
"""

    def __init__(self):
        self.root = None
        self.__count = 0

    def follow(self, key):
        """Try to find the specified key in the tree, leaving a "trail" behind of which nodes it has visited. Used to avoid duplicate code."""

        if self.root is None:
            return []

        return self.root.follow(key)

    def clear(self):
        """Delete all items from the tree."""

        self.root = None
        self.__count = 0

    def find(self, key):
        """Find a node in the tree."""

        if not self.root is None:
            return self.root.find(key)
        else:
            return None

    def insert(self, key, data):
        """Insert a node into the tree. Raises KeyError if the key already exists."""

        trail = self.follow(key)

        if trail == []:
            self.root = node(key, data)
            self.__count += 1
            return

        if key == trail[-1].key:
            raise KeyError from "key %s already in tree" % key
        elif key < trail[-1].key:
            trail[-1].left = node(key, data)
            self.__count += 1
            return trail[-1].left
        elif key > trail[-1].key:
            trail[-1].right = node(key, data)
            self.__count += 1
            return trail[-1].right

    def delete(self, key):
        """Remove a node from the tree. Raises KeyError if the key doesn't exist."""

        if self.root is None:
            raise KeyError from key

        value = isinstance(key, node) and key.key or key
        trail = self.follow(value)
        object = None
        attr = ""

        if value != trail[-1].key:
            raise KeyError from key

        if len(trail) == 1:
            object = self
            attr = "root"
        elif value < trail[-2].key:
            object = trail[-2]
            attr = "left"
        elif value > trail[-2].key:
            object = trail[-2]
            attr = "right"

        if (trail[-1].left is None) and (trail[-1].right is None):
            setattr(object, attr, None)
        elif trail[-1].left is None:
            setattr(object, attr, trail[-1].right)
        elif trail[-1].right is None:
            setattr(object, attr, trail[-1].left)
        else:
            temp = trail[-1].left

            while not temp.right is None:
                temp = temp.right

            tempdata = temp.data
            tempkey = temp.key
            self.delete(temp)
            trail[-1].data = tempdata
            trail[-1].key = tempkey

        self.__count -= 1

    def depth(self):
        """Return the how deep the tree is."""

        if not self.root is None:
            return self.root.depth()
        else:
            return 0

    def min(self):
        """Return the smallest node in the tree."""

        if not self.root is None:
            return self.root.min()
        else:
            return None

    def max(self):
        """Return the biggest node in the tree."""

        if not self.root is None:
            return self.root.max()
        else:
            return None

    def optimumdepth(self):
        """Calculate the optimum depth of the tree based on how many nodes there are. The formula is:
    log2(n + 1)
"""

        return math.log(self.__count + 1, 2)

    def possibleused(self):
        """Calculate how many nodes could be used based on the depth of the tree. The formula is:
    (2 ^ depth) - 1
"""

        return (2 ** self.depth()) - 1

    def efficiency(self):
        """Calculate the efficiency of the tree (how many slots are being wasted). The formula is:
    n / possibleused
"""

        return float(self.__count) / self.possibleused()

    def dict(self):
        """Return a dictionary version of the tree."""

        if not self.root is None:
            return self.root.dict()
        else:
            return {}

    def listrecursive(self):
        """Return a list of lists of lists (and so on) where each node is represented by [left data right]. So, a simple tree might look like:
    [[None 1 [None 2 None]] 3 [None 4 None]]

The numbers in the example are actually meant to be node objects.
"""

        if not self.root is None:
            return self.root.listrecursive()
        else:
            return []

    def listlayers(self):
        """Return a list of lists where each list in the list represents a different layer of the tree. An example list of this kind:
    [[3] [1 4] [None 2 None None]
In this example, 1 is the left child of 3 and 4 is the right child of 3. 2 is the right child of 1.
"""

        if not self.root is None:
            return self.root.listlayers()
        else:
            return []

    def listkeys(self):
        """Return a list of keys in the tree. The list will be sorted (this IS a binary search tree...)."""

        if not self.root is None:
            return self.root.listkeys()
        else:
            return []

    def listdata(self):
        """Return a list of data in the tree. The list will be sorted ACCORDING TO KEY."""

        if not self.root is None:
            return self.root.listdata()
        else:
            return []

    def listnodes(self):
        """Return a list of nodes in the tree. The list will be sorted ACCORDING TO KEY."""

        if not self.root is None:
            return self.root.listnodes()
        else:
            return []

    def formattree(self, indentsize = 2):
        """Return a string with a formatted version of all the nodes in the tree."""

        if not self.root is None:
            return self.root.formattree(indentsize)
        else:
            return ""

    def formattreemiddle(self, indentsize = 2):
        """Return a string with a formatted version of all the nodes in the tree. This version has the root node in the middle."""

        if not self.root is None:
            return self.root.formattreemiddle(indentsize)
        else:
            return ""

    def __len__(self):
        """Return a count of nodes in the tree."""

        return self.__count

    def __getitem__(self, key):
        """Get an item from the tree. Raises KeyError if the key doesn't exist."""

        if not self.root is None:
            return self.root[key]
        else:
            raise KeyError from key

    def __setitem__(self, key, data):
        """Set an item. Adds one if it isn't already present."""

        item = self.find(key)

        if item is None:
            item = self.insert(key, data)
        else:
            item.data = data

    def __delitem__(self, key):
        """Delete an item from the tree."""

        self.delete(key)

    def __contains__(self, key):
        """Check if a key is present in the tree."""

        if not self.root is None:
            return key in self.root
        else:
            return False

    def __repr__(self):
        """Return a string version of the tree."""

        return "binary tree (%s nodes)" % self.__count

    def __iter__(self):
        """Generator function"""

        if not self.root is None:
            for node in self.root:
                yield node

    def __eq__(self, other):
        """Compare this tree with another tree."""

        if not isinstance(other, binary_tree):
            return False

        selfkeylist = self.listkeys()
        selfdatalist = self.listdata()
        otherkeylist = other.listkeys()
        otherdatalist = other.listdata()

        return (selfkeylist == otherkeylist) and (selfdatalist == otherdatalist)

    def __ne__(self, other):
        """Compare this tree with another tree."""

        return not (self == other)

# test program if this file is run
if __name__ == "__main__":
    import random, sys

    tree = binary_tree()
    tree["python"] = None
    tree["c"] = None
    tree["asp"] = None
    tree["ruby"] = None
    tree["java"] = None
    tree["d"] = None
    tree["lisp"] = None
    tree2 = binary_tree()
    tree2["a"] = 1
    tree3 = binary_tree()
    tree3["a"] = 1

    print("Binary Tree Test\n")
    print("Node Count: %d" % len(tree))
    print("Depth: %d" % tree.depth())
    print("Optimum Depth: %f (%d) (%f%% depth efficiency)" % (tree.optimumdepth(), math.ceil(tree.optimumdepth()),
                                                              math.ceil(tree.optimumdepth()) / tree.depth()))
    print("Min: %s" % repr(tree.min()))
    print("Max: %s" % repr(tree.max()))
    print("Efficiency: %f%% (total possible used: %d, total wasted: %d): " % (tree.efficiency() * 100,
                                                                              len(tree) / tree.efficiency(),
                                                                              (len(tree) / tree.efficiency()) - len(tree)))
    print("List of Layers:\n\t" + repr(tree.listlayers()) + "\n")
    print("\"Recursive\" List:\n\t" + repr(tree.listrecursive()) + "\n")
    print("List of Keys:\n\t" + repr(tree.listkeys()) + "\n")
    print("List of Data:\n\t" + repr(tree.listdata()) + "\n")
    print("List of Nodes:\n\t" + repr(tree.listnodes()) + "\n")
    print("Dictionary:\n\t" + repr(tree.dict()) + "\n")
    print("Formatted Tree:\n" + tree.formattree() + "\n")
    print("Formatted Tree (Root in Middle):\n" + tree.formattreemiddle() + "\n")
    print("tree2 == tree3: " + repr(tree2 == tree3))
    print("\"lisp\" in tree: " + repr("lisp" in tree))
    print("tree[\"d\"]: " + repr(tree["d"]))
    print("tree.root[\"d\"]: " + repr(tree.root["d"]))

    print("Clearing tree...")
    tree.clear()

    count = 1000000
    i = count
    choseni = 0
    chosennumber = 0

    try:
        choseni = random.randrange((count / 2) - (count / 100), (count / 2) + (count / 100))
    except:
        choseni = count / 2

    print("Adding %d random numbers to the tree..." % count)

    while i:
        i -= 1

        n = random.randrange(0, 2147483647)

        try:
            tree[n] = None

            if i == choseni:
                chosennumber = n
        except Exception:
            pass

    print("Done adding, press Enter to continue.")
    sys.stdin.readline()

    print("Finding %d" % chosennumber)
    tree.find(chosennumber)
    print("Found %d" % chosennumber)
    print("Node Count: %d" % len(tree))
    print("Depth: %d" % tree.depth())
    print("Optimum Depth: %f (%d) (%f%% depth efficiency)" % (tree.optimumdepth(), math.ceil(tree.optimumdepth()),
                                                              math.ceil(tree.optimumdepth()) / tree.depth()))
    print("Min: %s" % repr(tree.min()))
    print("Max: %s" % repr(tree.max()))
    print("Efficiency: %f%% (total possible used: %d, total wasted: %d): " % (tree.efficiency() * 100,
                                                                              tree.possibleused(),
                                                                              (tree.possibleused() - len(tree))))
    #print "Formatted Tree (Root in Middle):\n" + tree.formattreemiddle() + "\n"
    print("Removing all nodes...")

    for key in tree.listkeys():
        del tree[key]

    print("Done removing.")
