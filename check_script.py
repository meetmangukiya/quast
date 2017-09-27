#!/usr/bin/env python3
"""
Performs various checks on the code, etc.
"""

import ast
import csv
import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))


def get_endpoint_nodes():
    """
    Parses app.py file and retrieves all the function that are app views or
    endpoints.
    """
    with open(os.path.join(abs_path, 'quast/app.py')) as f:
        mod = ast.parse(f.read())

    endpoints = []

    for node in mod.body:
        if isinstance(node, ast.FunctionDef):
            # retrieve all decorators that are function calls
            decors = [f for f in node.decorator_list if isinstance(f, ast.Call)]
            for function in decors:
                if function.func.value.id == 'app' and function.func.attr == 'route':
                    endpoints.append(node)
    return endpoints

def check_docs():
    okay_flag = True
    with open(os.path.join(abs_path, 'docs/api.csv')) as csvfile:
        reader = csv.reader(csvfile)
        documented_endpoints = []
        for end, description in reader:
            documented_endpoints.append(end)

    nodes = get_endpoint_nodes()
    for node in nodes:
        (endpoint, ) = tuple(filter(lambda x: (isinstance(x, ast.Call) and
                                               x.func.value.id == 'app' and
                                               x.func.attr == 'route'),
                                    node.decorator_list))
        if endpoint not in documented_endpoints:
            print("Endpoint not documented: {}".format(endpoint.args[0].s))
            okay_flag = False
    return okay_flag

if __name__ == '__main__':
    if not check_docs():
        sys.exit(-1)
