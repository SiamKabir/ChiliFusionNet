from pathlib import Path

import cv2
import numpy as np

from tensorflow.keras.applications.inception_resnet_v2 import (
    preprocess_input as preprocess_irv2
)

from tensorflow.keras.applications.efficientnet import (
    preprocess_input as preprocess_effnet
)

from tensorflow.keras.applications.xception import (
    preprocess_input as preprocess_xception
)

IMG_SIZE = (224, 224)
RESIZE_INTERPOLATION = cv2.INTER_LINEAR

CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_GRID_SIZE = (8, 8)

GAMMA = 1.1

GAUSSIAN_KERNEL = (3, 3)
GAUSSIAN_SIGMA = 0

SHARPEN_ALPHA = 0.5
_g = cv2.getGaussianKernel(3, GAUSSIAN_SIGMA)
SHARPEN_KERNEL = -SHARPEN_ALPHA * (_g @ _g.T).astype(np.float32)
SHARPEN_KERNEL[1, 1] += 1.0 + SHARPEN_ALPHA

DENOISE_H = 10
DENOISE_H_COLOR = 10
DENOISE_TEMPLATE_WINDOW = 7
DENOISE_SEARCH_WINDOW = 21

GAMMA_LUT = np.array(
    [
        np.clip(
            ((i / 255.0) ** (1.0 / GAMMA)) * 255.0,
            0,
            255
        )
        for i in range(256)
    ],
    dtype=np.uint8
)


def enhance_image(image_bgr):

    if image_bgr is None:
        raise ValueError("Input image is None.")

    if image_bgr.dtype != np.uint8:
        raise ValueError("Expected uint8 image.")

    image_bgr = cv2.resize(
        image_bgr,
        IMG_SIZE,
        interpolation=RESIZE_INTERPOLATION
    )

    image_lab = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2LAB
    )

    l_channel, a_channel, b_channel = cv2.split(
        image_lab
    )

    clahe = cv2.createCLAHE(
        clipLimit=CLAHE_CLIP_LIMIT,
        tileGridSize=CLAHE_TILE_GRID_SIZE
    )

    l_channel = clahe.apply(l_channel)

    image_lab = cv2.merge(
        [l_channel, a_channel, b_channel]
    )

    image_bgr = cv2.cvtColor(
        image_lab,
        cv2.COLOR_LAB2BGR
    )

    image_bgr = cv2.LUT(
        image_bgr,
        GAMMA_LUT
    )

    image_bgr = cv2.GaussianBlur(
        image_bgr,
        GAUSSIAN_KERNEL,
        sigmaX=GAUSSIAN_SIGMA
    )

    image_bgr = cv2.filter2D(
        image_bgr,
        ddepth=-1,
        kernel=SHARPEN_KERNEL
    )

    image_bgr = cv2.fastNlMeansDenoisingColored(
        image_bgr,
        None,
        DENOISE_H,
        DENOISE_H_COLOR,
        DENOISE_TEMPLATE_WINDOW,
        DENOISE_SEARCH_WINDOW
    )

    image_rgb = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2RGB
    )

    return image_rgb

def load_image(filepath):

    filepath = Path(filepath)

    if not filepath.is_file():
        raise FileNotFoundError(
            f"Image not found: {filepath}"
        )

    image_bgr = cv2.imread(
        str(filepath),
        cv2.IMREAD_COLOR
    )

    if image_bgr is None:
        raise ValueError(
            f"Unable to decode image: {filepath}"
        )

    image_rgb = enhance_image(image_bgr)

    return image_rgb.astype(np.float32)

PREPROCESS_FUNCTIONS = {
    "InceptionResNetV2": preprocess_irv2,
    "EfficientNetB3": preprocess_effnet,
    "Xception": preprocess_xception
}


def preprocess_for_backbone(images, backbone_name):

    if backbone_name not in PREPROCESS_FUNCTIONS:
        raise ValueError(
            f"Unsupported backbone: {backbone_name}"
        )

    images = np.asarray(
        images,
        dtype=np.float32
    )

    if images.ndim != 4 or images.shape[1:] != (
        224, 224, 3
    ):
        raise ValueError(
            "Expected shape (N, 224, 224, 3)."
        )

    return PREPROCESS_FUNCTIONS[
        backbone_name
    ](images.copy())

TEST_IMAGE = None

if TEST_IMAGE is not None:
    sample = load_image(TEST_IMAGE)
    print("Enhanced image:", sample.shape, sample.dtype,
          "range", float(sample.min()), "-", float(sample.max()))

    batch = sample[np.newaxis]
    for name in PREPROCESS_FUNCTIONS:
        out = preprocess_for_backbone(batch, name)
        print(f"{name:18s}: min {out.min():8.3f}  max {out.max():8.3f}")