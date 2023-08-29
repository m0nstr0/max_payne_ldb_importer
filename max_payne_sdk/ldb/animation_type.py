from __future__ import annotations

from max_payne_sdk.ldb.fsm_type import FSMMessageContainer


class Graph:
    def __init__(self, sample_rate: int) -> None:
        self.sample_rate: int = sample_rate
        self.points: list[float] = []

    def addPoint(self, f: float) -> None:
        self.points.append(f)


class Animation:
    def __init__(self, animation_name: str, length_in_secs: float, start_transform, end_transform, leaving_first_frame: FSMMessageContainer, returning_first_frame: FSMMessageContainer, reaching_second_frame: FSMMessageContainer, translation_graph: Graph, rotation_graph: Graph) -> None:
        self.animation_name: str = animation_name
        self.length_in_secs: float = length_in_secs
        self.start_transform = start_transform
        self.end_transform = end_transform
        self.leaving_first_frame: FSMMessageContainer = leaving_first_frame
        self.returning_first_frame: FSMMessageContainer = returning_first_frame
        self.reaching_second_frame: FSMMessageContainer = reaching_second_frame
        self.translation_graph: Graph = translation_graph
        self.rotation_graph: Graph = rotation_graph


class AnimationContainer:
    def __init__(self) -> None:
        self.animations: list[Animation] = []

    def add(self, animation: Animation):
        self.animations.append(animation)
