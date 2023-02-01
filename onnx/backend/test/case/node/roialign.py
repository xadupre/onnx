# SPDX-License-Identifier: Apache-2.0

import numpy as np

import onnx

from ..base import Base
from . import expect


def get_roi_align_input_values():  # type: ignore
    X = np.array(
        [
            [
                [
                    [
                        0.2764,
                        0.7150,
                        0.1958,
                        0.3416,
                        0.4638,
                        0.0259,
                        0.2963,
                        0.6518,
                        0.4856,
                        0.7250,
                    ],
                    [
                        0.9637,
                        0.0895,
                        0.2919,
                        0.6753,
                        0.0234,
                        0.6132,
                        0.8085,
                        0.5324,
                        0.8992,
                        0.4467,
                    ],
                    [
                        0.3265,
                        0.8479,
                        0.9698,
                        0.2471,
                        0.9336,
                        0.1878,
                        0.4766,
                        0.4308,
                        0.3400,
                        0.2162,
                    ],
                    [
                        0.0206,
                        0.1720,
                        0.2155,
                        0.4394,
                        0.0653,
                        0.3406,
                        0.7724,
                        0.3921,
                        0.2541,
                        0.5799,
                    ],
                    [
                        0.4062,
                        0.2194,
                        0.4473,
                        0.4687,
                        0.7109,
                        0.9327,
                        0.9815,
                        0.6320,
                        0.1728,
                        0.6119,
                    ],
                    [
                        0.3097,
                        0.1283,
                        0.4984,
                        0.5068,
                        0.4279,
                        0.0173,
                        0.4388,
                        0.0430,
                        0.4671,
                        0.7119,
                    ],
                    [
                        0.1011,
                        0.8477,
                        0.4726,
                        0.1777,
                        0.9923,
                        0.4042,
                        0.1869,
                        0.7795,
                        0.9946,
                        0.9689,
                    ],
                    [
                        0.1366,
                        0.3671,
                        0.7011,
                        0.6234,
                        0.9867,
                        0.5585,
                        0.6985,
                        0.5609,
                        0.8788,
                        0.9928,
                    ],
                    [
                        0.5697,
                        0.8511,
                        0.6711,
                        0.9406,
                        0.8751,
                        0.7496,
                        0.1650,
                        0.1049,
                        0.1559,
                        0.2514,
                    ],
                    [
                        0.7012,
                        0.4056,
                        0.7879,
                        0.3461,
                        0.0415,
                        0.2998,
                        0.5094,
                        0.3727,
                        0.5482,
                        0.0502,
                    ],
                ]
            ]
        ],
        dtype=np.float32,
    )
    batch_indices = np.array([0, 0, 0], dtype=np.int64)
    rois = np.array([[0, 0, 9, 9], [0, 5, 4, 9], [5, 5, 9, 9]], dtype=np.float32)
    return X, batch_indices, rois


