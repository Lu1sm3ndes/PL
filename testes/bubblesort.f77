PROGRAM BUBBLE
INTEGER ARR(5)
INTEGER I, J, TEMP, LIMITE

ARR(1) = 40
ARR(2) = 10
ARR(3) = 50
ARR(4) = 20
ARR(5) = 30

! 1. Separar o texto das variáveis com vírgulas e adicionar espaços!
PRINT *, '--- BUBBLE SORT EM FORTRAN ---'
PRINT *, 'ARRAY INICIAL: [ ', ARR(1), ', ', ARR(2), ', ', ARR(3), ', ', ARR(4), ', ', ARR(5), ' ]'
PRINT *, ' ' ! Imprime uma linha em branco

PRINT *, 'A ORDENAR O ARRAY...'
PRINT *, ' ' ! Imprime outra linha em branco

DO 10 I = 1, 4
    LIMITE = 5 - I
    DO 20 J = 1, LIMITE
        IF (ARR(J) .GT. ARR(J+1)) THEN
            ! Troca os valores (Swap)
            TEMP = ARR(J)
            ARR(J) = ARR(J+1)
            ARR(J+1) = TEMP
        ENDIF
    20 CONTINUE
10 CONTINUE

! 2. Imprimir o array ordenado com o número da posição
PRINT *, '--- RESULTADO ---'
PRINT *, 'ARRAY ORDENADO: [ ', ARR(1), ', ', ARR(2), ', ', ARR(3), ', ', ARR(4), ', ', ARR(5), ' ]'
END