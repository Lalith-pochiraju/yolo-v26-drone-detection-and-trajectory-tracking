import pandas as pd
import numpy as np

Tp = 8
Tf = 12

df = pd.read_csv("synthetic_drone_trajectories.csv")

X = []
Y = []

for traj_id in df["trajectory_id"].unique():

    traj = df[df["trajectory_id"] == traj_id]

    traj = traj.sort_values("frame")

    coords = traj[["x", "y"]].values

    if len(coords) < Tp + Tf:
        continue

    for i in range(len(coords) - Tp - Tf + 1):

        past = coords[i:i + Tp]

        future = coords[i + Tp:i + Tp + Tf]

        X.append(past)

        Y.append(future)

X = np.array(X)

Y = np.array(Y)

print("Past shape :", X.shape)
print("Future shape:", Y.shape)

np.save("X.npy", X)
np.save("Y.npy", Y)

print("\nSaved X.npy")
print("Saved Y.npy")