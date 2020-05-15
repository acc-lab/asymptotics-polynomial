from fractions import Fraction as frac
from bisect import bisect as bins
from itertools import product as prod

class Cmp():
    def __init__(self,real,imaginary):
        self.real_part = real
        self.imaginary_part = imaginary
    def __call__(self):
        return str(self.real_part)+' + '+str(self.imaginary_part)+'i'
    def __add__(self,obj):
        if type(obj) is int or type(obj) is float or type(obj) is frac:
            return Cmp(self.real_part+obj,self.imaginary_part)
        elif type(obj) is Cmp:
            return Cmp(self.real_part+obj.real_part,self.imaginary_part+obj.imaginary_part)
        else:
            return obj+self

    def __sub__(self,obj):
        if type(obj) is int or type(obj) is float or type(obj) is frac:
            return Cmp(self.real_part-obj,self.imaginary_part)
        elif type(obj) is Cmp:
            return Cmp(self.real_part-obj.real_part,self.imaginary_part-obj.imaginary_part)
        else:
            raise (-1)*obj+self

    def __radd__(self,obj):
        return self+obj

    def __rsub__(self,obj):
        return self*(-1)-obj

    def __rmul__(self,obj):
        return self*obj

    def __rtruediv__(self,obj):
        return self//obj

    def __repr__(self):
        return "{img}i+{real}".format(real=self.real_part, img=self.imaginary_part)
    
    
    def __mul__(self,obj):
        if type(obj) is int or type(obj) is float or type(obj) is frac:
            return Cmp(self.real_part*obj,self.imaginary_part*obj)
        elif type(obj) is Cmp:
            return Cmp(self.real_part*obj.real_part-self.imaginary_part*obj.imaginary_part,
                           self.real_part*obj.imaginary_part+self.imaginary_part*obj.real_part)
        else:
            return obj*self

    def __truediv__(self,obj):
        if type(obj) is int or type(obj) is float or type(obj) is frac:
            return Cmp(frac(self.real_part,obj),frac(self.imaginary_part,obj))
        elif type(obj) is Cmp:
            Den = obj.real_part**2 + obj.imaginary_part**2
            return Cmp(frac(self.real_part*obj.real_part+self.imaginary_part*obj.imaginary_part,Den),
                           frac(self.imaginary_part*obj.real_part-self.real_part*obj.imaginary_part,Den))
        else:
            return frac(1,obj)*self

    def __eq__(self,obj):
        if type(obj) is Cmp:
            return self.real_part==obj.real_part and self.imaginary_part==obj.imaginary_part
        else:
            return False
    
    def getSquaredSum(self):
        return (self.real_part**2+self.imaginary_part**2)

class Term():
    def __lt__(self, obj):
        for i in range(len(self.term)):
            if self.term[i]<obj.term[i]:
                return True
            elif self.term[i]>obj.term[i]:
                return False
        else:
            return False
    
    def __eq__(self, obj):
        return self.term==obj.term

    def __init__(self, const, term):
        self.const=const
        if const==0 or term==[]:
            self.term=[0,0,0]
        else:
            self.term=term
        
    def __add__(self, obj):
        assert self.term==obj.term or obj.const==0 or self.const==0
        if obj.const==0:
            if self.const==0:
                return Term(0,[])
            return self
        elif self.const==0:
            return obj
        else:
            return Term(self.const+obj.const, self.term)
    
    def __sub__(self, obj):
        return self+obj*-1
    
    def __mul__(self, obj):
        if type(obj) is Term:
            return Term(self.const*obj.const, [self.term[i]+obj.term[i] for i in range(len(self.term))])
        else:
            return Term(self.const*obj, self.term)
        
    def __repr__(self):
        body = ''.join(['' if self.term[i]==0 else(DEFAULT_TEXT[i] if self.term[i]==1 else '{base}^{power}'.format(base=DEFAULT_TEXT[i], power=self.term[i]))
                       for i in range(len(self.term))])
        if body=='':
            head = str(self.const)
        else:
            head = ('' if self.const==1 else ('-' if self.const==-1 else str(self.const)))

        return head+body
    
    def __truediv__(self, obj):
        return Term(frac(self.const,obj), self.term)
    
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

    def __call__(self, *arg): #kw: v1=xxx, v2=xxx, etc. Use "v"; Start with 1.
        ret=self.const
        index=0
        for term in self.term:
            ret*=arg[index]**term
            index+=1
        
        return ret

