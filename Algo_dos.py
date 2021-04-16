import numpy as np
import time
import math

class Algo_dos:
    def __init__(self, sequence_S, sequence_T, dictionnaire_score, c):

        self.op = 0
        self.sequence_S = np.array(list(sequence_S))
        self.sequence_T = np.array(list(sequence_T))
        self.matrice = np.zeros((len(sequence_S), len(sequence_T)))
        self.dictionnaire_score = dictionnaire_score
        self.c = c

    def case_valide(self, i, j):
        len_T = len(self.sequence_T)
        len_S = len(self.sequence_S)
        c = self.c
        diff = len_S - len_T
        if i == j:          #Diagonal suppérieur
            return True
        if i == j + diff:   #Diagonal inferieur
            return True
        if i < j + c:       #Triangle supperieur
            return False
        if i > j+ diff - c: #Triangle inférieur
            return False
        return True
    def minimum_general_c_gap(self):
        #On ramène nos variables localement pour pas avoir à ref self
        M = self.matrice
        sequence_S = self.sequence_S
        sequence_T = self.sequence_T
        c = self.c

        #Start the clock
        t0 = time.time()

        #Initialisation
        len_S = len(sequence_S)
        len_T = len(sequence_T)

        for i in range(len_S):
            if self.case_valide(i, 0):
                M[i][0] = i

        #On remplit la matrice
        for i in range(1, len_S):
            for j in range(1, len_T):
                if self.case_valide(i, j):
                    Diag = M[i - 1][j - 1] + self.dictionnaire_score[(sequence_S[i], sequence_T[j])]
                    Min_up = math.inf
                    # On check le minimum par rapport au variable au dessus
                    if c <= i:
                        for k in range(c, i):
                            if self.case_valide(i-k,j):
                                if Min_up > M[i-k,j] + k*self.dictionnaire_score[(sequence_S[i-k],'_')]:
                                    Min_up = M[i-k,j] + k*self.dictionnaire_score[(sequence_S[i-k],'_')]
                    if Diag < Min_up:
                        M[i][j]= Diag
                    else:
                        M[i][j] = Min_up


        t1 = time.time()
        self.matrice = M
        temps = t1 - t0
        return self.matrice[len(sequence_S)-1][len(sequence_T)-1], temps