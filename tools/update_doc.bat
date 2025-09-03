REM Copyright (c) ONNX Project Contributors

:: SPDX-License-Identifier: Apache-2.0

:: Run this script from ONNX root directory under Anaconda.
set ONNX_ML=1

python setup.py develop

python onnx\backend\test\cmd_tools.py generate-data

python onnx\backend\test\stat_coverage.py

python onnx\defs\gen_doc.py
