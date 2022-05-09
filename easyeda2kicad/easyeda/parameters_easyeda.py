# Global imports
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union

from pydantic import BaseModel, validator


class EasyedaPinType(Enum):
    unspecified = 0
    input = 1
    output = 2
    bidirectional = 3
    power = 4


# ------------------------- Symbol -------------------------
class EeSymbolBbox(BaseModel):
    x: float
    y: float


# ---------------- PIN ----------------
class EeSymbolPinSettings(BaseModel):
    is_displayed: bool
    type: str
    spice_pin_number: str
    pos_x: float
    pos_y: float
    rotation: int
    id: str
    is_locked: bool

    @validator("is_displayed", pre=True)
    def parse_display_field(cls, field: str) -> bool:
        return True if field == "show" else field

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, is_locked: str) -> str:
        return is_locked or False

    @validator("rotation", pre=True)
    def empty_str_rotation(cls, rotation: str) -> str:
        return rotation or 0.0


class EeSymbolPinDot(BaseModel):
    dot_x: float
    dot_y: float


@dataclass
class EeSymbolPinPath:
    path: str
    color: str


class EeSymbolPinName(BaseModel):
    is_displayed: bool
    pos_x: float
    pos_y: float
    rotation: int
    text: str
    text_anchor: str
    font: str
    font_size: float

    @validator("font_size", pre=True)
    def empty_str_font(cls, font_size: str) -> float:
        if isinstance(font_size, str) and "pt" in font_size:
            return float(font_size.replace("pt", ""))
        return font_size or 7.0

    @validator("is_displayed", pre=True)
    def parse_display_field(cls, field: str) -> str:
        return True if field == "show" else field

    @validator("rotation", pre=True)
    def empty_str_rotation(cls, rotation: str) -> str:
        return rotation or 0.0


class EeSymbolPinDotBis(BaseModel):
    is_displayed: bool
    circle_x: float
    circle_y: float

    @validator("is_displayed", pre=True)
    def parse_display_field(cls, field: str) -> str:
        return True if field == "show" else field


class EeSymbolPinClock(BaseModel):
    is_displayed: bool
    path: str

    @validator("is_displayed", pre=True)
    def parse_display_field(cls, field: str) -> str:
        return True if field == "show" else field


@dataclass
class EeSymbolPin:
    settings: EeSymbolPinSettings
    pin_dot: EeSymbolPinDot
    pin_path: EeSymbolPinPath
    name: EeSymbolPinName
    dot: EeSymbolPinDotBis
    clock: EeSymbolPinClock


# ---------------- RECTANGLE ----------------
class EeSymbolRectangle(BaseModel):
    pos_x: float
    pos_y: float
    rx: Union[float, None]
    ry: Union[float, None]
    width: float
    height: float
    stroke_color: str
    stroke_width: str
    stroke_style: str
    fill_color: str
    id: str
    is_locked: bool

    @validator("*", pre=True)
    def empty_str_to_none(cls, field: str) -> str:
        return field or None


# ---------------- CIRCLE ----------------
class EeSymbolCircle(BaseModel):
    ...  # TODO


# ---------------- ARC ----------------
class EeSymbolArc(BaseModel):
    ...  # TODO


# ---------------- POLYLINE ----------------
class EeSymbolPolyline(BaseModel):
    points: str
    stroke_color: str
    stroke_width: str
    stroke_style: str
    fill_color: str
    id: str
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field: str) -> str:
        return field or False


# ---------------- POLYGON ----------------
class EeSymbolPolygon(EeSymbolPolyline):
    ...


# ---------------- PATH ----------------
# TODO : EeSymbolPath.paths should be a SVG PATH https://www.w3.org/TR/SVG11/paths.html#PathElement
# TODO : small svg parser and then convert to kicad
# TODO: support bezier curve, currently paths are seen as polygone
class EeSymbolPath(BaseModel):
    paths: str
    stroke_color: str
    stroke_width: str
    stroke_style: str
    fill_color: str
    id: str
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field: str) -> str:
        return field or False

    # @validator("paths", pre=True)
    # def clean_svg_path(cls, paths:str):
    #     return paths.replace("M", "").replace("C","")


# ---------------- SYMBOL ----------------
@dataclass
class EeSymbolInfo:
    name: str = ""
    prefix: str = ""
    package: str = ""
    manufacturer: str = ""
    datasheet: str = ""
    lcsc_id: str = ""
    jlc_id: str = ""


@dataclass
class EeSymbol:
    info: EeSymbolInfo
    bbox: EeSymbolBbox
    pins: List[EeSymbolPin] = field(default_factory=list)
    rectangles: List[EeSymbolRectangle] = field(default_factory=list)
    polylines: List[EeSymbolPolyline] = field(default_factory=list)
    polygons: List[EeSymbolPolygon] = field(default_factory=list)
    paths: List[EeSymbolPath] = field(default_factory=list)


# ------------------------- Footprint -------------------------


def convert_to_mm(dim: float) -> float:
    return float(dim) * 10 * 0.0254


