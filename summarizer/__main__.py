from .args import parse_args
from .summary import summary, render


def main():
    args = parse_args()
    sum = summary(args)

    print(render(sum, "release-notes.adoc.j2"))


if __name__ == '__main__':
    main()
