PROGRAM CADEIAINT
INTEGER VALOR, RESULT

PRINT *, '--- TESTE DE STACKS ---'
PRINT *, 'INTRODUZA UM NUMERO PARA TESTAR AS FUNCOES:'
READ *, VALOR

PRINT *, 'MAIN: A chamar FUNC1 com valor: ', VALOR
RESULT = FUNC1(VALOR)

PRINT *, ' '
PRINT *, 'MAIN: De volta ao programa principal!'
PRINT *, 'MAIN: RESULTADO FINAL: ', RESULT
END

INTEGER FUNCTION FUNC1(X)
INTEGER X, DOBRO, FUNC2
PRINT *, '  -> FUNC1: Recebi o valor ', X
PRINT *, '  -> FUNC1: A chamar FUNC2 para dobrar o valor...'

DOBRO = FUNC2(X)

PRINT *, '  -> FUNC1: A FUNC2 devolveu o valor ', DOBRO
PRINT *, '  -> FUNC1: A somar 10 ao resultado e a regressar...'
FUNC1 = DOBRO + 10
RETURN
END

INTEGER FUNCTION FUNC2(Y)
INTEGER Y
PRINT *, '    -> FUNC2: Recebi o valor ', Y
PRINT *, '    -> FUNC2: A calcular o dobro...'
FUNC2 = Y * 2
RETURN
END