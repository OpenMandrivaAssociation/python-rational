"""Rational numbers.

   rational
   --------
     A function to construct rational numbers, with signature
     rational(n, d=1). Unless both n and d are integers, longs, or
     rationals, the result is undefined (although the result of "print
     rational(1.5)" may be "3.0/2.0" this should not be relied on).

     The resulting value is of a numeric type with the semantics of an
     unboundedly precise rational number, as described in PEP 239.

   gcd
   ---
     A function for computing the greatest common denominator.

   Extensions to PEP 239
   ---------------------
     * A hash function has been added, which guarantees that n/1
       hashes to the same value as n (handy for dictionaries).
     * The numerator has a default (0), to match other numeric types.
     * The invert operator (~) inverts the fraction.
     * Ints and longs can be coerced to rationals; otherwise,
       rationals are coerced to floats.
     * Includes 1/0, -1/0, and 0/0 as infinity, negative infinity,
       and NaN values. All NaN's are equal to each other, but not
       less than or greater than or equal to anything else. All
       infinities (of the same sign) are equal.
     * The attributes can be referred to by num and den as well as
       numerator and denominator.

   Differences from PEP 239
   ------------------------
     * The type returned by rational is rational, not RationalType.
     * The .trim method may not or may not be the same as defined in
       the PEP.
     * Because rational literals (PEP 240) are not implemented,
       the repr for rational numbers is rational(num, den).

   Open issues in PEP 239
   ----------------------
     * The type name is rational, not rat.
     * Rational numbers are not usable as sequence indices.
     * Shift operators are allowed, but mask operators are not (nor are
       bitwise logical operators).
     * Ints are not unified with rationals.

   Other issues
   ------------
     * There is no facility to convert strings ("1/2") to rationals.
     * Infinite/NaN arithmetic should match IEEE floats, but may not.
     * Because of the way cmp(x,y) works in python 2.2, it will return
       incorrect values (e.g., cmp(2, rational(0/0)) == -1). However,
       the direct comparison operators will all work properly.

   Example
   -------
     >>> from rational import rational
     >>> r = rational(2, 3)
     >>> r /= 10
     >>> print r
     1/15
"""

# rational.py version 0.1
# Written 24 June 2003 by andi payn <payn@myrealbox.com>
# This work is released under the LGPL, version 2.1 or later

def gcd(m, n):
    "Returns the greatest common denominator of its arguments."
    if m % n == 0:
        return n
    else:
        return gcd(n, m % n)

