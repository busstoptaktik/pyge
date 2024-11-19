# PYGE - PYthon GEodesy

## What?

A Python implementation of a minimum viable geodetic procesing data model. Somewhat inspired by the current version of ISO-19111 "Referencing by Coordinates", but focusing on the triplet of

- Reference frames
- Coordinate operations and
- Coordinates

Curently, PYGE is just a mock up of a data model, intended for ease-of-experimentation. PYGE does not implement any actual geodetic computational functionality, currently: It is merely a framework for demonstrating the data flow and the handling of parameters

PYGE builds on experience from [Rust Geodesy](https://github.com/busstoptaktik/geodesy)

## Why?

The raison d'etre for PYGE is not too different from that of Rust Geodesy. See the essays [Why Rust Geodesy](https://github.com/busstoptaktik/geodesy/blob/main/ruminations/004-rumination.md) and [What's wrong with ISO-19111?](https://github.com/busstoptaktik/geodesy/blob/main/ruminations/010-rumination.md) - and in general the material [listed here](https://github.com/busstoptaktik/geodesy/blob/main/ruminations/README.md).
