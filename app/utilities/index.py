import random

COLORS = [
    "#50b500",  # Green
    "#007bff",  # Blue
    "#f763a2",  # Pink
    "#ffbb00",  # Yellow
    "#34a853",  # Green
    "#ff5722",  # Orange
    "#8e44ad",  # Purple
    "#f39c12",  # Yellow
    "#e74c3c",  # Red
    "#3498db",  # Blue
    "#1abc9c",  # Teal
    "#f1c40f",  # Yellow
]


def get_random_color():
    return random.choice(COLORS)
