# SPDX-License-Identifier: Apache-2.0
# pylint: disable=C0200,R0912,R0913,R0914,R0915,R0916,R1702,W0221

import numpy as np

from ._op_common_pool import CommonPool


class LpPool(CommonPool):
    def _run(  # type: ignore
        self,
        x,
        auto_pad=None,
        ceil_mode=None,
        dilations=None,
        kernel_shape=None,
        p=None,
        pads=None,
        strides=None,
    ):
        if (
            dilations is not None
            and (min(dilations) != max(dilations) or min(dilations) != 1)
        ) or (
            strides is not None and (min(strides) != max(strides) or min(strides) != 1)
        ):
            return self._lp_pool(
                x,
                auto_pad=auto_pad,
                ceil_mode=ceil_mode,
                dilations=dilations,
                kernel_shape=kernel_shape,
                p=p,
                pads=pads,
                strides=strides,
            )

        return CommonPool._run(
            self,
            "LP",
            0,
            x,
            auto_pad=auto_pad,
            ceil_mode=ceil_mode,
            dilations=dilations,
            kernel_shape=kernel_shape,
            p=p,
            pads=pads,
            strides=strides,
        )

    def _lp_pool(  # type: ignore
        self,
        x,
        auto_pad,
        ceil_mode,
        dilations,
        kernel_shape,
        p,
        pads,
        strides,
    ):
        if pads is None:
            pads = [0 for i in range(len(kernel_shape) * 2)]
        if strides is None:
            strides = [1 for i in range(len(kernel_shape))]
        if dilations is None:
            dilations = [1 for i in range(len(kernel_shape))]

        n_dims = len(kernel_shape)
        new_pads = np.array([(pads[i], pads[i + n_dims]) for i in range(n_dims)])

        input_spatial_shape = x.shape[2:]
        output_spatial_shape = [0 for s in input_spatial_shape]
        if ceil_mode:
            for i in range(len(input_spatial_shape)):
                output_spatial_shape[i] = int(
                    np.ceil(
                        (
                            input_spatial_shape[i]
                            + new_pads[i].sum()
                            - ((kernel_shape[i] - 1) * dilations[i] + 1)
                        )
                        / strides[i]
                        + 1
                    )
                )
        else:
            for i in range(len(input_spatial_shape)):
                output_spatial_shape[i] = int(
                    np.floor(
                        (
                            input_spatial_shape[i]
                            + new_pads[i].sum()
                            - ((kernel_shape[i] - 1) * dilations[i] + 1)
                        )
                        / strides[i]
                        + 1
                    )
                )

        if auto_pad and auto_pad != "NOTSET":
            # Deprecated attribute
            if auto_pad in ("SAME_UPPER", "SAME_LOWER"):
                for i in range(len(input_spatial_shape)):
                    if auto_pad == "SAME_UPPER":
                        output_spatial_shape[i] = int(
                            np.ceil(input_spatial_shape[i] / strides[i])
                        )
                    else:
                        output_spatial_shape[i] = int(
                            np.floor(input_spatial_shape[i] / strides[i])
                        )
                    pad_i = (
                        (output_spatial_shape[i] - 1) * strides[i]
                        + ((kernel_shape[i] - 1) * dilations[i] + 1)
                        - input_spatial_shape[i]
                    )
                    new_pads[i, 0] = pad_i // 2
                    new_pads[i, 1] = pad_i - new_pads[i, 0]
            else:
                for i in range(len(input_spatial_shape)):
                    output_spatial_shape[i] = int(
                        np.ceil(
                            (
                                input_spatial_shape[i]
                                - ((kernel_shape[i] - 1) * dilations[i] + 1)
                                + 1
                            )
                            / strides[i]
                        )
                    )

        if len(input_spatial_shape) == 1:
            return self._lp_pool_1d(
                x,
                auto_pad,
                ceil_mode,
                dilations,
                kernel_shape,
                p,
                new_pads,
                strides,
                output_spatial_shape,
            )

        if len(input_spatial_shape) == 2:
            return self._lp_pool_2d(
                x,
                auto_pad,
                ceil_mode,
                dilations,
                kernel_shape,
                p,
                new_pads,
                strides,
                output_spatial_shape,
            )

        if len(input_spatial_shape) == 3:
            return self._lp_pool_3d(
                x,
                auto_pad,
                ceil_mode,
                dilations,
                kernel_shape,
                p,
                new_pads,
                strides,
                output_spatial_shape,
            )

        raise RuntimeError(f"Not implemented yet for shape {x.shape}.")

    def _lp_pool_1d(  # type: ignore
        self,
        x,
        auto_pad,  # pylint: disable=W0613
        ceil_mode,  # pylint: disable=W0613
        dilations,
        kernel_shape,
        p,
        new_pads,
        strides,
        output_spatial_shape,
    ):

        global_pooling = False
        y_dims = x.shape[:2] + tuple(output_spatial_shape)
        y = np.zeros(y_dims, dtype=x.dtype)
        x_dims = x.shape
        channels = x_dims[1]
        height = x_dims[2]
        pooled_height = y_dims[2]
        total_channels = x_dims[0] * channels
        stride_h = 1 if global_pooling else strides[0]

        x_step = height
        y_step = pooled_height
        dilation_h = dilations[0]

        X_data = x.ravel()
        Y_data = y.ravel()
        inv_p = 1 / p

        def iteration(c):
            x_d = c * x_step
            y_d = c * y_step
            for ph in range(pooled_height):
                hstart = ph * stride_h - new_pads[0, 0]
                hend = hstart + kernel_shape[0] * dilation_h
                Yh = 0
                for h in range(hstart, hend, dilation_h):
                    if h < 0 or h >= height:
                        continue
                    Yh += X_data[x_d + h] ** p
                Y_data[y_d + ph] = Yh**inv_p

        for c in range(total_channels):
            iteration(c)

        return (Y_data.reshape(y_dims),)

    def _lp_pool_2d(  # type: ignore
        self,
        x,
        auto_pad,  # pylint: disable=W0613
        ceil_mode,  # pylint: disable=W0613
        dilations,
        kernel_shape,
        p,
        new_pads,
        strides,
        output_spatial_shape,
    ):

        global_pooling = False
        y_dims = x.shape[:2] + tuple(output_spatial_shape)
        y = np.zeros(y_dims, dtype=x.dtype)
        x_dims = x.shape
        channels = x_dims[1]
        height = x_dims[2]
        width = x_dims[3] if len(kernel_shape) > 1 else 1
        pooled_height = y_dims[2]
        pooled_width = y_dims[3] if len(kernel_shape) > 1 else 1
        total_channels = x_dims[0] * channels
        stride_h = 1 if global_pooling else strides[0]
        stride_w = 1 if global_pooling else strides[1]

        x_step = height * width
        y_step = pooled_height * pooled_width
        dilation_h = dilations[0]
        dilation_w = dilations[1]

        X_data = x.ravel()
        Y_data = y.ravel()
        inv_p = 1 / p

        def iteration(c):  # type: ignore
            x_d = c * x_step  # X_data
            y_d = c * y_step  # Y_data
            for ph in range(pooled_height):
                hstart = ph * stride_h - new_pads[0, 0]
                hend = hstart + kernel_shape[0] * dilation_h
                for pw in range(pooled_width):
                    wstart = pw * stride_w - new_pads[1, 0]
                    wend = wstart + kernel_shape[1] * dilation_w
                    pool_index = ph * pooled_width + pw
                    Yh = 0
                    for h in range(hstart, hend, dilation_h):
                        if h < 0 or h >= height:
                            continue
                        for w in range(wstart, wend, dilation_w):
                            if w < 0 or w >= width:
                                continue
                            input_index = h * width + w
                            if input_index < 0 or input_index > X_data.shape[0]:
                                continue
                            Yh += X_data[x_d + input_index] ** p
                    Y_data[y_d + pool_index] = Yh**inv_p

        for c in range(total_channels):
            iteration(c)

        return (Y_data.reshape(y_dims),)

    def _lp_pool_3d(  # type: ignore
        self,
        x,
        auto_pad,  # pylint: disable=W0613
        ceil_mode,  # pylint: disable=W0613
        dilations,
        kernel_shape,
        p,
        new_pads,
        strides,
        output_spatial_shape,
    ):

        global_pooling = False
        y_dims = x.shape[:2] + tuple(output_spatial_shape)
        y = np.zeros(y_dims, dtype=x.dtype)
        x_dims = x.shape
        channels = x_dims[1]
        height = x_dims[2]
        width = x_dims[3] if len(kernel_shape) > 1 else 1
        depth = x_dims[4] if len(kernel_shape) > 2 else 1
        pooled_height = y_dims[2]
        pooled_width = y_dims[3] if len(kernel_shape) > 1 else 1
        pooled_depth = y_dims[4] if len(kernel_shape) > 2 else 1
        total_channels = x_dims[0] * channels
        stride_h = 1 if global_pooling else strides[0]
        stride_w = 1 if global_pooling else strides[1]
        stride_d = 1 if global_pooling else strides[2]

        x_step = height * width * depth
        y_step = pooled_height * pooled_width * pooled_depth
        dilation_h = dilations[0]
        dilation_w = dilations[1]
        dilation_d = dilations[2]

        X_data = x.ravel()
        Y_data = y.ravel()
        inv_p = 1 / p

        def iteration(c):
            x_d = c * x_step
            y_d = c * y_step

            for ph in range(pooled_height):
                hstart = ph * stride_h - new_pads[0, 0]
                hend = hstart + kernel_shape[0] * dilation_h
                for pw in range(pooled_width):
                    wstart = pw * stride_w - new_pads[1, 0]
                    wend = wstart + kernel_shape[1] * dilation_w
                    for pd in range(pooled_depth):
                        dstart = pd * stride_d - new_pads[2, 0]
                        dend = dstart + kernel_shape[2] * dilation_d
                        pool_index = (
                            ph * pooled_width * pooled_depth + pw * pooled_depth + pd
                        )
                        Yh = 0
                        for h in range(hstart, hend, dilation_h):
                            if h < 0 or h >= height:
                                continue
                            for w in range(wstart, wend, dilation_w):
                                if w < 0 or w >= width:
                                    continue
                                for d in range(dstart, dend, dilation_d):
                                    if d < 0 or d >= depth:
                                        continue
                                    input_index = h * width * depth + w * depth + d
                                    Yh += X_data[x_d + input_index] ** p

                        Y_data[y_d + pool_index] = Yh**inv_p

        for c in range(total_channels):
            iteration(c)

        return (Y_data.reshape(y_dims),)
