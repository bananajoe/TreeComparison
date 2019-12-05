from __future__ import absolute_import
from six.moves import range
from zss.simple_tree import Node
import random

class ExtendedNode(Node):
    def get_list(self):
        tree_list = []
        if len(self.get_children(self)) > 0:
            for c in self.get_children(self):
                tree_list.append(c.get_list())
            return tree_list
        return [self.label]

    def get_extended_list(self):
        extended_list = []
        if len(self.get_children(self)) > 0:
            for c in self.get_children(self):
                extended_list.append(c.get_extended_list())
            return {'l': self.label, 'sub': extended_list}
        return {'l': self.label}

    def number_of_leaves(self):
        return len(self.list_of_leaves())

    def list_of_leaves(self):
        leaf_list = []
        if len(self.get_children(self)) > 0:
            for c in self.get_children(self):
                for l in c.list_of_leaves():
                    leaf_list.append(l)
            return leaf_list
        return [self]

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