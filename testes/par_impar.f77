PROGRAM PARIMPAR
INTEGER N, RESTO
PRINT *, 'Introduza um número:'
READ *, N

RESTO = MOD(N, 2)

IF (RESTO .EQ. 0) THEN
    PRINT *, 'O número é PAR.'
ELSE
    PRINT *, 'O número é IMPAR.'
ENDIF

END 