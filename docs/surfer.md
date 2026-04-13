# Surfer — Overview

Surfer (by Golden Software) is a plotting and contouring package widely used for displaying spatial data. It is capable software and well suited to individual map and section figures, but it was not designed as an integrated interpretation environment in the way Petrel was.

Product page: <https://www.goldensoftware.com/products/surfer>

---

## Map View

Surfer does not provide a dedicated Map View that is separate from other views. All output — whether it is conceptually a map or a vertical section — is drawn into the same plot window. There is no automatic geographic context layer, no concept of "all datasets in their true location on a shared canvas," and no cross-view synchronisation. Each map is a standalone figure that the user constructs by hand.

---

## Section View

There is likewise no dedicated Section View. A vertical section is simply another plot placed in the same generic plot window. It is not linked to any map, so selecting a line on a map does not open the corresponding section, and moving a cursor on a section does not highlight the location on a map. The two are independent figures that happen to share an application.

---

## 3D View

Surfer offers 3D surface and wireframe plots, but these are again standalone outputs rather than a synchronised 3D workspace. A 3D plot does not share state with any 2D map or section that the user has open.

---

## Coordinate System

Surfer does not natively work in real-world geographic or projected coordinate systems the way Petrel does. Data is plotted against whatever coordinate values are supplied in the input file, and the user is responsible for ensuring those values are consistent across datasets. There is no built-in projection engine that places every dataset into a shared real-world frame.

---

## Workflow

Surfer's workflow is predominantly manual. Every dataset, every object, every label is added to the plot by the user. This is acceptable when producing a single figure, but it scales poorly when many datasets need to be kept consistent, when data is updated frequently, or when an interpreter needs to move fluidly between map, section, and 3D perspectives of the same subsurface model.
