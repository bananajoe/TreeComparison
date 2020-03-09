from __future__ import absolute_import
from six.moves import range
from zss.simple_tree import Node
from copy import deepcopy
import random

class ExtendedNode(Node):
    def __init__(self, label, children=None):
        self.tree_list = [label]
        self = super(ExtendedNode, self).__init__(label, children)

    def addkid(self, node, before=False):
        if len(self.get_children(self)) == 0:
            tree_list = [node.tree_list]
            self.tree_list = tree_list
        else:
            self.tree_list = [self.get_tree_list(self), node.get_tree_list(node)]

        self = super(ExtendedNode, self).addkid(node, before)
        return self

    def fix_tree_list(self):
        if len(self.get_children(self)) == 0:
            self.tree_list = [self.label]
        else:
            stack = deepcopy(self.get_children(self))
            tree_list = []
            while len(stack) > 0:
                node = stack.pop()
                tree_list.insert(0, node.get_tree_list(node))
            self.tree_list = tree_list

    def fix_complete_tree_list(self):
        stack = list()
        stack.append(self)
        pstack = list()
        while len(stack) > 0:
            node = stack.pop()
            if len(node.get_children(node)) > 0:
                for c in node.get_children(node):
                    stack.append(c)
                pstack.append(node)

        while len(pstack) > 0:
            node = pstack.pop()
            node.fix_tree_list()


    @staticmethod
    def get_tree_list(node):
        return node.tree_list

    #def get_extended_list(self):
    #    extended_list = []
    #    if len(self.get_children(self)) > 0:
    #        for c in self.get_children(self):
    #            extended_list.append(c.get_extended_list())
    #        return {'l': self.label, 'sub': extended_list}
    #    return {'l': self.label}

    def number_of_leaves(self):
        return len(self.list_of_leaves())

    def list_of_leaves(self):
        leaf_list = []
        stack = list()
        stack.append(self)
        while len(stack) > 0:
            node = stack.pop()
            if len(node.get_children(node)) > 0:
                for c in node.get_children(node):
                    stack.append(c)
            else:
                leaf_list.append(node)
        return leaf_list

    def list_of_leaf_labels(self):
        leaf_labels = []
        for l in self.list_of_leaves():
            leaf_labels.append(l.label)
        return leaf_labels

    def get_clusters(self, exclude_leaf_labels = 0):
        if exclude_leaf_labels == 0:
            clusters = [self.list_of_leaf_labels()]
        else:
            clusters = []
        if len(self.get_children(self)) > 0:
            for c in self.get_children(self):
                for l in c.get_clusters():
                    if len(l) > 1:
                        clusters.append(l)
            for c in clusters:
                if len(c) > 1:
                    c.sort()
            return clusters
        return clusters

    def label_leaves_randomly(self):
        #get leaves of tree
        leaves = self.list_of_leaves()
        number_of_leaves = len(self.list_of_leaves())

        #create a shuffled list of labels for leaves
        labels = list(range(1, number_of_leaves + 1))
        r = random.SystemRandom()
        r.shuffle(labels)

        #assign labels to leaves
        for i in range(0,number_of_leaves):
            leaves[i].label = labels[i]

        stack = [self]
        pstack = [self]
        while len(stack) > 0:
            node = stack.pop()
            if len(node.get_children(node)) > 0:
                for c in node.get_children(node):
                    stack.append(c)
                    pstack.append(c)
        while len(pstack) > 0:
            node = pstack.pop()
            node.fix_tree_list()
