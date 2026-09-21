import numpy as np
import matplotlib.pyplot as plt
import cv2

FRAME_PATH = "./Data/Depth/xyz/depth"
CSV_PATH = 'Data/bbox_light.csv'

def avg(A : int, B : int) -> int:
    return ((A + B) // 2)

def Center_From_Cords(Cords) -> tuple[int, int]:
    return avg(Cords[0], Cords[2]), avg(Cords[1], Cords[3])


def Get_File_Path(Frame: int) -> str:
    return f"{FRAME_PATH}{Frame:06d}.npz"

def Frame_Anyalsis(Frame : int, CenterCords : tuple[int, int]) -> tuple[float,float,float]:
    xyz_loaded = np.load(Get_File_Path(Frame))
    xyz_loaded_clean = np.nan_to_num(xyz_loaded["xyz"], nan=0.0, posinf=0.0, neginf=0.0)
        
    u, v = CenterCords[0], CenterCords[1]
    patch = xyz_loaded_clean[max(0, v-2):v+3, max(0, u-2):u+3, :3]
    valid_points = patch[patch[:, :, 0] > 0]
        
    if len(valid_points) > 0:
        X, Y, Z = np.median(valid_points, axis=0)
    else:
        X, Y, Z = xyz_loaded_clean[v, u][:3]

    print(f"X : {X}, Y : {Y}, Z : {Z}")
    return X, Y, Z

    



Postion_Data = np.zeros((299,4)) #Frame, X_m, Y_m, Z_m
Light_Box_Data = np.genfromtxt(CSV_PATH, delimiter=',', skip_header=1, dtype=np.int16)


for Cords in Light_Box_Data:
    Frame_Number = Cords[0]
    Postion_Data[Frame_Number] = Frame_Number,*Frame_Anyalsis(Frame_Number,Center_From_Cords(Cords[1:5]))

Postion_Data = Postion_Data[Postion_Data[:, 1] != 0]
Base_Postion = Postion_Data[0]
Trajectory_Data = np.zeros((len(Postion_Data),4))

for i,Cords in enumerate(Postion_Data):
    # X = Lateral Shift (starts at 0, ends near 0)
    # Y = Forward Progress (starts at 0, tops out under 14m)
    Trajectory_Data[i] = Cords[0], Cords[2] - Base_Postion[2], Base_Postion[1] - Cords[1], Cords[3]



print("Trajectory_Data:", Trajectory_Data)

for frame, Cords in enumerate(Trajectory_Data):
     print(f"Frame {int(Cords[0])}: x_m = {Cords[1]:.2f}m, y_m = {Cords[2]:.2f}m, z_m = {Cords[3]:.2f}m")

x = Trajectory_Data[:, 1]
y = Trajectory_Data[:, 2]

plt.figure(figsize=(8, 6))
plt.scatter(x, y, color="blue", alpha=0.6)
plt.plot(x, y, color="blue", linestyle="--", alpha=0.3)

# Start (Circle) and Finish (Star)
plt.scatter(x[0], y[0], color="green", marker="o", s=150, zorder=5)
plt.scatter(x[-1], y[-1], color="gold", marker="*", s=250, zorder=5)

plt.title("2D Array Coordinate Plot")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.axis("equal")
plt.grid(True)
plt.savefig("trajectory.png")
plt.show()
