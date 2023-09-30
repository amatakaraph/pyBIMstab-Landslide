

from numpy import array
from pybimstab.slope import NaturalSlope
from pybimstab.watertable import WaterTable
from pybimstab.bim import BlocksInMatrix
from pybimstab.slipsurface import CircularSurface, TortuousSurface
from pybimstab.slices import MaterialParameters, Slices
from pybimstab.slopestabl import SlopeStabl
terrainCoords = array(
    [[0.00, 2.28, 5.86, 8.49, 10.98, 
      14.28, 17.38, 20.41, 23.04, 26.28, 
      29.71, 32.14, 35.51, 39.89, 43.80, 
      47.57, 50.74, 54.71, 57.81, 62.73, 
      67.04, 71.02, 75.54, 80.12, 84.70, 
      90.09, 94.81, 97.77, 100.06, 103.43, 
      106.13, 108.42, 111.18, 115.02, 119.13, 
      123.38, 126.34, 129.58, 137.53, 137.53],
     [104.67, 104.49, 104.49, 103.34, 102.11, 
      101.22, 100.61, 100.16, 98.57, 96.63, 
      96.72, 97.25, 96.63, 95.48, 93.72, 
      92.30, 91.15, 90.18, 89.39, 86.47, 
      83.47, 80.56, 78.08, 75.43, 72.34, 
      68.63, 65.45, 63.51, 62.98, 61.21, 
      59.53, 58.83, 57.06, 55.82, 54.41, 
      53.97, 52.47, 50.52, 50, 50]])
slope = NaturalSlope(terrainCoords)
bim = BlocksInMatrix(slopeCoords=slope.coords, blockProp=0.17,
                     tileSize=0.2, seed=39)
watertabDepths = array([[0, 106.13, 126.34, 137.53],
                        [12, 16, 18, 20]])
watertable = WaterTable(slopeCoords=slope.coords,
                        watertabDepths=watertabDepths,
                        smoothFactor=2)
preferredPath = CircularSurface(
    slopeCoords=slope.coords, dist1=25,dist2=105, radius=50)
surface = TortuousSurface(
    bim, dist1=25,dist2=105, heuristic='euclidean',
    reverseLeft=False, reverseUp=False, smoothFactor=2,
    preferredPath=preferredPath.coords, prefPathFact=2)
material = MaterialParameters(
    cohesion=15, frictAngle=35, unitWeight=20,
    blocksUnitWeight=21, wtUnitWeight=9.807)
slices = Slices(
    material=material, slipSurfCoords=surface.coords,
    slopeCoords=slope.coords, numSlices=10,
    watertabCoords=watertable.coords, bim=bim)
stabAnalysis = SlopeStabl(slices, seedFS=1, Kh=0)
fig = stabAnalysis.plot()
