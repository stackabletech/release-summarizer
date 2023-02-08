from .args import parse_args
from .summary import summary, render
from sys import exit


def main():
    args = parse_args()
    sum = summary(args)
    print(render(sum, args.template))
    exit(0)


main()
