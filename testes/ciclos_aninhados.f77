PROGRAM ANINHADO
INTEGER I, J
PRINT *, 'Coordenadas da Matriz 3x2:'

DO 10 I = 1, 3
    DO 20 J = 1, 2
        PRINT *, 'Linha ', I, ' Coluna ', J
20  CONTINUE
10 CONTINUE

PRINT *, 'Fim da Matriz!'
END