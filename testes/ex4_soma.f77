PROGRAM SOMAARR
INTEGER NUMS(5)
INTEGER I, SOMA
SOMA = 0
PRINT *, 'Introduza 5 números inteiros, um de cada vez:'
DO 30 I = 1, 5
    READ *, NUMS(I)
    SOMA = SOMA + NUMS(I)
30 CONTINUE
PRINT *, 'A soma dos números é: ', SOMA
END