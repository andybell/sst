# ---------------------------------------------------------------------------------------------------
# Name: sst.pyt
# Purpose: ArcGIS python toolbox containing geoprocessing tools for netcdf sea surface temps
# Author: Andy Bell (ambell@ucdavis.edu)
# Created: 7/10/2015
# ---------------------------------------------------------------------------------------------------

import arcpy
import os
from arcpy.sa import *

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
		self.label = "SST"
		self.alias = "Tools for SST netCDFs"

		# List of tool classes associated with this toolbox
		self.tools = [days_above_c]


class days_above_c(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Number Days above Temperature"
		self.description = "Calculates the number of days above temperature threshold"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""

		sst_file = arcpy.Parameter(displayName="Sea Surface Temperature Daily Means (netCDF)", name="sst_file", datatype="DEFile",
								 parameterType="Required", direction="Input")

		sst_file.filter.list = ["nc"]

		threshold = arcpy.Parameter(displayName="Threshold Temperature (in C)", name="threshold", datatype="GPDouble",
		                            parameterType="Required")

		results = arcpy.Parameter(displayName="Output File", name="results", datatype=["DERasterDataset", "DERasterCatalog"],
								  parameterType="Required", direction="Output")

		params = [sst_file, threshold, results]
		return params

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""

		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""

		# get parameters
		# Parameters
		sst = parameters[0].valueAsText
		threshold = parameters[1].valueAsText
		out_raster = parameters[2].valueAsText

		arcpy.AddMessage("Working on: %s" % sst)

		ncFP = arcpy.NetCDFFileProperties(sst)
		ncDim = ncFP.getDimensions()


		# check to make
		sumEmpty = 'Yes'

		# loop through all dimensions and show the value
		for dim in ncDim:
			#print dim
			top = ncFP.getDimensionSize(dim)
			for i in range(0, top):
				if dim == "time":
					dimension_values = ncFP.getDimensionValue(dim, i)
					date = str(dimension_values)
					arcpy.AddMessage(date)
					dv1 = ["time", dimension_values]
					dimension_value = [dv1]
					arcpy.AddMessage("Dimension_value: %s" %dimension_value)
					arcpy.MakeNetCDFRasterLayer_md(sst, "sst", "lon", "lat", 'sst_rasterlayer', '#', dimension_value, "BY_VALUE")

					# classify raster based on threshold
					classified = Con(arcpy.Raster('sst_rasterlayer') >= float(threshold), 1, 0)

					if sumEmpty == 'Yes':
						sumRas = classified
						sumEmpty = 'No'
					else:
						sumRas = sumRas + classified

					arcpy.Delete_management('sst_rasterlayer')

		arcpy.AddMessage("FINISHED")

		sumRas.save(out_raster)

		return


