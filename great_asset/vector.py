from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types_.save_file import InnerVectorValue

__all__ = ("Vector",)


class Vector:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def __repr__(self) -> str:
        return f"<Vector x={self.x} y={self.y} z={self.z}>"

    @classmethod
    def default(cls) -> Vector:
        return cls(10, 2, -11)

    @classmethod
    def from_dict(cls, payload: InnerVectorValue) -> Vector:
        return cls(**payload)

    def serialise(self) -> InnerVectorValue:
        return {"x": self.x, "y": self.y, "z": self.z}
