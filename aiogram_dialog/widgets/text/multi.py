from typing import Any, Callable, Dict, Hashable, Union
from warnings import warn

from aiogram_dialog.api.internal import DialogManager
from .base import Multi as _Multi
from .base import Text
from ..when import WhenCondition

Selector = Callable[[Dict, "Case", DialogManager], Hashable]


class Multi(_Multi):
    def __init__(self, *texts: Text, sep="\n", when: WhenCondition = None):
        super().__init__(*texts, sep=sep, when=when)
        warn(
            "This is compatibility class"
            " and will be removed in aiogram_dialog==2.0, "
            " fix using `from aiogram_dialog.widgets.text import Multi`",
            DeprecationWarning,
            stacklevel=2,
        )


def new_case_field(fieldname: str) -> Selector:
    def case_field(
            data: Dict, widget: "Case", manager: DialogManager,
    ) -> Hashable:
        return data.get(fieldname)

    return case_field


class Case(Text):
    def __init__(
            self,
            texts: Dict[Any, Text],
            selector: Union[str, Selector],
            when: WhenCondition = None,
    ):
        super().__init__(when)
        self.texts = texts
        if isinstance(selector, str):
            self.selector = new_case_field(selector)
        else:
            self.selector = selector

    async def _render_text(self, data, manager: DialogManager) -> str:
        selection = self.selector(data, self, manager)
        return await self.texts[selection].render_text(data, manager)
