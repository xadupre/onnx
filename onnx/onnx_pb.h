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
using MapProto = ONNX_NAMESPACE::v2::MapProto;
using ModelProto = ONNX_NAMESPACE::v2::ModelProto;
using NodeProto = ONNX_NAMESPACE::v2::NodeProto;
using OperatorSetIdProto = ONNX_NAMESPACE::v2::OperatorSetIdProto;
using OptionalProto = ONNX_NAMESPACE::v2::OptionalProto;
using SequenceProto = ONNX_NAMESPACE::v2::SequenceProto;
using SparseTensorProto = ONNX_NAMESPACE::v2::SparseTensorProto;
using StringStringEntryProto = ONNX_NAMESPACE::v2::StringStringEntryProto;
using TensorProto = ONNX_NAMESPACE::v2::TensorProto;
using TensorShapeProto = ONNX_NAMESPACE::v2::TensorShapeProto;
using TypeProto = ONNX_NAMESPACE::v2::TypeProto;
using TensorShapeProto_Dimension = ONNX_NAMESPACE::v2::TensorShapeProto::Dimension;
using ValueInfoProto = ONNX_NAMESPACE::v2::ValueInfoProto;

using Version = ONNX_NAMESPACE::v2::Version;

using AttributeProto_AttributeType = ONNX_NAMESPACE::v2::AttributeProto::AttributeType;
using TensorProto_DataLocation = ONNX_NAMESPACE::v2::TensorProto::DataLocation;
using TensorProto_DataType = ONNX_NAMESPACE::v2::TensorProto::DataType;
using TypeProto_Map = ONNX_NAMESPACE::v2::TypeProto::Map;
using TypeProto_Sequence = ONNX_NAMESPACE::v2::TypeProto::Sequence;
using TypeProto_SparseTensor = ONNX_NAMESPACE::v2::TypeProto::SparseTensor;
using TypeProto_Tensor = ONNX_NAMESPACE::v2::TypeProto::Tensor;

#define TensorProto_DataType_IsValid ONNX_NAMESPACE::v2::TensorProto::DataType_IsValid

#define TensorProto_DataType_UNDEFINED ONNX_NAMESPACE::v2::TensorProto::DataType::UNDEFINED
#define TensorProto_DataType_FLOAT ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT
#define TensorProto_DataType_UINT8 ONNX_NAMESPACE::v2::TensorProto::DataType::UINT8
#define TensorProto_DataType_INT8 ONNX_NAMESPACE::v2::TensorProto::DataType::INT8
#define TensorProto_DataType_UINT16 ONNX_NAMESPACE::v2::TensorProto::DataType::UINT16
#define TensorProto_DataType_INT16 ONNX_NAMESPACE::v2::TensorProto::DataType::INT16
#define TensorProto_DataType_INT32 ONNX_NAMESPACE::v2::TensorProto::DataType::INT32
#define TensorProto_DataType_INT64 ONNX_NAMESPACE::v2::TensorProto::DataType::INT64
#define TensorProto_DataType_STRING ONNX_NAMESPACE::v2::TensorProto::DataType::STRING
#define TensorProto_DataType_BOOL ONNX_NAMESPACE::v2::TensorProto::DataType::BOOL
#define TensorProto_DataType_FLOAT16 ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT16
#define TensorProto_DataType_DOUBLE ONNX_NAMESPACE::v2::TensorProto::DataType::DOUBLE
#define TensorProto_DataType_UINT32 ONNX_NAMESPACE::v2::TensorProto::DataType::UINT32
#define TensorProto_DataType_UINT64 ONNX_NAMESPACE::v2::TensorProto::DataType::UINT64
#define TensorProto_DataType_COMPLEX64 ONNX_NAMESPACE::v2::TensorProto::DataType::COMPLEX64
#define TensorProto_DataType_COMPLEX128 ONNX_NAMESPACE::v2::TensorProto::DataType::COMPLEX128
#define TensorProto_DataType_BFLOAT16 ONNX_NAMESPACE::v2::TensorProto::DataType::BFLOAT16
#define TensorProto_DataType_FLOAT8E4M3FN ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT8E4M3FN
#define TensorProto_DataType_FLOAT8E4M3FNUZ ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT8E4M3FNUZ
#define TensorProto_DataType_FLOAT8E5M2 ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT8E5M2
#define TensorProto_DataType_FLOAT8E5M2FNUZ ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT8E5M2FNUZ
#define TensorProto_DataType_UINT4 ONNX_NAMESPACE::v2::TensorProto::DataType::UINT4
#define TensorProto_DataType_INT4 ONNX_NAMESPACE::v2::TensorProto::DataType::INT4
#define TensorProto_DataType_FLOAT4E2M1 ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT4E2M1
#define TensorProto_DataType_FLOAT8E8M0 ONNX_NAMESPACE::v2::TensorProto::DataType::FLOAT8E8M0

#define AttributeProto_AttributeType_FLOAT ONNX_NAMESPACE::v2::AttributeProto::AttributeType::FLOAT
#define AttributeProto_AttributeType_FLOATS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::FLOATS
#define AttributeProto_AttributeType_GRAPH ONNX_NAMESPACE::v2::AttributeProto::AttributeType::GRAPH
#define AttributeProto_AttributeType_GRAPHS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::GRAPHS
#define AttributeProto_AttributeType_INT ONNX_NAMESPACE::v2::AttributeProto::AttributeType::INT
#define AttributeProto_AttributeType_INTS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::INTS
#define AttributeProto_AttributeType_SPARSE_TENSOR ONNX_NAMESPACE::v2::AttributeProto::AttributeType::SPARSE_TENSOR
#define AttributeProto_AttributeType_SPARSE_TENSORS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::SPARSE_TENSORS
#define AttributeProto_AttributeType_STRING ONNX_NAMESPACE::v2::AttributeProto::AttributeType::STRING
#define AttributeProto_AttributeType_STRINGS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::STRINGS
#define AttributeProto_AttributeType_TENSOR ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TENSOR
#define AttributeProto_AttributeType_TENSORS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TENSORS
#define AttributeProto_AttributeType_TYPE_PROTO ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TYPE_PROTO
#define AttributeProto_AttributeType_TYPE_PROTOS ONNX_NAMESPACE::v2::AttributeProto::AttributeType::TYPE_PROTOS

#define IR_VERSION Version::IR_VERSION

#endif // ! ONNX_ONNX_PB_H
