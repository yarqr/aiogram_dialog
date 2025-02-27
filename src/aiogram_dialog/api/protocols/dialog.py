from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Type, Union, runtime_checkable

from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.api.entities import Data, LaunchMode, NewMessage
from ..internal import Widget

from ... import ChatEvent
from ..entities.context import DataDict
from .manager import DialogManager


@runtime_checkable
class DialogProtocol(Protocol):
    @property
    def launch_mode(self) -> LaunchMode:
        raise NotImplementedError

    @abstractmethod
    def states_group_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def states(self) -> List[State]:
        raise NotImplementedError

    @abstractmethod
    def states_group(self) -> Type[StatesGroup]:
        raise NotImplementedError

    @abstractmethod
    async def process_close(
        self,
        result: Any,
        manager: DialogManager,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def process_start(
        self,
        manager: "DialogManager",
        start_data: Data,
        state: Optional[State] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def process_result(
        self,
        start_data: Data,
        result: Any,
        manager: "DialogManager",
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, widget_id: str) -> Optional[Widget]:
        raise NotImplementedError

    @abstractmethod
    async def load_data(
        self,
        manager: DialogManager,
    ) -> Dict[str, Union[DataDict, Dict[str, Any], ChatEvent]]:
        raise NotImplementedError

    @abstractmethod
    async def render(self, manager: DialogManager) -> NewMessage:
        raise NotImplementedError
