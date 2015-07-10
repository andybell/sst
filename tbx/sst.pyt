# ---------------------------------------------------------------------------------------------------
# Name: sst.pyt
# Purpose: ArcGIS python toolbox containing geoprocessing tools for netcdf sea surface temps
# Author: Andy Bell (ambell@ucdavis.edu)
# Created: 7/10/2015
# ---------------------------------------------------------------------------------------------------

import arcpy
import os





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

		results = arcpy.Parameter(displayName="Output location", name="results", datatype="DEWorkspace",
								  parameterType="Required", direction="Output")

		params = [sst_file, results]
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
		out = parameters[1].valueAsText


		arcpy.AddMessage("Points: %s" % sst)

		return
