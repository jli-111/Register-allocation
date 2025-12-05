#!/usr/bin/env python3

import argparse
from pycparser import parse_file

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Parse and color functions in a C file")
    p.add_argument("input", help="Input C file")
    p.add_argument("output", help="Output file")

    args = p.parse_args()

    ast = parse_file(args.input, use_cpp=True,
                     cpp_args=["-I/usr/share/python3-pycparser/fake_libc_include/"])

    # process ast
