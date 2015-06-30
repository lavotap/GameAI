#!/usr/bin/env python
#-*-coding:utf-8-*-

import math
from number import Number

class Vector(object):
    # 验证是否为向量
    @classmethod
    def is_vector(cls,vector):
        if hasattr(vector,'get_value'):
            return True
        else:
            return False

    def __init__(self,x=0,y=0,z=0):
        if hasattr(x,'__getitem__'):
            self.x=x[0]
            self.y=x[1]
            self.z=x[2]
        elif Vector.is_vector(x):
            self.x=x.x
            self.y=x.y
            self.z=x.z
        elif Number.is_number(x) and Number.is_number(y) and Number.is_number(z):
            self.x=float(x)
            self.y=float(y)
            self.z=float(z)
        else:
            print("ERROR:<__init__@Vector>:Can not init.\n")
            exit()

        self.vector=(self.x,self.y,self.z)

    # 判断是否为向量的依据
    def get_value(self):
        return (self.x,self.y,self.z)

    def __str__(self):
        if self.z!=0:
            return("Vector(%s,%s,%s)"%(Number(self.x).format(),Number(self.y).format(),Number(self.z).format()))
        else:
            return("Vector(%s,%s)"%(Number(self.x).format(),Number(self.y).format()))

    def __add__(self, other):
        if Vector.is_vector(other):
            x=other.x
            y=other.y
            z=other.z
            return Vector(self.x+x,self.y+y,self.z+z)
        else:
            exit("ERROR:<__add__@Vector>:Can not add.\n")

    def __iadd__(self, other):
        return Vector(self.vector)+other

    def __sub__(self, other):
        if Vector.is_vector(other):
            x=other.x
            y=other.y
            z=other.z
            return Vector(self.x-x,self.y-y,self.z-z)
        else:
            exit("ERROR:<__sub__@Vector>:Can not subtract.\n")

    def __isub__(self, other):
        return Vector(self.vector)-other

    def __mul__(self, other):
        if Vector.is_vector(other):
            x=other.x
            y=other.y
            z=other.z
            return self.x*x+self.y*y+self.z*z
        elif Number.is_number(other):
            return Vector(self.x*other,self.y*other,self.z*other)
        else:
            exit("ERROR:<__mul__@Vector>:Can not multiply.\n")

    def __imul__(self, other):
        return Vector(self.vector)*other

    def __div__(self, other):
        if Number.is_number(other):
            return Vector(self.x/other,self.y/other,self.z/other)
        else:
            exit("ERROR:<__div__@Vector>:Can not divide.\n")

    def __idiv__(self, other):
        return Vector(self.vector)/other

    def __floordiv__(self, other):
        if Number.is_number(other):
            return Vector(self.x//other,self.y//other,self.z//other)
        else:
            exit("ERROR:<__floordiv__@Vector>:Can not divide.\n")

    def __xor__(self, other):
        if Vector.is_vector(other):
            x=other.x
            y=other.y
            z=other.z
            return Vector(self.y*z-y*self.z,self.z*x-z*self.x,self.x*y-x*self.y)
        else:
            exit("ERROR:<__xor__@Vector>:Can not cross multiply.\n")

    def __ixor__(self, other):
        return Vector(self.vector)^other

    def __eq__(self, other):
        if Vector.is_vector(other):
            x=other.x
            y=other.y
            z=other.z
            if self.x==x and self.y==y and self.z==z:
                return True
            else:
                return False
        else:
            exit("ERROR:<__eq__@Vector>:Can not compile.\n")

    def __ne__(self, other):
        if Vector.is_vector(other):
            x=other.x
            y=other.y
            z=other.z
            if self.x==x and self.y==y and self.z==z:
                return False
            else:
                return True
        else:
            exit("ERROR:<__ne__@Vector>:Can not compile.\n")

    def __gt__(self, other):
        if Vector.is_vector(other):
            if self.get_length()>other.get_length:
                return True
            else:
                return False
        else:
            exit("ERROR:<__gt__@Vector>:Can not compile.\n")


    def __lt__(self, other):
        if Vector.is_vector(other):
            if self.get_length()<other.get_length:
                return True
            else:
                return False
        else:
            exit("ERROR:<__lt__@Vector>:Can not compile.\n")


    def __ge__(self, other):
        if Vector.is_vector(other):
            if self.get_length()>=other.get_length:
                return True
            else:
                return False
        else:
            exit("ERROR:<__gt__@Vector>:Can not compile.\n")

    def __le__(self, other):
        if Vector.is_vector(other):
            if self.get_length()<=other.get_length:
                return True
            else:
                return False
        else:
            exit("ERROR:<__lt__@Vector>:Can not compile.\n")

    # 向量的模
    def get_length(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    # 单位向量
    def get_unit(self):
        length=Vector(self.vector).get_length()
        return Vector(self.x/length,self.y/length,self.z/length)

    # 从self.vector到other向量的无符号夹角
    def get_theta(self,other):
        if Vector.is_vector(other):
            value=(Vector(self.vector)*other)/(Vector(self.vector).get_length()*other.get_length())
            return math.acos(value)/math.pi*180.0
        else:
            exit("ERROR:<get_theta@Vector>:Can not get theta.\n")

    # 从self.vector到other向量的带符号夹角，other从self.vector出发逆时针为正，顺时针为负
    def get_theta_with_sign(self,other):
        theta=self.get_theta(other)
        if (Vector(self.vector)^other).z<0:
            return theta*-1
        else:
            return theta

    # 求左垂直，右垂直向量
    def get_left(self):
        return Vector(-1*self.y,self.x,0)

    def get_right(self):
        return Vector(self.y,-1*self.x,0)



