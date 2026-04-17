PROGRAM MATHINT
INTEGER A, B, C, RES1, RES2

PRINT *, '--- TESTE INTERATIVO DE PRECEDENCIA MATEMATICA ---'
PRINT *, 'INTRODUZA O VALOR DE A:'
READ *, A

PRINT *, 'INTRODUZA O VALOR DE B:'
READ *, B

PRINT *, 'INTRODUZA O VALOR DE C (Diferente de zero!):'
READ *, C

PRINT *, ' '
PRINT *, 'VALORES ESCOLHIDOS: A = ', A, ', B = ', B, ', C = ', C
PRINT *, ' '

! EXPRESSAO 1: Sem parenteses
! O compilador tem de saber fazer primeiro as multiplicacoes/divisoes:
! A + (B * C) - (A / C)
RES1 = A + B * C - A / C

PRINT *, 'TESTE 1: Sem parenteses'
PRINT *, 'CONTA: A + B * C - A / C'
PRINT *, 'OBTIDO:   ', RES1
PRINT *, ' '

! EXPRESSAO 2: Com parenteses
! O compilador tem de resolver primeiro os parenteses:
! (A + B) * C - (A / C)
RES2 = (A + B) * C - A / C

PRINT *, 'TESTE 2: Com parenteses'
PRINT *, 'CONTA: (A + B) * C - A / C'
PRINT *, 'OBTIDO:   ', RES2

END