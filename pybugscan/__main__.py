from pybugscan import *

if __name__ == "__main__":
    import argparse
    import glob
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", help="Files to analyze (passed to glob)", required=True)
    parser.add_argument("--showall", help="Whether to show all files analyzed", action="store_true")
    parser.add_argument("--possibly_mutable", help="Whether to possibly mutable defaults", action="store_true", default=False)
    args = parser.parse_args()
    globstring = args.files

    analyzers = [
        Analyzer(vars(args))
        for Analyzer
        in BugScanner.__subclasses__()
    ]

    found_bugs = set()
    for file in glob.glob(globstring, recursive=True):
        for ana in analyzers:
            ana.visit_file(file)
            warnings = ana.get_and_clear_warnings()
            if warnings:
                print(f"{ana.bug_type} in file: {file}")
            elif args.showall:
                print(f"File: {file}")
            if warnings:
                found_bugs.add(type(ana))
                for warning in warnings:
                    print("\t\t" + warning)
                print()

    if found_bugs:
        print("=========================")
        print("Found the following bugs:")
        print("=========================")
        for found_bug in found_bugs:
            print(f"\t - {found_bug.bug_type}: {found_bug.bug_description}")