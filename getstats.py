#!/usr/bin/env python3
import requests
import sys
import time
import os


def pretty_num(num):
    """Convert a number to a human-readable format with SI suffixed."""
    units = [(1e15, "P"), (1e12, "T"), (1e9, "G"), (1e6, "M"), (1e3, "K")]
    for size, unit in units:
        if num > size:
            return f"{round(num/size, 1)}{unit}"
    return f"{num}"


INTERVAL = 0.5

last_stats = {}

while True:
    stats = None
    while not stats:
        try:
            stats = requests.get(f"{sys.argv[1]}/stats.json").json()
        except requests.exceptions.ConnectionError:
            time.sleep(10)
    connections = stats.get("PixelFlutConnections", 0)
    bytes_recv = stats.get("ReceivedBytes", 0)
    pixels_recv = stats.get("ReceivedPixels", 0)
    pixels_sent = stats.get("SentPixels", 0)
    last_bytes_recv = last_stats.get("ReceivedBytes", 0)
    last_pixels_recv = last_stats.get("ReceivedPixels", 0)
    last_pixels_sent = last_stats.get("SentPixels", 0)
    bytes_recv_per_sec = (bytes_recv - last_bytes_recv) / INTERVAL
    pixels_recv_per_sec = (pixels_recv - last_pixels_recv) / INTERVAL
    pixels_sent_per_sec = (pixels_sent - last_pixels_sent) / INTERVAL
    os.system("clear")
    print(f"Current Connections: {pretty_num(connections)}")
    print(
        f"Bytes received: {pretty_num(bytes_recv)} total, {pretty_num(bytes_recv_per_sec)} per second"
    )
    print(
        f"Pixels received: {pretty_num(pixels_recv)} total, {pretty_num(pixels_recv_per_sec)} per second"
    )
    print(
        f"Pixels sent: {pretty_num(pixels_sent)} total, {pretty_num(pixels_sent_per_sec)} per second"
    )
    last_stats = stats
    time.sleep(INTERVAL)
