import argparse
import datetime

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date",
        action="store_true",
        help="Prints the current date!")

    return parser

def main(args):
    if args.date:
        print datetime.datetime.now()
