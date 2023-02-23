# SPDX-License-Identifier: Apache-2.0

import itertools
import os
import platform
import unittest
from typing import Any, Optional, Sequence, Tuple

import numpy

import onnx.backend.base
import onnx.backend.test
import onnx.shape_inference
import onnx.version_converter
from onnx import ModelProto, NodeProto, TensorProto
from onnx.backend.base import Device, DeviceType
from onnx.backend.test.runner import BackendIsNotSupposedToImplementIt
from onnx.reference import ReferenceEvaluator

# The following just executes a backend based on ReferenceEvaluator through the backend test


class ReferenceEvaluatorBackendRep(onnx.backend.base.BackendRep):
    def __init__(self, session):
        self._session = session

    def run(self, inputs, **kwargs):
        if isinstance(inputs, list):
            feeds = {}
            for i, inp in enumerate(self._session.input_names):
                feeds[inp] = inputs[i]
        elif isinstance(inputs, dict):
            feeds = inputs
        elif isinstance(inputs, numpy.ndarray):
            names = self._session.input_names
            if len(names) != 1:
                raise RuntimeError(f"Expecting one input not {len(names)}.")
            feeds = {names[0]: inputs}
        else:
            raise TypeError(f"Unexpected input type {type(inputs)!r}.")
        outs = self._session.run(None, feeds)
        return outs


class ReferenceEvaluatorBackend(onnx.backend.base.Backend):
    @classmethod
    def is_opset_supported(cls, model):
        return True, ""

    @classmethod
    def supports_device(cls, device: str) -> bool:
        d = Device(device)
        return d.type == DeviceType.CPU

    @classmethod
    def create_inference_session(cls, model):
        return ReferenceEvaluator(model)

    @classmethod
    def prepare(
        cls, model: Any, device: str = "CPU", **kwargs: Any
    ) -> ReferenceEvaluatorBackendRep:
        # if isinstance(model, ReferenceEvaluatorBackendRep):
        #    return model
        if isinstance(model, ReferenceEvaluator):
            return ReferenceEvaluatorBackendRep(model)
        if isinstance(model, (str, bytes, ModelProto)):
            inf = cls.create_inference_session(model)
            return cls.prepare(inf, device, **kwargs)
        raise TypeError(f"Unexpected type {type(model)} for model.")

    @classmethod
    def run_model(cls, model, inputs, device=None, **kwargs):
        rep = cls.prepare(model, device, **kwargs)
        return rep.run(inputs, **kwargs)

    @classmethod
    def run_node(cls, node, inputs, device=None, outputs_info=None, **kwargs):
        raise NotImplementedError("Unable to run the model node by node.")


backend_test = onnx.backend.test.BackendTest(ReferenceEvaluatorBackend, __name__)

if os.getenv("APPVEYOR"):
    backend_test.exclude("(test_vgg19|test_zfnet)")
if platform.architecture()[0] == "32bit":
    backend_test.exclude("(test_vgg19|test_zfnet|test_bvlc_alexnet)")

# The following tests are too slow with the reference implementation.
backend_test.exclude(
    "(test_bvlc_alexnet|test_inception_v1|test_inception_v2|test_squeezenet)"
)

# The following tests cannot pass because they consists in generating random number.
backend_test.exclude("(test_bernoulli)")

# import all test cases at global scope to make them visible to python.unittest
globals().update(backend_test.test_cases)

if __name__ == "__main__":
    unittest.main(verbosity=2)
