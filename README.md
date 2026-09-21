# 3D Point Cloud Trajectory Tracker

A concise processing pipeline that extracts 3D object trajectories by fusing 2D bounding box detections with 3D depth point cloud arrays (`.npz`).

---

## Methodology

1. **Target Center & Noise Removal**:
   * Calculates the 2D pixel center $(u, v)$ from bounding box bounds in `bbox_light.csv`.
   * Replaces invalid depth values (`NaN`, `+Inf`, `-Inf`) in raw `.npz` point cloud arrays with zero vectors.

2. **Coordinate Transformation & Mapping**:
   * Establishes the first valid detection as the relative origin $(0,0)$.
   * Remaps camera space to world displacement:
     * **Lateral Shift ($X_{world}$)**: Mapped from sensor $Y$-axis displacement ($Y_{frame} - Y_{base}$).
     * **Forward Progress ($Y_{world}$)**: Mapped from inverted sensor $X$-axis displacement ($X_{base} - X_{frame}$).

---

## Assumptions

* **Spatial Alignment**: 2D bounding box pixel coordinates in `bbox_light.csv` directly align with the array dimensions of `.npz` depth frames.
* **Relative Origin**: Object motion is measured relative to the sensor’s initial detection frame rather than external global GPS/SLAM coordinates.

---

## Results

* **Noise Reduction**: Patch-based median filtering removes trajectory spikes caused by edge noise or empty depth pixels.
* **Displacement Tracking**: Converts raw array depth indices into real-world meter metrics ($x_m, y_m, z_m$).
* **Artifact Generation**: Outputs formatted frame-by-frame console metrics and saves a 2D spatial path plot (`trajectory.png`).
