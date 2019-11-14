import logging
from time import sleep

from utils.RepeatedTimer import RepeatedTimer
from brain_module.Brain import Brain


logging.basicConfig(level=logging.DEBUG)


def main():
    brain = Brain()
    rt = RepeatedTimer(5, brain.run_cycle)
    try:
        logging.info('Roompy is very vigilant')
        sleep(240)
    finally:
        logging.info('Roompy has fallen asleep')
        rt.stop()


if __name__ == '__main__':
    main()
