import numpy as np
import time

"""
Modalité de calcul:
A lire pour comprendre comment je calcule le nombres d'opération faite,
Voici la liste générale, s'il y a des calculs plus spécifique et unique
j'expliquerai sur le code directement.
Liste:
 -Un calcul +/-/*/: = +1 opération
 -Un appel de fonction/variable : +1 opération, (un appel avec des variables en paramêtre font juste plus un, je
 considère qu'elle n'est pas appeler mais juste référencé.
 -Une comparaison : +1 opération

Je ne calcul que les opérations pertinentes à l'algorithme
 Exemple:
 -for i in range(n):
    continue
 Ici on va faire n addition, donc n opération, pour chaque addition on appel la variable i,
donc n autre opération, et a chaque itération on check si notre i a atteind n, donc une comparaison avec un appel.
Ce qui nous donne en 4n opérations
 - Soit M une matrice numpy, acceder a M[i][j] demande 3 opérations (2 pour avoir i et j, et une pour avoir le nombre
de la matrice M à la position i,j)

NB: J'utilise le mot "opération" pour me donner une unité de mesure, et mes méthodes de calculer mon nombre d'"opération",
sont purement arbitraire. Je sais que cela ne représente pas parfaitement bien ce qui ce passe dans la machine, et qu'avec
les nouveaux language/compilateur il y a de nombreux bypass sur l'utilisation des variables, mais je cherche juste a m'établir
un métric relativement simple, constant et relativement proche de ce qu'il se passe.

"""
class Algo_uno:
    def __init__(self, sequence_S, sequence_T, score, dictionnaire_score):

        self.op = 0
        self.sequence_S = np.array(list(sequence_S))
        self.sequence_T = np.array(list(sequence_T))
        self.score = score
        self.matrice = np.zeros((len(sequence_S), len(sequence_T)))
        self.dictionnaire_score = dictionnaire_score

    def Distance(self, s_w,t_w):
        s_i = self.Conversion(s_w)
        self.op += 2
        t_i = self.Conversion(t_w)
        self.op += 2
        return self.score[s_i][t_i]

    def Conversion(self, l):
        if l == 'A':
            self.op +=2   # 2, une pour comparaison, une pour chercher la lettre l
            return 0
        elif l == 'T':
            self.op += 4  # 2, une pour comparaison, une pour chercher la lettre l + 2 pour la précédente
            return 1
        elif l == 'C':
            self.op += 6  # 2, une pour comparaison, une pour chercher la lettre l + 2 pour les précédents
            return 2
        elif l == 'G':
            self.op += 8  # 2, une pour comparaison, une pour chercher la lettre l + 2 pour les précédents
            return 3
        elif l == '_':
            self.op += 10  # 2, une pour comparaison, une pour chercher la lettre l + 2 pour les précédents
            return 4
        else:
            print("Warning found other letter than A,T,C,G or _")

    def minimum_general_non_optimise(self):
        #On ramène nos variables localement pour pas avoir à ref self
        M = self.matrice
        sequence_S = self.sequence_S
        sequence_T = self.sequence_T
        self.op = 0
        op = 0

        #Start the clock
        t0 = time.time()
        #Initialisation
        for i in range(len(sequence_S)):
            M[i][0] = i
            op+=7 #4 pour la boucle 2 pour l'assignation, 1 pour chercher len a chaque iteration
        for i in range(len(sequence_T)):
            M[0][i] = i
            op+=7 #4 pour la boucle 2 pour l'assignation, 1 pour chercher len a chaque iteration

        #On remplit la matrice
        for i in range(1, len(sequence_S)):
            op+=5 #4 pour la boucle, 1 pour len(sequence_S)
            for j in range(1, len(sequence_T)):
                op += 5 #4 pour la boucle, 1 pour len(sequence_T)
                Up = M[i-1][j] + self.Distance(sequence_S[i],'_')
                op += 5
                Diag = M[i-1][j-1] + self.Distance(sequence_S[i],sequence_T[j])
                op += 5
                Left = M[i][j - 1] + self.Distance('_',sequence_T[j])
                op += 5
                if Diag < Up:
                    if Diag < Left:
                        M[i][j]= Diag
                    else:
                        M[i][j] = Left
                else:
                    if Up < Left:
                        M[i][j]= Up
                    else:
                        M[i][j] = Left
                op += 10#2 comparaison avec 2 variable chaque = 6 + on place une valeur dans notre tableau 4

        t1 = time.time()
        self.matrice = M
        temps = t1 - t0
        self.op += op
        return self.matrice[len(sequence_S)-1][len(sequence_T)-1], temps, self.op

    def minimum_general_optimise(self):
        #On ramène nos variables localement pour pas avoir à ref self
        M = self.matrice
        sequence_S = self.sequence_S
        sequence_T = self.sequence_T
        self.op = 0
        op = 0

        #Start the clock
        t0 = time.time()

        #Initialisation
        len_S = len(sequence_S)
        len_T = len(sequence_T)
        op += 4
        for i in range(len_S):
            M[i][0] = i
            op+=6 #2 pour la boucle 2 pour l'assignation
        for i in range(len_T):
            M[0][i] = i
            op+=6 #2 pour la boucle 2 pour l'assignation

        #On remplit la matrice
        for i in range(1, len_S):
            op+=4 #4 pour la boucle
            for j in range(1, len_T):
                op += 4 #4 pour la boucle
                #Je considère que le dictionnaire va retourner l'information en une opération
                Up = M[i-1][j] + self.dictionnaire_score[(sequence_S[i],'_')]
                op += 6
                Diag = M[i-1][j-1] + self.dictionnaire_score[(sequence_S[i],sequence_T[j])]
                op += 6
                Left = M[i][j - 1] + self.dictionnaire_score[('_',sequence_T[j])]
                op += 6
                if Diag < Up:
                    if Diag < Left:
                        M[i][j]= Diag
                    else:
                        M[i][j] = Left
                else:
                    if Up < Left:
                        M[i][j]= Up
                    else:
                        M[i][j] = Left
                op += 10#2 comparaison avec 2 variable chaque = 6 + on place une valeur dans notre tableau 4

        t1 = time.time()
        self.matrice = M
        temps = t1 - t0
        self.op += op
        return self.matrice[len(sequence_S)-1][len(sequence_T)-1], temps, self.op

    #Minimum local dans le cadran bas droite, de n par n, min étant la cellule minimum général
    def minimum_local(self,n, min):
        len_S = len(self.sequence_S)
        len_T = len(self.sequence_T)
        minimum_S = len_S
        minimum_T = len_T
        for i in range(len_S-n, len_S):
            for j in range(len_T - n, len_T):
                if self.matrice[i][j] < min :
                    min = self.matrice[i][j]
                    minimum_S = i
                    minimum_T = j

        return min, minimum_S, minimum_T