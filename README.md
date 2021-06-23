# CORHEL-Kamodo interface

CORHEL-Kamodo provides a functional interface for CORHEL fields and variables.

By functionalizing run output, many of the tasks needed in downstream analysis are vastly simplified, including:

* space-time slice interpolation
* point interpolation
* satellite fly-throughs
* coordinate transformation
* derived variables
* unit conversion
* plot generation

These capabilities are provided by subclassing the underlying [Kamodo](https://github.com/asherp/kamodo) Class, then registering functional interpolators for each variable of interest.

