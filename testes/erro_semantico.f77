PROGRAM ERROSEM
INTEGER X
LOGICAL FLAG

FLAG = .TRUE.
! O compilador tem de dar erro aqui:
X = FLAG + 10

PRINT *, X
END