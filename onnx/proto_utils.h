// Copyright (c) ONNX Project Contributors
//
// SPDX-License-Identifier: Apache-2.0

#pragma once

#include <string>
#include <vector>

#include "onnx/onnx_pb.h"

namespace ONNX_NAMESPACE {

template <typename Proto>
bool ParseProtoFromBytes(Proto* proto, const char* buffer, size_t length) {
  return proto->ParseFromString(std::string(buffer, length));
}

template <typename T>
inline std::vector<T> RetrieveValues(const AttributeProto& attr);
template <>
inline std::vector<int64_t> RetrieveValues(const AttributeProto& attr) {
  return {attr.ints().begin(), attr.ints().end()};
}

template <>
inline std::vector<std::string> RetrieveValues(const AttributeProto& attr) {
  return {attr.strings().begin(), attr.strings().end()};
}

template <>
inline std::vector<float> RetrieveValues(const AttributeProto& attr) {
  return {attr.floats().begin(), attr.floats().end()};
}

} // namespace ONNX_NAMESPACE
