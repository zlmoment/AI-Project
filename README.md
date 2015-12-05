AI Project

University of Missouri - Columbia

~~Always win:

   python pacman.py -p ReflexAgent -l openClassic --frameTime 0

   python pacman.py -p ReflexAgent -l openClassic --frameTime 0 -g DirectionalGhost


~~Minimax Agent:
   
   胜率可以达到60% - 80%，符合初步要求
   
   python pacman.py -p MinimaxAgent -l minimaxClassic --frameTime 0 -a depth=4 -n 10 -q
  
~~Alpha-Beta Agent:

   用minimaxClassic测试 胜率同上，测试速度快了好多
   
   python pacman.py -p AlphaBetaAgent -l minimaxClassic --frameTime 0 -a depth=4 -n 10 -q
   
   用smallClassic测试：
   
   python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic --frameTime 0

   