from fractions import Fraction
import sys
import copy
import time

def print1(a,var): #多項式の出力 a:２次配列
    COE = len(var)
    if len(a)!=0:
        for i in range(len(a)):
            p=0
            if a[i][COE]!=1:
                print(a[i][COE],end='')
                p=1
            for j in range(COE):
                if a[i][j]==1:
                    print(var[j],end='')
                    p=1
                elif a[i][j]!=0:
                    print(var[j],end='')
                    print("^",end='')
                    print(a[i][j],end='')
                    p=1
            if p==0:
                print(a[i][COE],end='')
            if i != len(a)-1:
                print("+",end='')
            else:
                print()
    else:
        print(0)

def zero(a,start,COE):  #係数が０の項を削除する a:２次配列,start:整数
    p = len(a)-1
    i = 0
    while i <= p:
        #print(i)
        if a[i][COE] == 0:
            a.pop(i)
            p = p-1
        else:
            i = i+1
            break


def comp(a,b,COE): #２項の大きさをlex順序に従って比較 a:１次配列,b:１次配列
    for i in range(COE):
        #print(i,a[i],b[i])
        if a[i] < b[i]: 
            return 0  #a<b
        elif a[i] > b[i]:
            return 1  #a>b
    return 2  #a=b

def comp_dim(a,b,COE):
    a_dim=0
    b_dim=0
    for i in range(COE):
        a_dim=a_dim+a[i]
        b_dim=b_dim+b[i]
    if a_dim < b_dim:
        return 0
    elif a_dim == b_dim:
        return 2
    else:
        return 1

def r_comp(a,b,COE):
    for i in range(COE-1,-1,-1):
        if a[i]<b[i]:
            return 1
        elif a[i]>b[i]:
            return 0
    return 2

def comp_glex(a,b,COE):
    if comp_dim(a,b,COE) == 0:
        return 0
    elif comp_dim(a,b,COE) == 1:
        return 1
    else:
        return comp(a,b,COE)

def comp_grlex(a,b,COE):
    if comp_dim(a,b,COE) == 0:
        return 0
    elif comp_dim(a,b,COE) == 1:
        return 1
    else:
        return r_comp(a,b,COE)

def select_comp(a,b,order,COE):
    if order == 0:
        comp(a,b,COE)
    elif order == 1:
        comp_glex(a,b,COE)
    else:
        comp_grlex(a,b,COE)
        
def change(a,i,j): #２項を入れ替える a:２次配列,ij:整数
    c = copy.copy(a[i])
    #print("c=",c)
    a[i] = a[j]
    a[j] = c

def sim(a,start,COE): #同類項を纏める  a:２次配列,start:整数
    if len(a)<=2:
        return
    i = 0
    p = len(a)-1
    while i < p:
        if comp(a[i],a[i+1],COE) == 2 :
            a[i][COE] = a[i][COE] + a[i+1][COE]
            a.pop(i+1)
            p = p-1
        else:
            i=i+1

def tdeg(f,COE):
    deg = 0
    for i in range(COE):
        deg = deg + f[i]
    return deg

def lex(a,COE): #lex順序で並び換える a:２次配列
    zero(a,0,COE)
    if len(a)==1:
        return
    #print("a=",a)
    for i in range(len(a)):
        for j in range(len(a)-1,i,-1):
            r = comp(a[j],a[j-1],COE)
            if r == 1:
                change(a,j,j-1)
    sim(a,0,COE)
    #print(a)
    zero(a,0,COE)

def grlex(a,COE):
    zero(a,0,COE)
    for i in range(len(a)):
        for j in range(len(a)-1,i,-1):
            r = comp_dim(a[j],a[j-1],COE)
            if r == 1:
                change(a,j,j-1)
            elif r == 0:
                pass
            else:
                if r_comp(a[j],a[j-1],COE) == 1:
                    change(a,j,j-1)
    sim(a,0,COE)
    zero(a,0,COE)

def glex(a,COE):
    zero(a,0,COE)
    for i in range(len(a)):
        for j in range(len(a)-1,i,-1):
            r = comp_dim(a[j],a[j-1],COE)
            if r == 1:
                change(a,j,j-1)
            elif r == 0:
                pass
            else:
                if comp(a[j],a[j-1],COE) == 1:
                    change(a,j,j-1)
    sim(a,0,COE)
    zero(a,0,COE)

def select_order(a,order,COE):
    if order == 0:
        lex(a,COE)
    elif order == 1:
        glex(a,COE)
    else:
        grlex(a,COE)


