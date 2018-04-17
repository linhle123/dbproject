
def find_approximate_functional_dependencies(DataFileName, depth_limit, minimum_support):
    print("shit")


# -*- coding: utf-8 -*-
"""
Data Mining Programming Assignment

This script aims to discover approximate functional dependencies in a given
data set.
"""
import sys
from multiprocessing import Queue

def pprint(FDs):
    """Pretty print of discovered FDs
    """
    print('\nDiscovered FDs:')
    for fd in FDs:
        print(', '.join(fd[0]), " -> ", fd[1], ' with support ', fd[2])


def load_data(data_file_name):
    """Read data from data_file_name and return a list of lists,
    where the first list (in the larger list) is the list of attribute names,
    and the remaining lists correspond to the tuples (rows) in the file.
    """
    with open(data_file_name, 'rU') as f:
        results = [[x.rstrip() for x in line.split(',')] for line in f]
    return results



def compute_support(domain, range, input_data, domain_indices, range_index):
    # if domain == ['Color'] and range == 'Size':
    # print("domain:", domain)
    # print("range:", range)
    # print(input_data)
    mappings = {}
    # mappings[lhs][rhs] = x means that lhs -> rhs occur x times

    # indices = [position[attr] for attr in domain]
    for row in input_data:
        lhs = tuple([row[i] for i in domain_indices])
        rhs = row[range_index]
        if lhs not in mappings:
            mappings[lhs] = {} #create and entry for lhs
            mappings[lhs][rhs] = 1 #freq of lhs -> rhs is 1
        elif rhs not in mappings[lhs]: #if lhs hasn't been mapped to rhs
            mappings[lhs][rhs] = 1
        else: #lhs has been mapped to rhs
            mappings[lhs][rhs] += 1

    # print("mappings:")
    # print(mappings)

    dominant_rhs_count = 0
    for rhs in list(mappings.values()):
        dominant_rhs_count += max(list(rhs.values()))

    # print(dominant_rhs_count)
    support = dominant_rhs_count / float(len(input_data))
    # print("support:", support)
    return support

def find_approximate_functional_dependencies(data_file_name, depth_limit, minimum_support):
    """Main function which you need to implement!

    The function discovers approximate functional dependencies in a given data

    Input:
        data_file_name - name of a CSV file with data
        depth_limit - integer that limits the depth of search through the space of
            domains of functional dependencies
        minimum_support - threshold for identifying adequately approximate FDs

    Output:
        FDs - a list of tuples. Each tuple represents a discovered FD.
        The first element of each tuple is a list containing LHS of discovered FD
        The second element of the tuple is a single attribute name, which is RHS of that FD
        The third element of the tuple is support for that FD

    Output example:
        [([A],C, 0.91), ([C, F],E, 0.97), ([A,B,C],D, 0.98), ([A, G, H],F, 0.92)]
        The above list represent the following FDs:
            A -> C, with support 0.91
            C, F -> E, with support 0.97
            A, B, C -> D, with support 0.98
            A, G, H -> F, with support 0.92
    """
    # read input data:
    input_data = load_data(data_file_name)
    # print(input_data)
    # Transform input_data (list of lists) into some better representation.
    # You need to decide what that representation should be.
    # Data transformation is optional!

    # --------Your code here! Optional! ----------#

    # Discover FDs with given minimun support and depth limit:
    FDs = []

    # --------Your code here!---------------------#
    domain_frontiers = Queue()
    attributes = input_data[0]
    # print(attributes)
    for attr in attributes:
        domain_frontiers.put([attr])


    position = {}
    for index, attribute in enumerate(attributes):
        position[attribute] = index

    # print(position)
    # minimum_support = 0.8
    # depth_limit = 3

    while not domain_frontiers.empty():
        next_domain = domain_frontiers.get()
        # print("next domain:", next_domain)
        # range Y which are in attributes, but not in next_domain
        # print("here:")
        # print("attr:", attributes)
        # print("next_domain:", next_domain)
        possible_ranges = list(set(attributes) - set(next_domain))
        # print("possible_ranges", possible_ranges)
        for range in possible_ranges:
            # print(range)
            domain_indices = [position[attr] for attr in next_domain]
            range_index = position[range]
            support = compute_support(next_domain, range, input_data[1:], domain_indices, range_index)
            if support >= minimum_support:
                # print("adding", next_domain)
                # append a copy of next_domain, not a reference to it (which is by default)
                FDs.append([list(next_domain), range, support])
                # print(FDs)

        # add new frontiers
        if len(next_domain) < depth_limit:
            # position of attribute with highest position in next_domain
            highest_position = max([position[x] for x in next_domain])

            # print("highest position:", highest_position)
            # generator
            possible_attributes_to_add = (x for x in attributes if position[x] > highest_position)
            # we want new_attribute to be added to next_domain to be among these possible attributes
            # see pseudo code
            for new_attribute in possible_attributes_to_add:
                # print("new att:", new_attribute)
                # parameter is a copy of next_domain with new_attribute appended
                domain_frontiers.put(next_domain + [new_attribute])

    return FDs



