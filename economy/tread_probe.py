"""What do linear treadmill tiers (x1 x2 x4 x6 x8 x10 = 50K/s x mult) do to the v5 progression on the CURRENT walk curve?"""
import random, statistics
import pacing_model as pm
import v5_model as v
FINAL = [40e3, 2e6, 5.5e6, 25e6, 125e6, 800e6, 1.8e9, 4e9, 20e9, 50e9, 80e9, 250e9, 900e9, 1.5e12, 2.25e12, 3.5e12, 5e12, 6.5e12, 9e12, 14e12]
lad = [[c, a, k] for c, (_, a, k) in zip(FINAL, pm.LADDER)]
prices = [p for p, _ in pm.TREADMILL]
pm.TREADMILL = [(p, 50_000 * m) for p, m in zip(prices, [1, 2, 4, 6, 8, 10])]
print("treadmill:", pm.TREADMILL)
v.report(lad, seeds=30)