class rational(object):
    """An unboundedly-precise rational type, as described in PEP 239.

    rational(num, den) -> rational number

    Create a rational number from a numerator and an optional
    denominator, equal to (numerator / denominator), where denominator
    defaults to 1. The result is only defined for exact types (integers,
    longs, and rationals); for inexact types the results will often be
    surprising (e.g., rational(1.5) may be "3.0/2.0" but rational(1.1)
    may be "2.47697979505e+15/2.25179981369e+15").
    """
    
    def __init__(self, num=0, den=1):
        if isinstance(num, rational) and isinstance(den, rational):
            self.num, self.den = num.num * den.den, num.den * den.num
        elif isinstance(num, rational):
            self.num, self.den = num.num, num.den * den
        elif isinstance(den, rational):
            self.num, self.den = num * den.den, den.num
        else:
            self.num, self.den = num, den
        self.__simplify_()
    def __simplify_(self):
        if self.den == 0:
            self.num = cmp(self.num, 0)
        else:
            g = gcd(self.num, self.den)
            self.num /= g
            self.den /= g
        return self
    
    def __getattr__(self, name):
        if name == 'numerator': return self.num
        elif name == 'denominator': return self.den
    
    def __setattr__(self, name, value):
        if name == 'numerator': name = 'num'
        elif name == 'denominator': name = 'den'
        self.__dict__[name] = value
    
    def __str__(self):
        if self.den == 1: return str(self.num)
        else: return str(self.num) + "/" + str(self.den)
    def __repr__(self):
        return "rational(" + str(self.num) + "," + str(self.den) + ")"
    
    def __pos__(self):
        return self
    def __neg__(self):
        return rational(-self.num, self.den)
    def __add__(self, other):
        if not isinstance(other, rational): other = rational(other)
        if self.isinfinity() and other.isinfinity():
            return rational(self.num + other.num, 0)
        return rational(self.num*other.den + self.den*other.num,
                        self.den*other.den)
    __radd__ = __add__
    def __iadd__(self, other):
        self = self + other; return self
    def __sub__(self, other):
        return self + -other
    def __rsub__(self, other):
        return -self + other
    def __isub__(self, other):
        self = self - other; return self
    
    def __invert__(self):
        return rational(self.den, self.num)
    def __mul__(self, other):
        if not isinstance(other, rational): other = rational(other)
        return rational(self.num*other.num, self.den*other.den)
    __rmul__ = __mul__
    def __imul__(self, other):
        self = self * other; return self
    def __div__(self, other):
        if not isinstance(other, rational): other = rational(other)
        return self * ~other
    __truediv__ = __div__
    def __rdiv__(self, other):
        return ~self * other
    __rtruediv__ = __rdiv__
    def __idiv__(self, other):
        self = self / other; return self
    __itruediv__ = __idiv__
    def __floordiv__(self, other):
        return int(self/other)
    def __rfloordiv__(self, other):
        return int(other/self)
    def __ifloordiv__(self, other):
        self = self // other; return self
    def __mod__(self, other):
        if other == 0: return rational(1,0)
        return self - int(self/other) * other
    def __rmod__(self, other):
        return other.__mod__(self)
    def __imod__(self, other):
        self = self % mod; return self
    def __divmod__(self, other):
        return self//other, self%other
    def __rdivmod__(self, other):
        return divmod(other, self)
    
    def __lshift__(self, other):
        return rational(self.num << other, self.den)
    def __ilshift__(self, other):
        self = self << other; return self
    def __rshift__(self, other):
        return rational(self.num, self.den << other)
    def __irshift__(self, other):
        self = self >> other; return self
    
    def __pow__(self, other, modulo=None):
        if isinstance(other, rational):
            if (other.den != 1):
                return pow(float(self), float(other), modulo)
            else:
                other = int(other)
        if modulo:
            return rational(self.num ** other,
                            self.den ** other) % modulo
        return rational(self.num ** other,
                        self.den ** other)
    def __rpow__(self, other, modulo=None):
        if (self.den == 1):
            return pow(other, int(self), modulo)
        else:
            return pow(other, float(self), modulo)
    def __ipow__(self, other, modulo=None):
        self = self.__pow__(other, modulo); return self
    
    def __cmp__(self, other):
        if not isinstance(other, rational): other = rational(other)
        if self.isnan() and not other.isnan(): return NotImplemented
        elif not self.isnan() and other.isnan(): return NotImplemented
        else: return self.num * other.den - other.num * self.den
    def __eq__(self, other):
        return self.__cmp__(other) == 0
    def __ne__(self, other):
        return self.__cmp__(other) != 0
    def __lt__(self, other):
        if not isinstance(other, rational): other = rational(other)
        if self.isnan() or other.isnan(): return 0
        else: return self.__cmp__(other) < 0
    def __gt__(self, other):
        if not isinstance(other, rational): other = rational(other)
        if self.isnan() or other.isnan(): return 0
        else: return self.__cmp__(other) > 0
    def __le__(self, other):
        if not isinstance(other, rational): other = rational(other)
        if self.isnan() and other.isnan(): return 1
        elif self.isnan() or other.isnan(): return 0
        else: return self.__cmp__(other) < 0
    def __ge__(self, other):
        if not isinstance(other, rational): other = rational(other)
        if self.isnan() and other.isnan(): return 1
        elif self.isnan() or other.isnan(): return 0
        else: return self.__cmp__(other) > 0
    
    def __nonzero__(self):
        return self.num != 0 or self.den == 0
    def isinfinity(self):
        return self.num != 0 and self.den == 0
    def isnan(self):
        return self.num == 0 and self.den == 0
    
    def __float__(self):
        if self.den == 0:
            return float(1e30000) * self.num
        else:
            return float(self.num) / self.den
    def __int__(self):
        return int(self.num//self.den)
    def __long__(self):
        return long(self.num//self.den)

    def __coerce__(self, other):
        if isinstance(other, rational):
            return self, other
        elif isinstance(other, (int, long)):
            return self, rational(other)
        elif isinstance(other, type(None)):
            return self, None
        else:
            if self.den == 0:
                return int(self).__coerce__(other)
            else:
                return float(self).__coerce__(other)
    
    def __abs__(self):
        return rational(abs(self.num), self.den)
    
    def __hash__(self):
        return hash(self.num * self.den + self.den - 1)

    def __oct__(self):
        if self.den == 1: return oct(self.num)
        else: return oct(self.num) + "/" + oct(self.den)
    def __hex__(self):
        if self.den == 1: return hex(self.num)
        else: return hex(self.num) + "/" + hex(self.den)    
    
    def issimpler(self, other):
        return self.num <= other.num and self.den <= other.den and self != other
    # This algorithm is borrowed from Scheme's "rationalize" function.
    def __simplest_(self, other):
        if int(self) >= self:
            return rational(int(self))
        elif int(self) == int(other):
            rat = (~(other-int(other))).__simplest_(~(self-int(self)))
            return rational(rat.den + int(self) * rat.num, rat.num)
        else:
            return rational(int(self) + 1, 1)
    def __find_ratio_between_(self, other):
        if other < self: return other.__find_ratio_between_(self)
        elif other == self: return other
        elif self < 0: return -(other.__find_ratio_between_(-self))
        else: return self.__simplest_(other)
    def trim(self, max_den):
        return int(self) + (self-int(self)).__find_ratio_between_(rational(1, max_den))
