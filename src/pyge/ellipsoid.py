from math import sqrt, hypot, atan2, sin, cos, copysign, pi


class Ellipsoid:
    """
    An ellipsoid class with fundamental geometric primitives

    Based on the ellipsoid trait from Rust Geodesy
    """

    # a: float = 6378137.0
    # f: float = 1.0 / 298.2572221008827

    def __init__(self, a: float, rf: float):
        self.a = a
        self.f = 1.0 / rf

    def named(name: str):
        match name:
            case "GRS80":
                return Ellipsoid(6378137.0, 298.2572221008827)
            case "WGS84":
                return Ellipsoid(6378137.0, 298.257223563)
            case "intl":
                return Ellipsoid(6378388.0, 297.0)

        # Not a known ellipsoid - try to interpret is as an (a,1/f) pair
        af = name.split(",")
        if len(af) != 2:
            raise NameError(f"Unknown ellipsoid '{name}'")
        try:
            a, f = float(af[0]), float(af[1])
        except ValueError:
            raise NameError(f"Unknown ellipsoid '{name}'")
        return Ellipsoid(a, f)

    def eccentricity_squared(self):
        """The squared eccentricity *e² = (a² - b²) / a²*"""
        return self.f * (2 - self.f)

    def eccentricity(self):
        """The eccentricity *e*"""
        return sqrt(self.f * (2 - self.f))

    def second_eccentricity_squared(self) -> float:
        """The squared second eccentricity *e'² = (a² - b²) / b² = e² / (1 - e²)*"""
        es = self.eccentricity_squared()
        return es / (1.0 - es)

    def second_eccentricity(self) -> float:
        """The second eccentricity *e'*"""
        return sqrt(self.second_eccentricity_squared())

    def semimajor_axis(self):
        return self.a

    def semiminor_axis(self):
        """The semiminor axis, *b*"""
        return self.a * (1.0 - self.f)

    def prime_vertical_radius_of_curvature(self, latitude: float) -> float:
        """The radius of curvature in the prime vertical, *N*"""
        s = sin(latitude)
        return self.a / sqrt(1.0 - s * s * self.eccentricity_squared())

    def meridian_radius_of_curvature(self, latitude: float) -> float:
        """The meridian radius of curvature, *M*"""
        es = self.eccentricity_squared()
        num = self.semimajor_axis() * (1.0 - es)
        denom = 1.0 - sin(latitude) ** 2 * pow(es, 1.5)
        return num / denom

    def flattening(self) -> float:
        """The flattening, *f  =  (a - b) / a*"""
        return self.f

    def second_flattening(self) -> float:
        """The second flattening, *g  =  (a - b) / b*"""
        b = self.semiminor_axis()
        return (self.semimajor_axis() - b) / b

    def third_flattening(self) -> float:
        """The third flattening, *n  =  (a - b) / (a + b)  =  f / (2 - f)*"""
        flattening = self.flattening()
        return flattening / (2.0 - flattening)

    def aspect_ratio(self) -> float:
        """The aspect ratio, *a / b  =  1 / ( 1 - f )  =  1 / sqrt(1 - e²)*"""
        return 1.0 / (1.0 - self.flattening())

    def rectifying_radius_bowring(self) -> float:
        """
        The rectifying radius, *A*, following Bowring (1983).
        An utterly elegant way of writing out the series truncated after the *n⁴* term.
        In general, however, prefer using the *n⁸* version, in Rust Geodesy implemented as
        [rectifying_radius](Meridians::rectifying_radius), based on
        [Karney (2010)](crate::Bibliography::Kar10) eq. (29), as elaborated in
        [Deakin et al (2012)](crate::Bibliography::Dea12) eq. (41)
        """
        # A is the rectifying radius - truncated after the n⁴ term
        n = self.third_flattening()
        m = 1.0 + n * n / 8.0
        return self.a * m * m / (1.0 + n)

    def meridian_latitude_to_distance(self, latitude: float) -> float:
        """
        The distance, *M*, along a meridian from the equator to the given latitude.

        A special case of a geodesic length. This implementation follows the remarkably
        simple algorithm by Bowring (1983). See also
        https://en.wikipedia.org/wiki/Transverse_Mercator:_Bowring_series.
        Deakin et al (2012) provide a higher order (*n⁸*) implementation.
        """
        n = self.third_flattening()

        # A = self.rectifying_radius_bowring()
        # Inlining since we already have n
        m = 1.0 + n * n / 8.0
        A = self.a * m * m / (1.0 + n)

        B = 9.0 * (1.0 - 3.0 * n * n / 8.0)
        s = sin(2.0 * latitude)
        c = cos(2.0 * latitude)
        x = 1.0 + 13.0 / 12.0 * n * c
        y = 0.0 + 13.0 / 12.0 * n * s
        r = hypot(x, y)
        v = atan2(y, x)
        theta = latitude - B * pow(r, -2.0 / 13.0) * sin(2.0 * v / 13.0)
        return A * theta

    def meridian_distance_to_latitude(self, distance_from_equator: float) -> float:
        # Compute the latitude of a point, given *M*, its distance from the equator,
        # along its local meridian.
        #
        # This implementation follows the remarkably simple algorithm
        # by [Bowring (1983)](crate::Bibliography::Bow83).
        #
        # See also
        # [meridian_latitude_to_distance](Meridians::meridian_latitude_to_distance)
        n = self.third_flattening()

        # A = self.rectifying_radius_bowring()
        # Inlining since we already have n
        m = 1.0 + n * n / 8.0
        A = self.a * m * m / (1.0 + n)

        theta = distance_from_equator / A
        s = sin(2.0 * theta)
        c = cos(2.0 * theta)
        x = 1.0 - 155.0 / 84.0 * n * c
        y = 0.0 + 155.0 / 84.0 * n * s
        r = hypot(x, y)
        v = atan2(y, x)

        C = 1.0 - 9.0 * n * n / 16.0
        return theta + 63.0 / 4.0 * C * pow(r, 8.0 / 155.0) * sin(8.0 / 155.0 * v)

    def cartesian(
        self, longitude: float, latitude: float, height: float
    ) -> tuple[float, float, float]:
        """Cartesian coordinates from geographical+height"""
        N = self.prime_vertical_radius_of_curvature(latitude)
        sinlat = sin(latitude)
        coslat = cos(latitude)
        coslon = cos(longitude)
        sinlon = sin(longitude)

        X = (N + height) * coslat * coslon
        Y = (N + height) * coslat * sinlon
        Z = (N * (1.0 - self.eccentricity_squared()) + height) * sinlat
        return (X, Y, Z)

    def geographic(self, X: float, Y: float, Z: float) -> tuple[float, float, float]:
        """Cartesian to geographic conversion"""
        # We need a few additional ellipsoidal parameters
        b = self.semiminor_axis()
        eps = self.second_eccentricity_squared()
        es = self.eccentricity_squared()

        # The longitude is straightforward: Plain geometry in the equatoreal plane
        lam = atan2(Y, X)

        # The perpendicular distance from the point coordinate to the Z-axis
        p = hypot(X, Y)

        # For p < 1 picometer, we simplify things to avoid numerical havoc.
        if p < 1.0e-12:
            # The sign of Z determines the hemisphere
            phi = copysign(pi, Z)
            # We have forced phi to one of the poles, so the height is |Z| - b
            h = abs(Z) - self.semiminor_axis()
            return (lam, phi, h)

        # Fukushima (1999)
        a = self.semimajor_axis()
        T = (Z * a) / (p * b)
        c = 1.0 / sqrt(1.0 + T * T)
        s = c * T

        phi_num = Z + eps * b * s * s * s
        phi_denom = p - es * a * c * c * c
        phi = atan2(phi_num, phi_denom)

        lenphi = hypot(phi_num, phi_denom)
        sinphi = phi_num / lenphi
        cosphi = phi_denom / lenphi

        a = self.semimajor_axis()
        N = self.prime_vertical_radius_of_curvature(phi)

        # Bowring (1985), as quoted by Burtch (2006), suggests this expression
        # as more accurate than the commonly used h = p / cosphi - N
        h = p * cosphi + Z * sinphi - a * a / N
        return (lam, phi, h)
