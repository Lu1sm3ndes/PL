PROGRAM FIBO
INTEGER TERMOS, T1, T2, PROX, I

PRINT *, 'Quantos termos da serie de Fibonacci pretende ver?'
READ *, TERMOS

T1 = 0
T2 = 1

PRINT *, 'Série:'
PRINT *, T1
PRINT *, T2

DO 10 I = 3, TERMOS
    PROX = T1 + T2
    PRINT *, PROX
    
    ! Troca de variaveis para a proxima iteracao
    T1 = T2
    T2 = PROX
10 CONTINUE

END