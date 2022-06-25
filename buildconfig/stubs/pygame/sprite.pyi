from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    SupportsFloat,
    Tuple,
    Union,
)

from pygame.rect import Rect
from pygame.surface import Surface

from ._common import RectValue

class Sprite:
    image: Optional[Surface] = None
    rect: Optional[Rect] = None
    @property
    def layer(self) -> int: ...
    @layer.setter
    def layer(self, value: int) -> None: ...
    def __init__(self, *groups: AbstractGroup) -> None: ...
    def add_internal(self, group: AbstractGroup) -> None: ...
    def remove_internal(self, group: AbstractGroup) -> None: ...
    def update(self, *args: Any, **kwargs: Any) -> None: ...
    def add(self, *groups: AbstractGroup) -> None: ...
    def remove(self, *groups: AbstractGroup) -> None: ...
    def kill(self) -> None: ...
    def alive(self) -> bool: ...
    def groups(self) -> List[AbstractGroup]: ...

class DirtySprite(Sprite):
    dirty: int
    blendmode: int
    source_rect: Rect
    visible: int
    _layer: int
    def _set_visible(self, val: int) -> None: ...
    def _get_visible(self) -> int: ...

class AbstractGroup:
    spritedict: Dict[Sprite, Rect]
    lostsprites: List[int]  # I think
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Sprite]: ...
    def __bool__(self) -> bool: ...
    def __contains__(self, item: Any) -> bool: ...
    def add_internal(self, sprite: Sprite, layer: None = None) -> None: ...
    def remove_internal(self, sprite: Sprite) -> None: ...
    def has_internal(self, sprite: Sprite) -> bool: ...
    def copy(self) -> AbstractGroup: ...
    def sprites(self) -> List[Sprite]: ...
    def add(
        self,
        *sprites: Union[Sprite, AbstractGroup, Iterable[Union[Sprite, AbstractGroup]]]
    ) -> None: ...
    def remove(self, *sprites: Sprite) -> None: ...
    def has(self, *sprites: Sprite) -> bool: ...
    def update(self, *args: Any, **kwargs: Any) -> None: ...
    def draw(self, surface: Surface) -> List[Rect]: ...
    def clear(self, surface: Surface, bgd: Surface) -> None: ...
    def empty(self) -> None: ...

class Group(AbstractGroup):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None: ...
    def copy(self) -> Group: ...

class RenderPlain(Group):
    def copy(self) -> RenderPlain: ...

class RenderClear(Group):
    def copy(self) -> RenderClear: ...

class RenderUpdates(Group):
    def copy(self) -> RenderUpdates: ...
    def draw(self, surface: Surface) -> List[Rect]: ...

class OrderedUpdates(RenderUpdates):
    def copy(self) -> OrderedUpdates: ...

class LayeredUpdates(AbstractGroup):
    def __init__(self, *sprites: Sprite, **kwargs: Any) -> None: ...
    def copy(self) -> LayeredUpdates: ...
    def add(
        self,
        *sprites: Union[Sprite, AbstractGroup, Iterable[Union[Sprite, AbstractGroup]]],
        **kwargs: Any
    ) -> None: ...
    def draw(self, surface: Surface) -> List[Rect]: ...
    def get_sprites_at(
        self, pos: Union[Tuple[int, int], List[int]]
    ) -> List[Sprite]: ...
    def get_sprite(self, idx: int) -> Sprite: ...
    def remove_sprites_of_layer(self, layer_nr: int) -> List[Sprite]: ...
    def layers(self) -> List[int]: ...
    def change_layer(self, sprite: Sprite, new_layer: int) -> None: ...
    def get_layer_of_sprite(self, sprite: Sprite) -> int: ...
    def get_top_layer(self) -> int: ...
    def get_bottom_layer(self) -> int: ...
    def move_to_front(self, sprite: Sprite) -> None: ...
    def move_to_back(self, sprite: Sprite) -> None: ...
    def get_top_sprite(self) -> Sprite: ...
    def get_sprites_from_layer(self, layer: int) -> List[Sprite]: ...
    def switch_layer(self, layer1_nr: int, layer2_nr: int) -> None: ...

class LayeredDirty(LayeredUpdates):
    def __init__(self, *sprites: DirtySprite, **kwargs: Any) -> None: ...
    def copy(self) -> LayeredDirty: ...
    def draw(self, surface: Surface, bgd: Optional[Surface] = None) -> List[Rect]: ...
    def clear(self, surface: Surface, bgd: Surface) -> None: ...
    def repaint_rect(self, screen_rect: RectValue) -> None: ...
    def set_clip(self, screen_rect: Optional[RectValue] = None) -> None: ...
    def get_clip(self) -> Rect: ...
    def set_timing_treshold(
        self, time_ms: SupportsFloat
    ) -> None: ...  # This actually accept any value
    def set_timing_threshold(
        self, time_ms: SupportsFloat
    ) -> None: ...  # This actually accept any value

class GroupSingle(AbstractGroup):
    sprite: Sprite
    def __init__(self, sprite: Optional[Sprite] = None) -> None: ...
    def copy(self) -> GroupSingle: ...

def spritecollide(
    sprite: Sprite,
    group: AbstractGroup,
    dokill: bool,
    collided: Optional[Callable[[Sprite, Sprite], bool]] = None,
) -> List[Sprite]: ...
def collide_rect(left: Sprite, right: Sprite) -> bool: ...

class collide_rect_ratio:
    ratio: float
    def __init__(self, ratio: float) -> None: ...
    def __call__(self, left: Sprite, right: Sprite) -> bool: ...

def collide_circle(left: Sprite, right: Sprite) -> bool: ...

class collide_circle_ratio:
    ratio: float
    def __init__(self, ratio: float) -> None: ...
    def __call__(self, left: Sprite, right: Sprite) -> bool: ...

def collide_mask(left: Sprite, right: Sprite) -> Tuple[int, int]: ...
def groupcollide(
    groupa: AbstractGroup,
    groupb: AbstractGroup,
    dokilla: bool,
    dokillb: bool,
    collided: Optional[Callable[[Sprite, Sprite], bool]] = None,
) -> Dict[Sprite, Sprite]: ...
def spritecollideany(
    sprite: Sprite,
    group: AbstractGroup,
    collided: Optional[Callable[[Sprite, Sprite], bool]] = None,
) -> Sprite: ...
