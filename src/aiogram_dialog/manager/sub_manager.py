import dataclasses
from typing import Any, Dict, Optional, Union, cast

from aiogram.fsm.state import State

from aiogram_dialog.api.entities import (
    ChatEvent,
    Context,
    Data,
    ShowMode,
    Stack,
    StartMode,
)
from aiogram_dialog.api.entities.context import DataDict
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.api.protocols import BaseDialogManager, DialogManager


class SubManager(DialogManager):
    def __init__(
        self,
        widget: Widget,
        manager: DialogManager,
        widget_id: str,
        item_id: str,
    ):
        self.widget = widget
        self.manager = manager
        self.widget_id = widget_id
        self.item_id = item_id

    @property
    def event(self) -> ChatEvent:
        return self.manager.event

    @property
    def middleware_data(self) -> Dict[str, Any]:
        """Middleware data."""
        return self.manager.middleware_data

    @property
    def dialog_data(self) -> DataDict:
        """Dialog data for current context."""
        return self.current_context().dialog_data

    @property
    def start_data(self) -> Data:
        """Start data for current context."""
        return self.manager.start_data

    def current_context(self) -> Context:
        context = self.manager.current_context()
        data = cast(Dict[str, Data], context.widget_data.setdefault(self.widget_id, {}))
        row_data = cast(Dict[str, Data], data.setdefault(self.item_id, {}))
        return dataclasses.replace(context, widget_data=row_data)

    def has_context(self) -> bool:
        return self.manager.has_context()

    def is_preview(self) -> bool:
        return self.manager.is_preview()

    def current_stack(self) -> Stack:
        return self.manager.current_stack()

    async def close_manager(self) -> None:
        return await self.manager.close_manager()

    async def show(self, show_mode: Optional[ShowMode] = None) -> None:
        return await self.manager.show(show_mode)

    async def answer_callback(self) -> None:
        return await self.manager.answer_callback()

    async def reset_stack(self, remove_keyboard: bool = True) -> None:
        return await self.manager.reset_stack(remove_keyboard)

    async def load_data(
        self,
    ) -> Dict[str, Union[Data, DataDict, Dict[str, Any], ChatEvent]]:
        return await self.manager.load_data()

    def find(self, widget_id: str) -> Optional[Any]:
        widget = self.widget.find(widget_id)
        if not widget:
            return None
        return widget.managed(self)

    def find_in_parent(self, widget_id: str) -> Optional[Any]:
        return self.manager.find(widget_id)

    @property
    def show_mode(self) -> ShowMode:
        return self.manager.show_mode

    @show_mode.setter
    def show_mode(self, show_mode: ShowMode) -> None:
        self.manager.show_mode = show_mode

    async def next(self, show_mode: Optional[ShowMode] = None) -> None:
        await self.manager.next(show_mode)

    async def back(self, show_mode: Optional[ShowMode] = None) -> None:
        await self.manager.back(show_mode)

    async def done(
        self,
        result: Any = None,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        await self.manager.done(result, show_mode)

    async def mark_closed(self) -> None:
        await self.manager.mark_closed()

    async def start(
        self,
        state: State,
        data: Data = None,
        mode: StartMode = StartMode.NORMAL,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        await self.manager.start(
            state=state,
            data=data,
            mode=mode,
            show_mode=show_mode,
        )

    async def switch_to(
        self,
        state: State,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        await self.manager.switch_to(state, show_mode)

    async def update(
        self,
        data: DataDict,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        self.current_context().dialog_data.update(data)
        await self.show(show_mode)

    def bg(
        self,
        user_id: Optional[int] = None,
        chat_id: Optional[int] = None,
        stack_id: Optional[str] = None,
        load: bool = False,
    ) -> BaseDialogManager:
        return self.manager.bg(
            user_id=user_id,
            chat_id=chat_id,
            stack_id=stack_id,
            load=load,
        )
