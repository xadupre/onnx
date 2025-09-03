<!--
Copyright (c) ONNX Project Contributors

SPDX-License-Identifier: Apache-2.0
-->

# Installation

## Official Python packages

ONNX released packages are published in PyPi.

```sh
pip install onnx  # or pip install onnx[reference] for optional reference implementation dependencies
```

[ONNX weekly packages](https://pypi.org/project/onnx-weekly/) are published in PyPI to enable experimentation and early testing.

## vcpkg packages

ONNX is in the maintenance list of [vcpkg](https://github.com/microsoft/vcpkg), you can easily use vcpkg to build and install it.

```sh
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
./bootstrap-vcpkg.bat # For powershell
./bootstrap-vcpkg.sh # For bash
./vcpkg install onnx
```

## Conda packages

A binary build of ONNX is available from [Conda](https://conda.io), in [conda-forge](https://conda-forge.org/):

```sh
conda install -c conda-forge onnx
```

## Build ONNX from Source

Before building from source uninstall any existing versions of ONNX via `pip uninstall onnx`.

C++17 or higher C++ compiler version is required to build ONNX from source. Still, users can specify their own `CMAKE_CXX_STANDARD` version for building ONNX.

### Windows

```
git clone https://github.com/onnx/onnx.git
cd onnx
git submodule update --init --recursive
# prefer lite proto
pip install -e . -v
```

### Conda-forge-based development environment

A conda-forge-based development environment is also provided.
After installing the [pixi package manager](https://prefix.dev/), users may directly execute any of the following commands. Upon doing so pixi will install the required dependencies automatically in isolated environments.
Running

```sh
pixi run install
```

builds and installs the `onnx` package into the default environment.
After the installation has completed one can run the gtest and pytest suites via the pixi-tasks of the same name:

```sh
pixi run gtest
```

and

```sh
pixi run pytest
```

Further task for re-generating the operator documentation (`pixi run gen-docs`), setting-up lintrunner (`pixi run lintrunner-init`), and executing lintrunner (`pixi run lintrunner-run`) are also available.

### Linux

You can build ONNX as:

```sh
git clone https://github.com/onnx/onnx.git
cd onnx
git submodule update --init --recursive
# Optional: prefer lite proto
pip install -e . -v
```

### Mac

You can build ONNX as:

```sh
git clone --recursive https://github.com/onnx/onnx.git
cd onnx
# Optional: prefer lite proto
pip install -e . -v
```

## Verify Installation

After installation, run

```sh
python -c "import onnx"
```

to verify it works.

## Common Build Options

For full list refer to CMakeLists.txt

### Environment variables

* `USE_MSVC_STATIC_RUNTIME` should be 1 or 0, not ON or OFF. When set to 1 ONNX links statically to runtime library.
**Default**: `USE_MSVC_STATIC_RUNTIME=0`

* `DEBUG` should be 0 or 1. When set to 1 ONNX is built in debug mode. For debug versions of the dependencies, you need to open the [CMakeLists file](https://github.com/onnx/onnx/blob/main/CMakeLists.txt) and append a letter `d` at the end of the package name lines.
**Default**: `Debug=0`

### CMake variables

* `ONNX_WERROR` should be `ON` or `OFF`. When set to `ON` warnings are treated as errors.
**Default**: `ONNX_WERROR=OFF` in local builds, `ON` in CI and release pipelines.

## Common Errors

* Note: the `import onnx` command does not work from the source checkout directory; in this case you'll see `ModuleNotFoundError: No module named 'onnx.onnx_cpp2py_export'`. Change into another directory to fix this error.

* If you run into any issues while building ONNX from source, and your error message reads, `Could not find pythonXX.lib`, ensure that you have consistent Python versions for common commands, such as `python` and `pip`. Clean all existing build files and rebuild ONNX again.
