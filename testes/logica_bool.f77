PROGRAM LOGICA
INTEGER IDADE
LOGICAL MAIOR, MENOR, ATIVO

PRINT *, 'Introduza a sua idade:'
READ *, IDADE

! Avalia as condicoes relacionais
MAIOR = IDADE .GE. 18
MENOR = IDADE .LT. 65

! Junta tudo com um AND
ATIVO = MAIOR .AND. MENOR

IF (ATIVO) THEN
    PRINT *, 'A pessoa é um adulto em idade ativa!'
ELSE
    PRINT *, 'A pessoa é dependente ou reformada.'
ENDIF

END