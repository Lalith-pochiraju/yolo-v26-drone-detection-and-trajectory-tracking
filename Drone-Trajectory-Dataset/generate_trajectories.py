import numpy as np
import pandas as pd
import random

np.random.seed(42)
random.seed(42)

NUM_TRAJECTORIES = 1000
MIN_LENGTH = 80
MAX_LENGTH = 120

trajectories = []


def noise(x, y):
    return (
        x + np.random.normal(0, 0.005),
        y + np.random.normal(0, 0.005)
    )


def hover(length):
    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)

    pts = []

    for _ in range(length):
        x, y = noise(x, y)
        pts.append((x, y))

    return pts


def straight(length):

    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)

    theta = np.random.uniform(0, 2 * np.pi)

    speed = np.random.uniform(0.015, 0.03)

    pts = []

    for _ in range(length):

        x += speed * np.cos(theta)
        y += speed * np.sin(theta)

        x, y = noise(x, y)

        pts.append((x, y))

    return pts


def circle(length):

    r = np.random.uniform(0.2, 0.7)

    cx = np.random.uniform(-1, 1)
    cy = np.random.uniform(-1, 1)

    pts = []

    for i in range(length):

        t = 4 * np.pi * i / length

        x = cx + r * np.cos(t)
        y = cy + r * np.sin(t)

        x, y = noise(x, y)

        pts.append((x, y))

    return pts


def patrol(length):

    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)

    pts = []

    target = np.random.uniform(-1, 1, 2)

    for _ in range(length):

        dx = target[0] - x
        dy = target[1] - y

        d = np.sqrt(dx ** 2 + dy ** 2)

        if d < 0.1:
            target = np.random.uniform(-1, 1, 2)

        else:
            x += 0.03 * dx / d
            y += 0.03 * dy / d

        x, y = noise(x, y)

        pts.append((x, y))

    return pts


def zigzag(length):

    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)

    theta = np.random.uniform(0, 2 * np.pi)

    pts = []

    for i in range(length):

        if i % 15 == 0:
            theta += np.deg2rad(random.choice([-30, 30]))

        x += 0.025 * np.cos(theta)
        y += 0.025 * np.sin(theta)

        x, y = noise(x, y)

        pts.append((x, y))

    return pts


def evasive(length):

    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)

    theta = np.random.uniform(0, 2 * np.pi)

    pts = []

    for _ in range(length):

        if random.random() < 0.15:
            theta += np.deg2rad(random.uniform(-120, 120))

        speed = np.random.uniform(0.01, 0.04)

        x += speed * np.cos(theta)
        y += speed * np.sin(theta)

        x, y = noise(x, y)

        pts.append((x, y))

    return pts


def approach(length):

    start = np.random.uniform(-1, 1, 2)

    target = np.random.uniform(-1, 1, 2)

    x, y = start

    pts = []

    for _ in range(length):

        dx = target[0] - x
        dy = target[1] - y

        d = np.sqrt(dx ** 2 + dy ** 2)

        if d > 0.02:
            x += 0.03 * dx / d
            y += 0.03 * dy / d

        x, y = noise(x, y)

        pts.append((x, y))

    return pts


motions = {
    "hover": hover,
    "straight": straight,
    "circle": circle,
    "patrol": patrol,
    "zigzag": zigzag,
    "evasive": evasive,
    "approach": approach
}

for tid in range(NUM_TRAJECTORIES):

    motion = random.choice(list(motions.keys()))

    length = random.randint(MIN_LENGTH, MAX_LENGTH)

    path = motions[motion](length)

    for frame, (x, y) in enumerate(path):

        trajectories.append({
            "trajectory_id": tid,
            "frame": frame,
            "motion": motion,
            "x": x,
            "y": y
        })

df = pd.DataFrame(trajectories)

df.to_csv("synthetic_drone_trajectories.csv", index=False)

print(df.head())

print("\nSaved synthetic_drone_trajectories.csv")