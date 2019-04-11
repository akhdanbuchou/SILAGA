from abc import ABCMeta, abstractmethod


class StateInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def filter_entry(self): raise NotImplementedError

class OmedClassifiedFilter(StateInterface):
    @override
    def filter_entry:

class FilterResponse:

    def __init__(self, ):
        self.current_state =