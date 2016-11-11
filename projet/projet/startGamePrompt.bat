@echo off

set /p J1=Entrer le joueur 1 :
set /p J2=Entrer le joueur 2 :

python mainServer.py %J1% %J2%