def add(a,b,order,COE): #多項式+多項式 a:２次配列,b:２次配列
    c = a + b
    select_order(c,order,COE)
    return c

def diff(a,b,order,COE):  #多項式-多項式 a:２次配列,b:２次配列
    d=[]
    for i in range(len(b)):
        d.append([])
    for i in range(len(b)):
        for j in range(COE+1):
            d[i].append(0)
    for i in range(len(b)):
        for j in range(COE):
            d[i][j]=b[i][j]
        d[i][COE] = -b[i][COE]
    c = a+d
    select_order(c,order,COE)
    return c

def pro(a,b,COE): #多項式×単項式 a:２次配列,b:１次配列
    c = []
    for i in range(len(a)):
        c.append([])
    for i in range(len(a)):
        for j in range(COE+1):
            c[i].append(0)
    for i in range(len(a)):
        for j in range(COE):
            c[i][j] = a[i][j] + b[j]
        c[i][COE] = a[i][COE]*b[COE]
    return c

def quo_const(a,b): #整数×整数 a,b:整数
    c = Fraction(a,b)
    return c

def quo_mono(a,b,COE): #単項式÷単項式 a:１次配列,b:１次配列
    c=[]
    for i in range(len(a)):
        c.append(0)
    for i in range(COE):
        c[i] = a[i] - b[i]
    c[COE] = quo_const(a[COE],b[COE])
    return c

def comp_mono(a,b,COE): #割り算可能か否かの判定 a:１次配列,b:１次配列
    for i in range(COE):
        if a[i]<b[i]:
            return 0
    return 1
        

def warizan(a,F,order,COE): #割り算algorithm a:２次配列,F:３次配列
    r = []
    s=[]
    s = copy.copy(a)
    p=1
    while len(s) != 0:
        lts = s[0]
        while p != 0:
            p=0
            for i in range(len(F)):
                ltf = F[i][0]
                while comp_mono(lts,ltf,COE) == 1:
                    p=1
                    lts_ltf = quo_mono(lts,ltf,COE)
                    product = pro(F[i],lts_ltf,COE)
                    s = diff(s,product,order,COE)
                    select_order(s,order,COE)
                    if len(s) == 0:
                        return r
                    lts = s[0]
        r.append(s[0])
        s.pop(0)
    return r

def LCM(a,b,COE): #単項式の最大公倍元を求める a,b:１次配列
    c=[]
    for i in range(COE):
        if a[i]>=b[i]:
            c.append(a[i])
        else:
            c.append(b[i])
    c.append(1)
    return c

        


def s_poly(a,b,order,COE): #２つの多項式のS多項式を求める
    lta=a[0]
    ltb=b[0]
    gamma=LCM(lta,ltb,COE)
    s_a=quo_mono(gamma,lta,COE)
    s_b=quo_mono(gamma,ltb,COE)
    f_a=pro(a,s_a,COE)
    f_b=pro(b,s_b,COE)
    c=diff(f_a,f_b,order,COE)
    return c

def prime(a,b,COE): #aとbの先頭項が互いに素であるかを判定 a:２次配列,b:２次配列
    for i in range(COE):
        if a[0][i]>0 and b[0][i]>0:
            return 0
    return 1

def Criterion(i,j,Sp,G,COE):
    for k in range(len(G)):
        if i != k and j != k:
            #print(G)
            if comp_mono(LCM(G[i][0],G[j][0],COE),G[k][0],COE) == 1:
                if i>k:
                    P1=(k,i)
                else:
                    P1=(i,k)
                if j>k:
                    P2=(k,j)
                else:
                    P2=(j,k)
                #print("a")
                if P1 not in Sp and P2 not in Sp:
                    return 1
    return 0

def normal_strategy(p,G,order,COE):
    if len(p) == 0:
        return
    for i in range(len(p)-1):
        for j in range(len(p)-1,i,-1):
            c=select_comp(LCM(G[p[j][0]][0],G[p[j][1]][0],COE),LCM(G[p[j-1][0]][0],G[p[j-1][1]][0],COE),order,COE)
            if c == 0:
                change(p,j,j-1)

def minimal_sugar(Sp,Sp_sugar,COE,order):
    min_sugar=[]
    if len(Sp) == 1:
        min_sugar.append(Sp[0])
        return min_sugar
    for i in range(len(Sp)-1):
        for j in range(len(Sp)-1,i,-1):
            if Sp_sugar[Sp[j-1]] > Sp_sugar[Sp[j]]:
                change(Sp,j-1,j)
    min_sugar.append(Sp[0])
    for i in range(1,len(Sp)):
        if Sp_sugar[Sp[0]] == Sp_sugar[Sp[i]]:
            min_sugar.append(Sp[i])
    return min_sugar
        
        
        
