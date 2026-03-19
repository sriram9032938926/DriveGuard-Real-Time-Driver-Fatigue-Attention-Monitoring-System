import numpy as np
import cv2

NOSE_TIP = 1
CHIN = 152
LEFT_EYE_IDX = 33
RIGHT_EYE_IDX = 263
LEFT_MOUTH_IDX = 61
RIGHT_MOUTH_IDX = 291


def get_head_pose(landmarks, frame_w, frame_h):
    image_points = np.array([
        (landmarks[NOSE_TIP].x * frame_w, landmarks[NOSE_TIP].y * frame_h),
        (landmarks[CHIN].x * frame_w, landmarks[CHIN].y * frame_h),
        (landmarks[LEFT_EYE_IDX].x * frame_w, landmarks[LEFT_EYE_IDX].y * frame_h),
        (landmarks[RIGHT_EYE_IDX].x * frame_w, landmarks[RIGHT_EYE_IDX].y * frame_h),
        (landmarks[LEFT_MOUTH_IDX].x * frame_w, landmarks[LEFT_MOUTH_IDX].y * frame_h),
        (landmarks[RIGHT_MOUTH_IDX].x * frame_w, landmarks[RIGHT_MOUTH_IDX].y * frame_h),
    ], dtype="double")

    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -63.6, -12.5),
        (-43.3, 32.7, -26.0),
        (43.3, 32.7, -26.0),
        (-28.9, -28.9, -24.1),
        (28.9, -28.9, -24.1),
    ])

    focal_length = frame_w
    center = (frame_w / 2, frame_h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vec, translation_vec = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE,
    )

    if not success:
        return 0.0, 0.0, 0.0

    rmat, _ = cv2.Rodrigues(rotation_vec)
    angles, *_ = cv2.RQDecomp3x3(rmat)
    pitch, yaw, roll = angles
    return float(pitch), float(yaw), float(roll)