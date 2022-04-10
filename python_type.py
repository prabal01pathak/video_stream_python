from typing import List, Tuple, Dict, Set, Optional
from pydantic import BaseModel
import pprint


def main(name: str, list_: List[int], 
         tuple_: Tuple[int, str],
         dict_: Dict[str, int], set_: Set[int],
         optional: Optional[int], *args, **kwargs) -> dict:

    return User(name=name, list_=list_, tuple_=tuple_, dict_=dict_,
                set_=set_, optional=optional)

class User(BaseModel):
    name: int
    age: Optional[int] = None
    email: Optional[str] = None
    list_: List[int] = []
    tuple_: Tuple[int, str] = (0, '')
    dict_: Dict[str, int] = {}
    set_: Set[int] = set()

    class Config:
        arbitrary_types_allowed = True

if __name__ == '__main__':
    user = main('1', [1, 2, 3], (1, 'a'), {'a': 1}, {1, 2, 3}, 1)
    pp = pprint.PrettyPrinter(indent=4)
    print(dir(pp))
    pp.pprint(user.dict())
