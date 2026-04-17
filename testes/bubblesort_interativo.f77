PROGRAM BUBBLEINT
! Criamos um "buffer" de 50 posições para garantir que há espaço
INTEGER ARR(50)
INTEGER N, I, J, TEMP, LIMITE, MAXOUT

PRINT *, '--- BUBBLE SORT INTERATIVO ---'
PRINT *, 'QUANTOS NUMEROS QUER ORDENAR? (MAX 50):'
READ *, N

PRINT *, 'INTRODUZA OS ', N, ' NUMEROS (UM DE CADA VEZ):'
DO 10 I = 1, N
    READ *, ARR(I)
10 CONTINUE

PRINT *, ' '
PRINT *, '--- ESTADO INICIAL ---'
DO 15 I = 1, N
    PRINT *, 'Posicao ', I, ' : ', ARR(I)
15 CONTINUE
PRINT *, ' '

PRINT *, 'A ORDENAR O ARRAY...'
PRINT *, ' '

! A matemática do Bubble Sort ajustada para N elementos
MAXOUT = N - 1
DO 20 I = 1, MAXOUT
    LIMITE = N - I
    DO 30 J = 1, LIMITE
        IF (ARR(J) .GT. ARR(J+1)) THEN
            ! Troca os valores (Swap)
            TEMP = ARR(J)
            ARR(J) = ARR(J+1)
            ARR(J+1) = TEMP
        ENDIF
    30 CONTINUE
20 CONTINUE

PRINT *, '--- RESULTADO FINAL ---'
PRINT *, 'ARRAY ORDENADO:'
DO 40 I = 1, N
    PRINT *, '[', I, '] -> ', ARR(I)
40 CONTINUE
END