class RoiAlign(Base):
    @staticmethod
    def export_roialign_aligned_false() -> None:
        node = onnx.helper.make_node(
            "RoiAlign",
            inputs=["X", "rois", "batch_indices"],
            outputs=["Y"],
            spatial_scale=1.0,
            output_height=5,
            output_width=5,
            sampling_ratio=2,
            coordinate_transformation_mode="output_half_pixel",
        )

        X, batch_indices, rois = get_roi_align_input_values()
        # (num_rois, C, output_height, output_width)
        Y = np.array(
            [
                [
                    [
                        [0.4664, 0.4466, 0.3405, 0.5688, 0.6068],
                        [0.3714, 0.4296, 0.3835, 0.5562, 0.3510],
                        [0.2768, 0.4883, 0.5222, 0.5528, 0.4171],
                        [0.4713, 0.4844, 0.6904, 0.4920, 0.8774],
                        [0.6239, 0.7125, 0.6289, 0.3355, 0.3495],
                    ]
                ],
                [
                    [
                        [0.3022, 0.4305, 0.4696, 0.3978, 0.5423],
                        [0.3656, 0.7050, 0.5165, 0.3172, 0.7015],
                        [0.2912, 0.5059, 0.6476, 0.6235, 0.8299],
                        [0.5916, 0.7389, 0.7048, 0.8372, 0.8893],
                        [0.6227, 0.6153, 0.7097, 0.6154, 0.4585],
                    ]
                ],
                [
                    [
                        [0.2384, 0.3379, 0.3717, 0.6100, 0.7601],
                        [0.3767, 0.3785, 0.7147, 0.9243, 0.9727],
                        [0.5749, 0.5826, 0.5709, 0.7619, 0.8770],
                        [0.5355, 0.2566, 0.2141, 0.2796, 0.3600],
                        [0.4365, 0.3504, 0.2887, 0.3661, 0.2349],
                    ]
                ],
            ],
            dtype=np.float32,
        )

        expect(
            node,
            inputs=[X, rois, batch_indices],
            outputs=[Y],
            name="test_roialign_aligned_false",
        )

    @staticmethod
    def export_roialign_aligned_true() -> None:
        node = onnx.helper.make_node(
            "RoiAlign",
            inputs=["X", "rois", "batch_indices"],
            outputs=["Y"],
            spatial_scale=1.0,
            output_height=5,
            output_width=5,
            sampling_ratio=2,
            coordinate_transformation_mode="half_pixel",
        )

        X, batch_indices, rois = get_roi_align_input_values()
        # (num_rois, C, output_height, output_width)
        Y = np.array(
            [
                [
                    [
                        [0.5178, 0.3434, 0.3229, 0.4474, 0.6344],
                        [0.4031, 0.5366, 0.4428, 0.4861, 0.4023],
                        [0.2512, 0.4002, 0.5155, 0.6954, 0.3465],
                        [0.3350, 0.4601, 0.5881, 0.3439, 0.6849],
                        [0.4932, 0.7141, 0.8217, 0.4719, 0.4039],
                    ]
                ],
                [
                    [
                        [0.3070, 0.2187, 0.3337, 0.4880, 0.4870],
                        [0.1871, 0.4914, 0.5561, 0.4192, 0.3686],
                        [0.1433, 0.4608, 0.5971, 0.5310, 0.4982],
                        [0.2788, 0.4386, 0.6022, 0.7000, 0.7524],
                        [0.5774, 0.7024, 0.7251, 0.7338, 0.8163],
                    ]
                ],
                [
                    [
                        [0.2393, 0.4075, 0.3379, 0.2525, 0.4743],
                        [0.3671, 0.2702, 0.4105, 0.6419, 0.8308],
                        [0.5556, 0.4543, 0.5564, 0.7502, 0.9300],
                        [0.6626, 0.5617, 0.4813, 0.4954, 0.6663],
                        [0.6636, 0.3721, 0.2056, 0.1928, 0.2478],
                    ]
                ],
            ],
            dtype=np.float32,
        )

        expect(
            node,
            inputs=[X, rois, batch_indices],
            outputs=[Y],
            name="test_roialign_aligned_true",
        )

    @staticmethod
    def export_roialign_mode_max() -> None:
        X = np.array(
            [
                [
                    [
                        [
                            0.2764,
                            0.715,
                            0.1958,
                            0.3416,
                            0.4638,
                            0.0259,
                            0.2963,
                            0.6518,
                            0.4856,
                            0.725,
                        ],
                        [
                            0.9637,
                            0.0895,
                            0.2919,
                            0.6753,
                            0.0234,
                            0.6132,
                            0.8085,
                            0.5324,
                            0.8992,
                            0.4467,
                        ],
                        [
                            0.3265,
                            0.8479,
                            0.9698,
                            0.2471,
                            0.9336,
                            0.1878,
                            0.4766,
                            0.4308,
                            0.34,
                            0.2162,
                        ],
                        [
                            0.0206,
                            0.172,
                            0.2155,
                            0.4394,
                            0.0653,
                            0.3406,
                            0.7724,
                            0.3921,
                            0.2541,
                            0.5799,
                        ],
                        [
                            0.4062,
                            0.2194,
                            0.4473,
                            0.4687,
                            0.7109,
                            0.9327,
                            0.9815,
                            0.632,
                            0.1728,
                            0.6119,
                        ],
                        [
                            0.3097,
                            0.1283,
                            0.4984,
                            0.5068,
                            0.4279,
                            0.0173,
                            0.4388,
                            0.043,
                            0.4671,
                            0.7119,
                        ],
                        [
                            0.1011,
                            0.8477,
                            0.4726,
                            0.1777,
                            0.9923,
                            0.4042,
                            0.1869,
                            0.7795,
                            0.9946,
                            0.9689,
                        ],
                        [
                            0.1366,
                            0.3671,
                            0.7011,
                            0.6234,
                            0.9867,
                            0.5585,
                            0.6985,
                            0.5609,
                            0.8788,
                            0.9928,
                        ],
                        [
                            0.5697,
                            0.8511,
                            0.6711,
                            0.9406,
                            0.8751,
                            0.7496,
                            0.165,
                            0.1049,
                            0.1559,
                            0.2514,
                        ],
                        [
                            0.7012,
                            0.4056,
                            0.7879,
                            0.3461,
                            0.0415,
                            0.2998,
                            0.5094,
                            0.3727,
                            0.5482,
                            0.0502,
                        ],
                    ]
                ]
            ],
            dtype=np.float32,
        )
        rois = np.array(
            [[0.0, 0.0, 9.0, 9.0], [0.0, 5.0, 4.0, 9.0], [5.0, 5.0, 9.0, 9.0]],
            dtype=np.float32,
        )
        batch_indices = np.array([0, 0, 0], dtype=np.int64)

        Y = np.array(
            [
                [
                    [
                        [0.3445228, 0.37310338, 0.37865096, 0.446696, 0.37991184],
                        [0.4133513, 0.5455125, 0.6651902, 0.55805874, 0.27110294],
                        [0.21223956, 0.40924096, 0.8417618, 0.792561, 0.37196714],
                        [0.46835402, 0.39741728, 0.8012819, 0.4969306, 0.5495158],
                        [0.3595896, 0.5196813, 0.5403741, 0.23814403, 0.19992709],
                    ]
                ],
                [
                    [
                        [0.30517197, 0.5086199, 0.3189761, 0.4054401, 0.47630402],
                        [0.50862, 0.8477, 0.37808004, 0.24936005, 0.79384017],
                        [0.17620805, 0.29368007, 0.44870415, 0.4987201, 0.63148826],
                        [0.51066005, 0.8511, 0.5368801, 0.9406, 0.70008016],
                        [0.4487681, 0.51066035, 0.5042561, 0.5643603, 0.42004836],
                    ]
                ],
                [
                    [
                        [0.21062402, 0.3510401, 0.37416005, 0.5967599, 0.46507207],
                        [0.32336006, 0.31180006, 0.6236001, 0.9946, 0.7751202],
                        [0.35744014, 0.5588001, 0.35897616, 0.7030401, 0.6353923],
                        [0.5996801, 0.27940005, 0.17948808, 0.35152006, 0.31769615],
                        [0.3598083, 0.40752012, 0.2385281, 0.43856013, 0.26313624],
                    ]
                ],
            ],
            dtype=np.float32,
        )

        node = onnx.helper.make_node(
            "RoiAlign",
            inputs=["X", "rois", "batch_indices"],
            mode="max",
            outputs=["Y"],
            spatial_scale=1.0,
            output_height=5,
            output_width=5,
            coordinate_transformation_mode="output_half_pixel",
        )

        expect(
            node,
            inputs=[X, rois, batch_indices],
            outputs=[Y],
            name="test_roialign_mode_max",
        )
