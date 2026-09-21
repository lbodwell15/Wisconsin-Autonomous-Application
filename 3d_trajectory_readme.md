# 3D Point Cloud Trajectory Tracker

A concise processing pipeline that extracts 3D object trajectories by fusing 2D bounding box detections with 3D depth point cloud arrays (`.npz`).

---

## Methodology

1. **Target Center & Noise Removal**:
   * Calculates the 2D pixel center $(u, v)$ from bounding box bounds in `bbox_light.csv`.
   * Replaces invalid depth values (`NaN`, `+Inf`, `-Inf`) in raw `.npz` point cloud arrays with zero vectors.

2. **Spatial Patch & Median Filtering**:
   * Samples a $5 \times 5$ pixel patch centered at $(u, v)$ to prevent single-pixel depth noise or missing values.
   * Filters for points where $X > 0$ and computes the spatial median coordinate $(X, Y, Z)$ across valid neighborhood returns.

3. **Coordinate Transformation & Mapping**:
   * Establishes the first valid detection as the relative origin $(0,0)$.
   * Remaps camera space to world displacement:
     * **Lateral Shift ($X_{world}$)**: Mapped from sensor $Y$-axis displacement ($Y_{frame} - Y_{base}$).
     * **Forward Progress ($Y_{world}$)**: Mapped from inverted sensor $X$-axis displacement ($X_{base} - X_{frame}$).

---

## Assumptions

* **Spatial Alignment**: 2D bounding box pixel coordinates in `bbox_light.csv` directly align with the array dimensions of `.npz` depth frames.
* **Valid Depth Returns**: Target points possess positive values along the depth axis ($X > 0$), and the $5 \times 5$ patch primarily covers the target object.
* **Relative Origin**: Object motion is measured relative to the sensor’s initial detection frame rather than external global GPS/SLAM coordinates.

---

## Results

* **Noise Reduction**: Patch-based median filtering removes trajectory spikes caused by edge noise or empty depth pixels.
* **Displacement Tracking**: Converts raw array depth indices into real-world meter metrics ($x_m, y_m, z_m$).
* **Motion Profile**: Accurately tracks forward progress topping out under $14\text{ m}$ along $Y_{world}$ with minimal lateral drift near $0\text{ m}$ along $X_{world}$.
* **Artifact Generation**: Outputs formatted frame-by-frame console metrics and saves a 2D spatial path plot (`trajectory.png`).