# def main():
#     FDs = []
#     input_data = [['Color', 'Size', 'Shape'], ['blue', 'large', 'circle'], ['green', 'large', 'square'],
#                   ['blue', 'medium', 'triangle'], ['red','small', 'square']]
#     domain_frontiers = queue.Queue()
#     domain_frontiers.put(["Color"])
#
#     attributes = input_data[0]
#     # print(attributes)
#
#     position = {}
#     for index, attribute in enumerate(attributes):
#         position[attribute] = index
#
#     # print(position)
#     minimum_support = 0.8
#     depth_limit = 3
#
#     while not domain_frontiers.empty():
#         next_domain = domain_frontiers.get()
#         # print("next domain:", next_domain)
#         #range Y which are in attributes, but not in next_domain
#         # print("here:")
#         # print("attr:", attributes)
#         # print("next_domain:", next_domain)
#         possible_ranges = list(set(attributes) - set(next_domain))
#         # print("possible_ranges", possible_ranges)
#         for range in possible_ranges:
#             # print(range)
#             domain_indices = [position[attr] for attr in next_domain]
#             range_index = position[range]
#             support = compute_support(next_domain, range, input_data[1:], domain_indices, range_index)
#             if support >= minimum_support:
#                 # print("adding", next_domain)
#                 #append a copy of next_domain, not a reference to it (which is by default)
#                 FDs.append([next_domain.copy(), range, support])
#                 # print(FDs)
#
#         #add new frontiers
#         if len(next_domain) < depth_limit:
#             #position of attribute with highest position in next_domain
#             highest_position = max([position[x] for x in next_domain])
#
#             # print("highest position:", highest_position)
#             #generator
#             possible_attributes_to_add = (x for x in attributes if position[x] > highest_position)
#             #we want new_attribute to be added to next_domain to be among these possible attributes
#             #see pseudo code
#             for new_attribute in possible_attributes_to_add:
#                 # print("new att:", new_attribute)
#                 #parameter is a copy of next_domain with new_attribute appended
#                 domain_frontiers.put(next_domain + [new_attribute])
#     return FDs

# print("FDs:", main())


if __name__ == '__main__':
    # parse command line arguments:
    if (len(sys.argv) < 3):
        print('Wrong number of arguments. Correct example:')
        print('python find_fds.py input_data_set.csv 3 0.91')
    else:
        data_file_name = str(sys.argv[1])
        depth_limit = int(sys.argv[2])
        minimum_support = float(sys.argv[3])

        # Main function which you need to implement.
        # It discover FDs in the input data with given minimum support and depth limit
        FDs = find_approximate_functional_dependencies(data_file_name, depth_limit, minimum_support)

        # print you findings:
        pprint(FDs)
