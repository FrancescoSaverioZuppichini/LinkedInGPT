from typing import Callable

from src.actions import Action
from src.types import GeneratedContent


def input_confirmation(repeat_func: Callable) -> bool:
    while True:
        user_input = input("Proceed [yes/no/repeat]").lower().strip()
        match user_input:
            case "yes":
                return True
            case "no":
                return False
            case "repeat":
                return repeat_func()
