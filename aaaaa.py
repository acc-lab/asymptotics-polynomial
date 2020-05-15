n=5

class Point():
    def __init__(self, x, y):
        self.x=x
        self.y=y
        

def isPositiveRect(p1, p2, p3):
    area2 = abs(p1.x*p2.y+p2.x*p3.y+p3.x*p1.y-p1.y*p2.x-p2.y*p3.x-p3.y*p1.x)

    return area2!=0

total=0

for p1x in range(n):
    for p1y in range(n):
        
        for p2x in range(n):
            for p2y in range(n):
                
                for p3x in range(n):
                    for p3y in range(n):
                        
                        p1 = Point(p1x,p1y)
                        p2 = Point(p2x,p2y)
                        p3 = Point(p3x,p3y)

                        if isPositiveRect(p1, p2, p3):
                            total+=1
                            print(total)
                            
print("ANS:", total//6)
