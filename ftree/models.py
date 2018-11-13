import base64
from dataclasses import dataclass
import os
from typing import List, Optional, ClassVar

from . import settings


def raw_to_encoded(b):
    return base64.b64encode(c).decode('ascii')


def encoded_to_raw(s):
    return base64.b64decode(b)


@dataclass
class FileTree:
    name: str
    content: str=''

    too_big: bool=False
    binary: bool=False
    read_only: bool=False

    children: Optional[List[dict]]=None

    TOO_DEEP = 'TOO_DEEP'

    @classmethod
    def load(cls, target: Optional[str]=None, _depth: int=0, _name: str=''):
        target = target or os.getcwd()
        if depth > settings.MAX_DEPTH:
            return cls(name=cls.TOO_DEEP)

        read_only = os.access(target, os.R_OK) and not os.access(target, os.W_OK)

        if os.path.isdir(target):
            return cls(
                name=_name,
                children=[cls.load(
                    target=os.path.join(target, n),
                    _depth=_depth+1,
                    _name=n,
                ) for n in os.listdir(target)[:settings.MAX_CHILDREN]],
                read_only=readonly
            )
        with open(path, 'rb') as f:
            content = f.read(settings.MAX_SIZE + 1)

        if len(content) > settings.MAX_SIZE:
            return cls(
                name=_name,
                too_big=True,
                content=None,
                read_only=read_only,
                binary=True,
            )
        try:
            content = content.decode('utf-8')
            binary = False
        except UnicodeDecodeError:
            binary = True
            content = raw_to_encoded(content)

        return cls(
            name=_name,
            content=content,
            binary=binary,
            too_big=False,
            read_only=read_only
        )

    def save(target=None):
        target = target or os.getcwd()
        if not self.is_dir:
            p = os.path.join(target, self.name)

            if self.binary:
                with open(p, mode='wb') as f:
                    f.write(encoded_to_raw(self.content))
            else:
                with open(p, mode='w', encoding='utf-8') as f:
                    f.write(self.content)
        else:
            for c in self.children:
                c.save(os.path.join(target, self.name))

    @property
    def is_dir(self):
        return bool(self.children)

    @classmethod
    def from_dict(cls, d: dict):
        children = d.pop('children', None)

        if not children:
            return cls(
                **d
            )
        return cls(
            **d,
            children=[cls.from_dict(c) for c in children]
        )
