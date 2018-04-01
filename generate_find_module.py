#!/usr/bin/env python3

#
# Generates a find module for CMake
#


import argparse
import string
import os.path


def generate(f, template_str, args):
    template = string.Template(template_str)
    d = {}
    d["name"] = args.name
    d["include"] = args.include
    d["lib"] = args.lib
    d["target"] = args.target
    d["package"] = args.package if args.package else "NO"

    result = template.substitute(d)

    f.write(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Generates a find module for CMake")
    parser.add_argument("--name", dest = "name", help = "Library name", required = True)
    parser.add_argument("--include", dest = "include", help = "Include file to search for", required = True)
    parser.add_argument("--lib", dest = "lib", help = "Library file to search file", required = False)
    parser.add_argument("--target", dest = "target", help = "Target to create", required = False)
    parser.add_argument("--package", dest = "package", help = "pkg-config package name", required = False)
    parser.add_argument("--outdir", dest = "outdir", help = "Output directory", required = False)
    args = parser.parse_args()

    if(not args.target):
        args.target = "{}::{}".format(args.name, args.name)

    template_file = os.path.join(os.path.dirname(__file__), "generate_find_module.template")
    template_str = None
    with open(template_file, "rt") as f:
        template_str = f.read()

    filename = "Find{}.cmake".format(args.name)

    if(args.outdir):
        filename = os.path.join(args.outdir, filename)

    with open(filename, "wt") as f:
        generate(f, template_str, args)



