import numpy as np
import Algo_uno as uno
import random
import time

class Algo_tres:
    def __init__(self, sequence_S, sequence_T, dictionnaire_score, marge, variation, rand_min, rand_max):

        self.op = 0
        self.sequence_S = np.array(list(sequence_S))
        self.sequence_T = np.array(list(sequence_T))
        self.matrice = np.zeros((len(sequence_S), len(sequence_T)))
        self.dictionnaire_score = dictionnaire_score
        self.marge = marge
        self.variation = variation
        self.rand_min = rand_min
        self.rand_max = rand_max

    def minimum_approximation_global(self):
        #Appel des self
        marge = self.marge
        variation = self.variation
        rand_min = self.rand_min
        rand_max = self.rand_max


        #Initialisation
        score = 0
        op = 0
        t0 = time.time()
        len_S = len(self.sequence_S)
        ind_Beg_S = 0
        ind_End_S = len_S
        len_T = len(self.sequence_T)
        ind_Beg_T = 0
        ind_End_T = len_T
        distance = 0
        keep = True
        while keep:
            #On génère la taille de notre sous-matrice puis on vérifie qu'on fait pas de "Out of bound"
            taille = random.randint(rand_min,rand_max)
            if len_T > ind_Beg_T + rand_max:
                ind_End_T = ind_Beg_T + taille
            else:
                ind_End_T = len_T - 1
                keep = False
            if len_S > ind_Beg_S + rand_max:
                ind_End_S = ind_Beg_S + taille
            else:
                ind_End_S = len_S - 1
                keep = False

            # On ajoute notre biais
            diff = random.randint(-variation,variation)
            if ind_End_T + diff < len_T:
                ind_End_T += diff

            algo = uno.Algo_uno(self.sequence_S[ind_Beg_S:ind_End_S], self.sequence_T[ind_Beg_T:ind_End_T], score, self.dictionnaire_score)
            resultat, temps, operation = algo.minimum_general_optimise()
            op += operation
            distance_local, ind_Beg_S_inc, ind_Beg_T_inc = algo.minimum_local(marge, resultat)
            distance += distance_local
            ind_Beg_S += ind_Beg_S_inc
            ind_Beg_T += ind_Beg_T_inc

        if ind_End_S >= len_S - 1:
            distance += len_T - ind_Beg_T - 1
        elif ind_End_T >= len_T - 1:
            distance += len_S - ind_Beg_S - 1
        t1 = time.time()
        return distance, t1 - t0, op

