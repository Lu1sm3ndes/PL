
PROGRAM MATH
INTEGER A, B, C, RES1, RES2

A = 10
B = 5
C = 2

PRINT *, '--- TESTE DE PRECEDENCIA MATEMATICA ---'
PRINT *, 'VALORES: A = 10, B = 5, C = 2'
PRINT *, ' '

! EXPRESSAO 1: Sem parenteses
! O compilador tem de saber fazer primeiro as multiplicacoes/divisoes:
! 10 + (5 * 2) - (10 / 2) = 10 + 10 - 5 = 15
RES1 = A + B * C - A / C

PRINT *, 'TESTE 1: Sem parenteses'
PRINT *, 'CONTA: A + B * C - A / C'
PRINT *, 'ESPERADO: 15'
PRINT *, 'OBTIDO:   ', RES1
PRINT *, ' '

! EXPRESSAO 2: Com parenteses
! O compilador tem de resolver primeiro os parenteses:
! (10 + 5) * 2 - (10 / 2) = 15 * 2 - 5 = 30 - 5 = 25
RES2 = (A + B) * C - A / C

PRINT *, 'TESTE 2: Com parenteses'
PRINT *, 'CONTA: (A + B) * C - A / C'
PRINT *, 'ESPERADO: 25'
PRINT *, 'OBTIDO:   ', RES2

END