__author__ = 'Andy'

import arcpy
import os

# location of folder
sst = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

in_netcdf = os.path.join(sst, r"data\sst.day.mean.2014.v2.nc")

print in_netcdf

try:
	ncFP = arcpy.NetCDFFileProperties(in_netcdf)
	ncDim = ncFP.getDimensions()

	# loop through all dimensions and show the value
	for dim in ncDim:
		#print dim
		top = ncFP.getDimensionSize(dim)
		for i in range(0,top):
			if dim == "time":
				print ncFP.getDimensionValue(dim, i)
except:
	print arcpy.GetMessage(2)