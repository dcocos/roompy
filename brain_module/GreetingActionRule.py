import logging

from brain_module import Brain


class GreetingActionRule:
    def __init__(self, brain: Brain):
        self.brain = brain
        self.greeted_events = {}

    def check_do(self):
        brain = self.brain
        for event in brain.current_open_events:
            if event.start < brain.current_time < event.end and event.id not in self.greeted_events:
                logging.info(f'Movement detected and event not greeted, greeting it.')
                self.greeted_events[event.id] = True
                brain.speak.speak('Hello puny human. Thank you for actually showing up for your reservation. '
                                  'Be sure to leave on time.')
