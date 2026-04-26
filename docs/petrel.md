# Petrel as a Reference Point

> **Why this document exists.** Petrel appears in this project only as a reference. It is the standard interpretation platform in oil and gas, built by Schlumberger, and it works well there. Constra is not a Petrel competitor and is not an attempt to make Petrel cheaper. It is being built for a different industry, engineering and construction, which has no equivalent workspace of its own. Petrel is reproduced here because it shows what an integrated geoscience workspace can do for the geologist who lives inside it. That is the shape Constra has to take for its own industry.

## Overview

Inside oil and gas, Petrel handles seismic data, well logs, geological surfaces, and reservoir models in one project. The user works in 2D maps, vertical sections, and 3D scenes, and everything stays in sync.

## Map View

The Map View shows everything in its real-world location. Satellite imagery, seismic line tracks, well heads, and cultural features (roads, buildings, infrastructure) layer up in the same window.

**Figure 1. Satellite basemap in Map View.** A satellite image of the project area is loaded as the bottom layer of the map and gives every other layer its geographic context.

![Satellite basemap in Petrel Map View](images/01-petrel-map-view-satellite.png)

**Figure 2. Seismic lines and well locations on the same map.** The interpreter can see which line passes nearest to which well and open that line directly from the map.

![Seismic lines and wells in Petrel Map View](images/02-petrel-map-seismic-wells.png)

## Section View

The Section View is for data that lives on a vertical slice through the ground: 2D seismic lines, well logs, horizons, and faults. Click a line on the map and it opens here as a vertical section, ready to interpret.

**Figure 3. A 2D seismic line displayed as a vertical section in Petrel.**

![2D seismic section in Petrel](images/03-petrel-section-view-seismic.png)

> **Map View and Section View are linked.** Pick a horizon in the section and the same pick shows up on the map. Move a crosshair on the map and the section follows. The same is true for every other data type in the project.

## 3D View

The 3D View shows the same data in three dimensions. It is linked to the Map and Section views, so a selection made anywhere appears in all three.

**Figure 4. Several 2D seismic lines drawn together in 3D.** The geologist sees how the subsurface looks along the different acquisition directions at once.

![3D view of seismic lines in Petrel](images/04-petrel-3d-seismic-lines.png)

**Figure 5. A reservoir model in 3D with a well trajectory through it.** The well path against the reservoir body is visible at a glance.

![3D reservoir and well in Petrel](images/05-petrel-3d-reservoir-well.png)

## Coordinate System

Petrel works in real-world coordinates, both geographic (latitude/longitude) and projected (Easting/Northing). Reprojection is handled by the software, not by the user. Two datasets in different systems land in the right place without manual intervention. This is what makes the cross-view interactivity actually useful: the well in the Map View is the same well in the Section View and in 3D, because all three views read from the same coordinate frame. Constra needs the same property for engineering data.
