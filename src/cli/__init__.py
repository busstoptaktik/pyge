from .agurk import agurk


def plonk():
    print("PLONK!")


def plink():
    print("PLINK-PLONK!")
    plonk()
    agurk()


def ellps():
    from pyge.ellipsoid import Ellipsoid

    e = Ellipsoid.named("GRS80")
    print(f"Eccentricity [ppm]: {e.eccentricity()*1e6}")
    print(f"Eccentricity squared [ppm]: {e.eccentricity_squared()*1e6}")
    print(f"Third flattening [ppm]: {e.third_flattening()*1e6}")
    print(f"Third flattening squared [ppm]: {(e.third_flattening()**2)*1e6}")
    print(f"Eccentricity/Third flattening: {e.eccentricity()/e.third_flattening()}")
