from fractions import Fraction
import sys
import sugar_strategy_ver5
import readpoly
import time

F_origin ='x+-t+-u,y+-t^2+-2*t*u,z+-t^3+-3*t^2*u'
var = ['t','u','x','y','z']
F = readpoly.poly_to_list(F_origin,var)
print(F)
print("order=",end="")
order=int(input())
for i in range(len(F)):
    sugar_strategy_ver5.select_order(F[i],order,len(var))
    print("F[",i,"]= ",end="")
    sugar_strategy_ver5.print1(F[i],var)
#print(F)
t1=time.time()
G = sugar_strategy_ver5.buchberger(F,order,var)
t2=time.time()
print("buch 経過時間",t2-t1)
print()
print("impbuch: groebner basies")
for i in range(len(G)):
    print("f",i,"=",end='')
    sugar_strategy_ver5.print1(G[i],var)
#sugar_strategy_ver4.count(G,order,var)
#MINI=f_buch.minimal(G)
#print()
#print("minimal groebner basies")
#for i in range(len(MINI)):
    #print("f~",i,"=",end='')
    #f_buch.print1(MINI[i])
#f_buch.count(MINI)
