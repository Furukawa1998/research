def poly_to_list(poly,var):
    minus_var = []
    for w in var:
        minus_var.append('-'+w)
    DIM = len(var)
    F0 = []
    F1 = []
    F2 = []
    F3 = []
    F = []
    F0 = poly.split(',')
    for w in F0:
        F1.append(w.split('+'))
    for i in range(len(F1)):
        F2.append([])
        for j in range(len(F1[i])):
            F2[i].append(F1[i][j].split('*'))
    for i in range(len(F2)):
        F3.append([])
        for j in range(len(F2[i])):
            F3[i].append([])
            for k in range(len(F2[i][j])):
                F3[i][j].append(F2[i][j][k].split('^'))
    for i in range(len(F3)):
        F.append([])
        for j in range(len(F3[i])):
            F[i].append([])
            for k in range(len(var)):
                F[i][j].append(0)
            F[i][j].append(1)
            for k in range(len(F3[i][j])):
                if len(F3[i][j][k]) == 2:
                    for l in range(len(var)):
                        if var[l] == F3[i][j][k][0]:
                            F[i][j][l] = int(F3[i][j][k][1])
                            break
                        elif minus_var[l] == F3[i][j][k][0]:
                            F[i][j][l] = int(F3[i][j][k][1])
                            F[i][j][DIM] = F[i][j][DIM]*(-1)
                            break
                else:
                    if F3[i][j][k][0] in var:
                        #print(F3[i][j][k][0])
                        for l in range(len(var)):
                            #print("var[l] = ",var[l])
                            if var[l] == F3[i][j][k][0]:
                                F[i][j][l] = 1
                                break
                    elif F3[i][j][k][0] in minus_var:
                         for l in range(len(minus_var)):
                             if minus_var[l] == F3[i][j][k][0]:
                                 F[i][j][l] = 1
                                 F[i][j][DIM] = F[i][j][DIM]*(-1)
                                 break
                    else:
                        F[i][j][DIM] = F[i][j][DIM]*int(F3[i][j][k][0])
    return F

