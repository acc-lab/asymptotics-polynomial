from fractions import Fraction as frac

class Pt():
    def __init__(self, li):
        self.x=li[0]
        self.y=li[1]
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

def lagrange(Point):
    Func=[]
    for index in range(0, len(Point)):
        my_func=Pol([1])
        num=1
        for index2 in range(0, len(Point)):
            if index==index2:continue
            my_func*=Pol([-(Point[index2].x), 1])
            num*=Point[index].x-Point[index2].x
        my_func=my_func/num
        Func.append(my_func)
    typeOrf=sum([Func[x]*(Point[x].y) for x in range(POWER+1)], Pol([0]))
    return typeOrf


class Pol():
    def __init__(self, pol, texting="x"):
        assert texting in ["x","y","z"]
        if pol!=[]:
            while pol[-1]==0:
                pol=pol[:-1]
                if pol==[]:
                    break
                
        self.pol=list(pol)
        self.text=texting

    def __pow__(self, n):
        if type(n) is int:
            if n==0:
                return Pol([1])
            else:
                return self*(self**(n-1))

    def __repr__(self):
        string=''
        index=len(self.pol)-1
        while index>=0:
            sign='+'
            if str(index)=='0':
                base=''
            elif str(index)=='1':
                base=self.text
            else:
                base=self.text+'^'+str(index)
                
            if str(self.pol[index])=='1':
                if base=='':
                    coe='1'
                else:
                    coe=''
            elif str(self.pol[index])=='-1':
                sign='-'
                if base=='':
                    coe='1'
                else:
                    coe=''
            elif str(self.pol[index])=='0':
                index-=1
                continue
            else:
                coe=str(self.pol[index])
                if self.pol[index]<0:
                    coe=str(-self.pol[index])
                    sign='-'
                    
                
            string+=' {} '.format(sign)+coe+base
            index-=1
            
        if string=='':
            string=' 0'

        if string[1]=="+":
            string=string[2:]
            
        string=string[1:]
        return string

    def __add__(self, obj):
        if type(obj) is Pol:
            ret=[0]*max(len(self.pol),len(obj.pol))
            for index in range(len(ret)):
                if index>=len(obj.pol):
                    ret[index]=self.pol[index]
                elif index>=len(self.pol):
                    ret[index]=obj.pol[index]
                else:
                    ret[index]=self.pol[index]+obj.pol[index]
                    
            return Pol(ret, self.text)
        else:
            return self+Pol([obj], self.text)

    def __sub__(self, obj):
        return self+obj*-1
            
    def __mul__(self, obj):
        if type(obj) is Pol:
            ret=[0]*(len(self.pol)+len(obj.pol)-1)
            for s in range(len(self.pol)):
                for o in range(len(obj.pol)):
                    ret[s+o]+=self.pol[s]*obj.pol[o]
            return Pol(ret, self.text)
        else:
            ret=[0]*len(self.pol)
            for s in range(len(self.pol)):
                ret[s]=self.pol[s]*obj
            return Pol(ret, self.text)
            

    def __truediv__(self, obj):
        ret=[0]*len(self.pol)
        for s in range(len(self.pol)):
            ret[s]=frac(self.pol[s], obj)
        return Pol(ret, self.text)

    def __radd__(self, obj):
        return self+obj
    def __rsub__(self, obj):
        return self*(-1)+obj
    def __rmul__(self, obj):
        return self*obj

    def __neg__(self):
        return self*(-1)
    def __pos__(self):
        return self

    def __call__(self, obj):
        ret=sum([self.pol[i]*(obj**(i)) for i in range(len(self.pol))])
        try:
            if ret%1==0:
                return int(ret)
            else:
                return ret
        except TypeError:
            return ret

    def _getdir_(self):
        return Pol([i*self.pol[i] for i in range(len(self.pol))][1:], self.text)
        
    def _dir_(self):
        self.pol=self._getdir_().pol

def lag(INPUT):
    global POWER
    POWER=INPUT
    Point=[]
    for p in range(POWER+1):
       Point.append(Pt([int(n) for n in input('x'+str(p)+' '+'y'+str(p)+':').split()]))

    sol=lagrange(Point)
        

    print(sol)


sumFunc=[Pol([0,1]),Pol([0,1])*Pol([1,1])/2,Pol([0,1])*Pol([1,1])*Pol([1,2])/6]

index=3

n=Pol([0,1])

while True:
    #power: index
    
    sumFunc.append((n*sumFunc[index-1]+\
                    sumFunc[index-1].pol[-1]*(n**index)-\
                    sum([sumFunc[index-1].pol[power]*(sumFunc[power](n-1)) for power in range(0,index)]))\
                   /(sumFunc[index-1].pol[-1]+1))

    index+=1
    
    if input(sumFunc[-1])=='!':
        ret = sumFunc[-1]
        
        break
