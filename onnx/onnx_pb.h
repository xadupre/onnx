/*
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ONNX_ONNX_PB_H
#define ONNX_ONNX_PB_H

// Defines ONNX_EXPORT and ONNX_IMPORT. On Windows, this corresponds to
// different declarations (dllexport and dllimport). On Linux/Mac, it just
// resolves to the same "default visibility" setting.
#if defined(_MSC_VER)
#if defined(ONNX_BUILD_SHARED_LIBS) || defined(ONNX_BUILD_MAIN_LIB)
#define ONNX_EXPORT __declspec(dllexport)
#define ONNX_IMPORT __declspec(dllimport)
#else
#define ONNX_EXPORT
#define ONNX_IMPORT
#endif
#else
#if defined(__GNUC__)
#define ONNX_EXPORT __attribute__((__visibility__("default")))
#else
#define ONNX_EXPORT
#endif
#define ONNX_IMPORT ONNX_EXPORT
#endif

// ONNX_API is a macro that, depends on whether you are building the
// main ONNX library or not, resolves to either ONNX_EXPORT or
// ONNX_IMPORT.

#if defined(ONNX_BUILD_SHARED_LIBS) || defined(ONNX_BUILD_MAIN_LIB)
#define ONNX_API ONNX_EXPORT
#else
#define ONNX_API ONNX_IMPORT
#endif

#include "onnx/onnx2/cpu/onnx2.h"

using Message = ONNX_NAMESPACE::v2::Message;
using AttributeProto = ONNX_NAMESPACE::v2::AttributeProto;
using FunctionProto = ONNX_NAMESPACE::v2::FunctionProto;
using GraphProto = ONNX_NAMESPACE::v2::GraphProto;
using ModelProto = ONNX_NAMESPACE::v2::ModelProto;
using NodeProto = ONNX_NAMESPACE::v2::NodeProto;
using SparseTensorProto = ONNX_NAMESPACE::v2::SparseTensorProto;
using TensorProto = ONNX_NAMESPACE::v2::TensorProto;
using TensorShapeProto = ONNX_NAMESPACE::v2::TensorShapeProto;
using TypeProto = ONNX_NAMESPACE::v2::TypeProto;
using TensorShapeProto_Dimension = ONNX_NAMESPACE::v2::TensorShapeProto::Dimension;

using AttributeProto_AttributeType = ONNX_NAMESPACE::v2::AttributeProto::AttributeType;
using TypeProto_Map = ONNX_NAMESPACE::v2::TypeProto::Map;
using TypeProto_Sequence = ONNX_NAMESPACE::v2::TypeProto::Sequence;
using TypeProto_SparseTensor = ONNX_NAMESPACE::v2::TypeProto::SparseTensor;
using TypeProto_Tensor = ONNX_NAMESPACE::v2::TypeProto::Tensor;

#define AttributeProto_AttributeType_FLOAT ONNX_NAMESPACE::v2::AttributeProto::AttributeType::FLOAT
#define AttributeProto_AttributeType_FLOATS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::FLOATS
#define AttributeProto_AttributeType_GRAPH ONNX_NAMESPACE::v2::AttributeProto::AttributeType::GRAPH
#define AttributeProto_AttributeType_GRAPHS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::GRAPHS
#define AttributeProto_AttributeType_INT ONNX_NAMESPACE::v2::AttributeProto::AttributeType::INT
#define AttributeProto_AttributeType_INTS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::INTS
#define AttributeProto_AttributeType_STRING ONNX_NAMESPACE::v2::AttributeProto::AttributeType::STRING
#define AttributeProto_AttributeType_STRINGS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::STRINGS
#define AttributeProto_AttributeType_TENSOR ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TENSOR
#define AttributeProto_AttributeType_TENSORS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TENSORS
#define AttributeProto_AttributeType_TYPE_PROTO ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TYPE_PROTO
#define AttributeProto_AttributeType_TYPE_PROTOS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TYPE_PROTOS

#endif // ! ONNX_ONNX_PB_H
