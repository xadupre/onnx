# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import numpy as np

import onnx
from onnx.backend.test.case.base import Base
from onnx.backend.test.case.node import expect


class Abs(Base):
    @staticmethod
    def export() -> None:
        node = onnx.helper.make_node(
            "Abs",
            inputs=["x"],
            outputs=["y"],
        )
        x = np.random.randn(3, 4, 5).astype(np.float32)
        y = np.abs(x)

        expect(node, inputs=[x], outputs=[y], name="test_abs")
