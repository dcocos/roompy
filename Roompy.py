import logging

from brain_module.Brain import Brain

logging.basicConfig(level=logging.DEBUG)


def main():
    brain = Brain()
    brain.start_thinking()


if __name__ == '__main__':
    main()
