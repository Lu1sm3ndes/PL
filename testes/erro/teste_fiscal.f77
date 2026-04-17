PROGRAM TESTEFISCAL
INTEGER NORMAL
INTEGER LISTA(5)

PRINT *, 'A TESTAR O FISCAL SEMANTICO...'

! ERRO 1: Tentar escrever numa variável normal como se fosse array
NORMAL(2) = 100

! ERRO 2: Tentar ler de uma variável normal como se fosse array
PRINT *, NORMAL(3)

END