def generate_sugar(f,COE):
    sugar = 0
    for i in range(len(f)):
        deg_i = tdeg(f[i],COE)
        if sugar < deg_i:
            sugar = deg_i
    return sugar
    
def generate_Sp_sugar(F,p,f_sugar,COE):
    lta = F[p[0]][0]
    ltb = F[p[1]][0]
    gamma = LCM(F[p[0]][0],F[p[1]][0],COE)
    s_a = quo_mono(gamma,lta,COE)
    s_b = quo_mono(gamma,ltb,COE)
    deg_a = tdeg(s_a,COE)
    deg_b = tdeg(s_b,COE)
    sp_sugar = max(f_sugar[p[0]]+deg_a,f_sugar[p[1]]+deg_b)
    return sp_sugar
    
def buchberger(F,order,var): #buchberger algorithm F:３次配列
    COE = len(var)
    #print(F)
    G = []
    Sp = []
    f_sugar = []
    min_sugar = []
    G = copy.copy(F)
    t = len(F)-1
    Spoly={}
    Sp_sugar = {}
    check1=0
    check2=0
    time_warizan =0
    waste = 0
    #print("G=",G)
    for i in range(len(F)):
        f_sugar.append(generate_sugar(F[i],COE))
    for i in range(len(F)-1):
        for j in range(i+1,len(F)):
            Sp.append((i,j))
            Spoly[(i,j)] = s_poly(G[i],G[j],order,COE)
            Sp_sugar[(i,j)] = generate_Sp_sugar(G,(i,j),f_sugar,COE)
    #print(Spoly)
    #print(Sp)
    while Sp != []:
        check1=check1+1
        time_1 = 0
        time_2 = 0
        min_sugar = minimal_sugar(Sp,Sp_sugar,COE,order)
        #print(min_sugar)
        #print('Sp =',Sp)
        #print()
        normal_strategy(min_sugar,G,order,COE)
        #print(G)
        #print(min_sugar[0][0],min_sugar[0][1])
        if prime(G[min_sugar[0][0]],G[min_sugar[0][1]],COE) != 1 and Criterion(min_sugar[0][0],min_sugar[0][1],Sp,G,COE) != 1:
            check2=check2+1
            s=Spoly[min_sugar[0]]
            time_1 = time.time()
            s=warizan(s,G,order,COE)
            time_2 = time.time()
            time_warizan = time_warizan + (time_2 - time_1)
            #print("s=", s)
            if s != []:
                t=t+1
                G.append(s)
                f_sugar.append(generate_sugar(G[t],COE))
                #print("G=",G)
                for j in range(t):
                    Sp.append((j,t))
                    Spoly[(j,t)] = s_poly(G[j],G[t],order,COE)
                    Sp_sugar[(j,t)] = generate_Sp_sugar(G,(j,t),f_sugar,COE)
            else:
                waste = waste + 1
        for i in range(len(Sp)):
            if Sp[i] == min_sugar[0]:
                Spoly.pop(Sp[i])
                Sp_sugar.pop(Sp[i])
                Sp.pop(i)
                break
        #print(Sp)
    print("全体のroop",check1,"Criterion",check2)
    print("time_warizan =",time_warizan)
    print("waste =",waste)
    return G
                
        

def count(g,order,var):
    COE = len(var)
    a=0
    for i in range(len(g)-1):
        for j in range(i+1,len(g)):
            s=s_poly(g[i],g[j],order,COE)
            r=warizan(s,g,order,COE)
            if r != []:
                print("FALSE",i,j)
                a=1
    if a == 0:
        print("TRUE")

def minimal(g):
    mini=copy.copy(g)
    newG=[]
    delete=[]
    for i in range(len(g)):
        t=quo_const(1,g[i][0][COE])
        for j in range(len(g[i])):
            mini[i][j][COE]=mini[i][j][COE]*t
    print(mini)
    for i in range(len(g)-1):
        for j in range(i+1,len(g)):
            ltfi=mini[i][0]
            ltfj=mini[j][0]
            if comp_mono(ltfi,ltfj)==1:
                if i not in delete:
                    delete.append(i)
            elif comp_mono(ltfj,ltfi)==1:
                if j not in delete:
                    delete.append(j)
    print(delete)
    for i in range(len(mini)):
        if i not in delete:
            newG.append(mini[i])
    return newG
