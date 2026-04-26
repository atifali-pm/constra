# Surfer as a Reference Point

> **Why this document exists.** Surfer is included as a different sort of reference. Petrel shows what a workspace can be. Surfer shows what a plotting tool cannot do for someone who needs more than a finished figure. Surfer is good at what it does. It just is not a workspace, and a workspace is what engineering needs.

## Overview

Surfer (Golden Software) is a plotting and contouring package widely used in geoscience. It produces excellent individual map and section figures. It was not built as an integrated interpretation environment.

Product page: <https://www.goldensoftware.com/products/surfer>

## No dedicated views

Surfer does not have separate Map, Section, and 3D views that share state. Maps and sections both end up in the same generic plot window. There is no shared canvas, no automatic basemap, no cross-view synchronisation. Every figure is built by hand, and every figure is its own thing.

## No project-level coordinate frame

Surfer does not put every dataset into a shared coordinate system. It plots data against whatever values are in the file, and it is up to the user to make sure those values agree across files. If two datasets are in different coordinate systems, the user notices that, not the software.

## Manual workflow

Every layer, every object, every label has to be added by hand. That is fine for a one-off figure. It is not fine when many datasets have to stay consistent, when the underlying data changes regularly, or when the interpreter needs to switch between map, section, and 3D in the course of a working day.