def addable(a,b):
    return a==b or a.const==0 or b.const==0

class Poly():
    def __init__(self, *arg):
        arg=list(arg)
        self.poly=arg
        self.poly.sort()

    def __add__(self, obj):
        if len(self.poly)<len(obj.poly):
            return obj+self
        
        ret = self.poly
        
        for term in obj.poly:
            index=bins(ret, term, 0, len(ret)-1)
            if addable(ret[index-1],term):
                ret[index-1]+=term
            else:
                ret.insert(index, term)

        return Poly(*ret)
    
    def __sub__(self, obj):
        return self+obj*-1
    
    def __mul__(self, obj):
        if type(obj) is Poly:
            ret=Poly(Term(0,[]))
            for my_term in self.poly:
                for term in obj.poly:
                    ret+=Poly(my_term*term)
            return ret
        else:
            return Poly(*[self.poly[i]*obj for i in range(len(self.poly))])

        
    def __repr__(self):
        ret=''
        for term in self.poly:
            ret+=str(term)+' + '
        ret=ret[:-3]
        return ret

    def __call__(self, *arg):
        ret = 0
        for term in self.poly:
            ret+=term(*arg)
        return ret
    
    def __truediv__(self, obj):
        return self*frac(1,obj)
    
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
    
    def __eq__(self, obj):
        if type(obj) is Poly:
            return self.poly == obj.poly
        else:
            return False

DEFAULT_TEXT=['x','y','z']
vary=3

getBodyByPowerRec={}
def getBodyByPower(power):
    if power in getBodyByPowerRec:
        return getBodyByPowerRec[power]
    else:
        if power==0:
            ret=[Poly(Term(1, []))]
        else:
            p = prod(getBodyByPower(power-1),[Poly(Term(1, [j==i for j in range(vary)])) for i in range(vary)])
            ret=[]
            for tup in p:
                if not(tup[0]*tup[1] in ret):
                    ret.append(tup[0]*tup[1])
        getBodyByPowerRec[power]=ret
        return ret

def getBodyByPowerAbove(power):
    ret = []
    for i in range(power+1):
        ret+=getBodyByPower(i)
    return ret

def getPolyByMesh(mesh, power):
    body=getBodyByPowerAbove(power)
    p=prod(*([mesh]*len(body)))
    ret=[]
    loader=0
    loaderMax=len(mesh)**((3**(power+1)-1)//2) #m^[(3^(p+1)-1)/2]
    for tup in p:
        s=Poly(Term(0,[]))
        for i in range(len(body)):
            s+=tup[i]*body[i]
        loader+=1
        if loader%1000==0:
            print("[*] Big F progress:{this}/{all_}".format(this=loader//1000, all_=loaderMax//1000+1))
        yield s

class lowest:
    def __init__(self):pass
    def __lt__(self, obj):return True

def bigF(*arg):
    ge = getPolyByMesh(mesh=mesh_k, power=m)
    maxium=lowest()
    maxpoly=None

    avoid_count = 0
    
    while True:
        try:
            poly=next(ge)
            power=1 if m==1 else 1/m
            mother = getComp(lambda *inp: poly(*inp).getSquaredSum()**power)
            if mother==0:
                avoid_count+=1
                if avoid_count%100==1:
                    print("[*] Skipped totally {count} polynomial(s) for avoiding zero division.".format(count=avoid_count))
                continue
            
            value=(poly(*arg).getSquaredSum()**power)/mother
            if value.real>maxium:
                maxium=value.real
                maxpoly=poly
                print("[!] Found new highest value {value} from the polynomial {pol}. (Mother:{mother})".format(value=maxium, pol=poly, mother=mother))
        except StopIteration:
            break
    return maxium

def getComp(function):
    return 2*function(1,0,0)-function(0,0,1)

def getI():
    return getComp(bigF)


#Runtime: m^[(3^(p+1)-1)/2]

m=1
p=prod(list([frac(i,2) for i in range(-2,3)]),list([Cmp(0,frac(i,2)) for i in range(-2,3)]))
p=list(p)
mesh_k=[]
for tup in p:
    mesh_k.append(tup[0]+tup[1])


while True:
    target=getI()
    print("I{}={}".format(m,target))
    m+=1
    input()