from pydantic import BaseModel
from pydantic import ConfigDict

from fast_depends import inject
from fast_depends import Provider
from fast_depends import Depends as Depends

from typing import Callable
from typing import Any
from typing import Awaitable
from inspect import signature

class Command(BaseModel):
    model_config = ConfigDict(frozen=True)

class Mapper:
    def __init__(self, key_generator: Callable[[str], str] = lambda name: name):
        self.key_generator = key_generator
        self.command_map = dict[str, type[Command]]()

    def register(self, command_type: type[Command]):
        key = self.key_generator(command_type.__name__)
        self.map[key] = command_type
        return command_type
    
    def map(self, action: str, payload: dict[str, Any]) -> Command:
        command_type = self.command_map[action]
        return command_type.model_validate(payload)

class Bus:
    def __init__(self, key_generator: Callable[[str], str] = lambda name: name):
        self.key_generator = key_generator 
        self.command_mapper = Mapper(key_generator)
        self.dependency_provider = Provider()
        self.command_handlers = dict[str, Callable[[Command], Awaitable[Any]]]()

    @property
    def dependency_overrides(self) -> dict[Callable, Callable]:
        return self.dependency_provider.dependency_overrides        

    def register(self, handler: Callable[[Command] , Awaitable[Any]]) -> Callable[[Command] , Awaitable[Any]]:
        handler_signature = signature(handler)
        first_parameter = next(iter(handler_signature.parameters.values()))
        command_type = first_parameter.annotation
        action = self.key_generator(command_type.__name__)
        self.command_mapper.register(command_type)
        handler_with_inject = inject(dependency_overrides_provider=self.dependency_provider)(handler)
        self.command_handlers[action] = handler_with_inject
        return handler_with_inject

    async def execute(self, command: Command):
        handler = self.command_handlers.get(self.key_generator(command.__class__.__name__), None)
        if not handler:
            raise KeyError
        await handler(command)