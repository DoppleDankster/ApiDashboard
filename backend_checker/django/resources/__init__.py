#!/usr/bin/env python3
from abc import ABC, abstractclassmethod, abstractmethod
from backend_checker.services.backend import Backend


class Resource(ABC):
    def __init__(self, backend: Backend):
        self.backend = backend

    @abstractclassmethod
    def from_json(cls, attributes):
        return cls(**attributes)

    @abstractmethod
    def to_json(self):
        pass