@dataclass
class EeFootprintBbox:

    x: float
    y: float

    def convert_to_mm(self) -> None:
        self.x = convert_to_mm(self.x)
        self.y = convert_to_mm(self.y)


class EeFootprintPad(BaseModel):
    shape: str
    center_x: float
    center_y: float
    width: float
    height: float
    layer_id: int
    net: str
    number: str
    hole_radius: float
    points: str
    rotation: float
    id: str
    hole_length: float
    hole_point: str
    is_plated: bool
    is_locked: bool

    def convert_to_mm(self) -> None:
        self.center_x = convert_to_mm(self.center_x)
        self.center_y = convert_to_mm(self.center_y)
        self.width = convert_to_mm(self.width)
        self.height = convert_to_mm(self.height)
        self.hole_radius = convert_to_mm(self.hole_radius)
        self.hole_length = convert_to_mm(self.hole_length)

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field: str) -> str:
        return field or False

    @validator("rotation", pre=True)
    def empty_str_rotation(cls, field: str) -> str:
        return field or 0.0


class EeFootprintTrack(BaseModel):
    stroke_width: float
    layer_id: int
    net: str
    points: str
    id: str
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field: str) -> str:
        return field or False

    def convert_to_mm(self) -> None:
        self.stroke_width = convert_to_mm(self.stroke_width)


class EeFootprintHole(BaseModel):
    center_x: float
    center_y: float
    radius: float
    id: str
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field: str) -> str:
        return field or False

    def convert_to_mm(self) -> None:
        self.center_x = convert_to_mm(self.center_x)
        self.center_y = convert_to_mm(self.center_y)
        self.radius = convert_to_mm(self.radius)


class EeFootprintCircle(BaseModel):
    cx: float
    cy: float
    radius: float
    stroke_width: float
    layer_id: int
    id: str
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field: str) -> str:
        return field or False

    def convert_to_mm(self) -> None:
        self.cx = convert_to_mm(self.cx)
        self.cy = convert_to_mm(self.cy)
        self.radius = convert_to_mm(self.radius)
        self.stroke_width = convert_to_mm(self.stroke_width)


class EeFootprintRectangle(BaseModel):
    x: float
    y: float
    width: float
    height: float
    stroke_width: float
    id: str
    layer_id: int
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field):
        return False if field == "" else field

    def convert_to_mm(self):
        self.x = convert_to_mm(self.x)
        self.y = convert_to_mm(self.y)
        self.width = convert_to_mm(self.width)
        self.height = convert_to_mm(self.height)


class EeFootprintArc(BaseModel):
    stroke_width: float
    layer_id: int
    net: str
    path: str
    helper_dots: str
    id: str
    is_locked: bool

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field):
        return False if field == "" else field


class EeFootprintText(BaseModel):
    type: str
    center_x: float
    center_y: float
    stroke_width: float
    rotation: int
    miror: str
    layer_id: int
    net: str
    font_size: float
    text: str
    text_path: str
    is_displayed: bool
    id: str
    is_locked: bool

    @validator("is_displayed", pre=True)
    def empty_str_display(cls, field):
        return True if field == "" else field

    @validator("is_locked", pre=True)
    def empty_str_lock(cls, field):
        return False if field == "" else field

    @validator("rotation", pre=True)
    def empty_str_rotation(cls, field):
        return 0.0 if field == "" else field

    def convert_to_mm(self):

        self.center_x = convert_to_mm(self.center_x)
        self.center_y = convert_to_mm(self.center_y)
        self.stroke_width = convert_to_mm(self.stroke_width)
        self.font_size = convert_to_mm(self.font_size)


# ---------------- FOOTPRINT ----------------


@dataclass
class EeSymbolPinPath:
    path: str
    color: str


@dataclass
class EeFootprintInfo:
    name: str
    fp_type: str
    model_3d_name: str


# ------------------------- 3D MODEL -------------------------
class Ee3dModelBase(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def convert_to_mm(self) -> None:
        self.x = convert_to_mm(self.x)
        self.y = convert_to_mm(self.y)
        # self.z = convert_to_mm(self.z)


@dataclass
class Ee3dModel:
    name: str
    uuid: str
    translation: Ee3dModelBase
    rotation: Ee3dModelBase
    raw_obj: str = None

    def convert_to_mm(self) -> None:
        self.translation.convert_to_mm()
        # self.translation.z = self.translation.z


@dataclass
class ee_footprint:
    info: EeFootprintInfo
    bbox: EeFootprintBbox
    model_3d: Ee3dModel
    pads: List[EeFootprintPad] = field(default_factory=list)
    tracks: List[EeFootprintTrack] = field(default_factory=list)
    holes: List[EeFootprintHole] = field(default_factory=list)
    circles: List[EeFootprintCircle] = field(default_factory=list)
    arcs: List[EeFootprintArc] = field(default_factory=list)
    rectangles: List[EeFootprintRectangle] = field(default_factory=list)
    texts: List[EeFootprintText] = field(default_factory=list)
