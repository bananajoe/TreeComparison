#Creating test instances and associated functionalities

from extended_node import ExtendedNode
import catalan_numbers
import random
import json
import os

def random_full_binary_tree(n):
    if n == 1:
        return ExtendedNode(n)
    else:
        catalan = catalan_numbers.load_catalan_numbers_until(n)
        lower = 0
        r = random.random()
        for i in range(1,n):
            p = (catalan[i-1] / float(catalan[n-1]) * catalan[n-i-1])
            upper = lower + p
            if lower <= r and r < upper:
                break
            lower = upper
        return ExtendedNode(n, [random_full_binary_tree(i), random_full_binary_tree(n-i)])

def random_full_binary_tree_stack(n):
    root = ExtendedNode(n)
    stack = [root]
    pstack = []
    while len(stack) > 0:
        node = stack.pop()
        pstack.append(node)
        n = node.get_label(node)
        if n > 1:
            catalan = catalan_numbers.load_catalan_numbers_until(n)
            lower = 0
            r = random.random()
            for i in range(1,n):
                p = (catalan[i-1] * catalan[n-i-1]) / float(catalan[n-1])
                upper = lower + p
                if lower <= r and r < upper:
                    break
                lower = upper
            left = ExtendedNode(i)
            node.addkid(left)
            stack.append(left)
            right = ExtendedNode(n-i)
            node.addkid(right)
            stack.append(right)

    return root

def create_random_binary_trees(tree_size, number_of_trees):
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'

    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
    else:
        tree_list = []

    current_list_length = len(tree_list)
    safety_net = 0
    while current_list_length < number_of_trees and safety_net < 10 * number_of_trees:
        new_tree_one_list = random_full_binary_tree_stack(tree_size)
        new_tree_one_list.label_leaves_randomly()
        new_tree_one_list = new_tree_one_list.get_tree_list(new_tree_one_list)
        new_tree_two_list = random_full_binary_tree_stack(tree_size)
        new_tree_two_list.label_leaves_randomly()
        new_tree_two_list = new_tree_two_list.get_tree_list(new_tree_two_list)
        append = 0
        if new_tree_one_list.__str__() != new_tree_two_list.__str__():
            append = 1
            new_tree_list = {"one": new_tree_one_list,"two": new_tree_two_list}
            for tree in tree_list:
                if new_tree_list.__str__() == tree.__str__():
                    append = 0
                    break

        if append == 1:
            tree_list.append(new_tree_list)
            current_list_length = current_list_length + 1
        safety_net = safety_net + 1

    with open(file_name, 'w') as outfile:
        json.dump(tree_list, outfile)

def create_binary_tree_from_list(list):
    if len(list) == 1:
        return ExtendedNode(list[0])
    elif len(list) == 2:
        node = ExtendedNode(0, [create_binary_tree_from_list(list[0]), create_binary_tree_from_list(list[1])])
        node.fix_tree_list()
        return node

def adapt_tree_one(tree_one, tree_two):
    stack = list()
    one_copy = deepcopy(tree_one)
    stack.append((one_copy, tree_two))
    while len(stack) > 0:
        n1, n2 = stack.pop()
        c1 = n1.get_children(n1)
        c2 = n2.get_children(n2)
        cc = [[0 for _ in range(2)] for _ in range(2)]
        cc[0][0] = c1[0].number_of_leaves()
        cc[0][1] = c1[1].number_of_leaves()
        cc[1][0] = c2[0].number_of_leaves()
        cc[1][1] = c2[1].number_of_leaves()
        if (cc[0][0] - cc[0][1]) * (cc[1][0] - cc[1][1]) < 0:
            n1.children = list()
            n1.addkid(c1[1])
            n1.addkid(c1[0])
        nc1 = n1.get_children(n1)
        for x in range(2):
            if nc1[x].number_of_leaves() > 1 and c2[x].number_of_leaves() > 1:
                stack.append((nc1[x], c2[x]))
    one_copy.fix_complete_tree_list()
    return one_copy
    