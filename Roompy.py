import logging

from brain_module.Brain import Brain
from opencvdetect import Detector
from utils.RepeatedTimer import RepeatedTimer

logging.basicConfig(level=logging.DEBUG)


def main():
    brain = Brain()
    rt = RepeatedTimer(5, brain.run_cycle)
    try:
        logging.info('Roompy is very vigilant')
        detector = Detector()
        detector.motionDetected += brain.update_last_movement
        detector.detect()
    finally:
        logging.info('Roompy has fallen asleep')
        rt.stop()


if __name__ == '__main__':
    main()
