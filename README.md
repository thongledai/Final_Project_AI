# Final_Project_AI
AI search algorithms project

Ví dụ state:
state = [[3, 3, 2, 2],    	# lọ 0
         [2, 1, 3   ],      # lọ 1
         [3, 2      ],      # lọ 2
         [1, 1,1    ]]      # lọ 3

START = [[1, 3, 2, 2],    	# lọ 0
         [3, 2, 1, 3],      # lọ 1
         [3, 2, 1, 1],      # lọ 2
         [          ]]      # lọ 3

GOAL = [[1, 1, 1, 1],       # lọ 0
        [2, 2, 2, 2],       # lọ 1
        [3, 3, 3, 3],       # lọ 2
        [          ]]       # lọ 3
GOAL=A(3,4)=24 (vì số cách sắp xếp 3 màu khác nhau vào 4 lọ là chỉnh hợp chập 3 của 4 phần tử)

Điều kiện: (để thực hiện được đổ mực lọ này vào lọ kia thì:)
Tầng trên cùng của cả 2 lọ phải cùng số. 
Lọ được đổ phải bé hơn 4 giá trị (còn chỗ trống). 
Lọ nguồn phải chứa ít nhất 1 màu (không được toàn số 0). 
Không được đổ từ một lọ sang chính nó. 
Chỉ được đổ một đoạn màu liên tiếp ở trên cùng của lọ nguồn. 
Nếu lọ đích hoàn toàn rỗng thì có thể nhận bất kỳ màu nào từ lọ nguồn. 
Số lượng ô màu được đổ không được vượt quá:
        Số ô cùng màu liên tiếp trên cùng của lọ nguồn.
        Số ô còn trống của lọ đích.

Kết quả:
Sau khi đổ, các ô vừa lấy khỏi lọ sẽ thành rỗng. 
Sau khi đổ, các ô trống trên cùng của lọ đích được thay bằng màu vừa đổ. 
Một trạng thái được coi là hợp lệ nếu mỗi lọ luôn có giá trị:[1,3] hoặc rỗng
Trạng thái đích đạt được khi mỗi lọ:
        hoặc là cùng màu và đầy lọ 
        hoặc là rỗng
Chi phí của mỗi lần đổ được tính là 1. 

Cấu trúc thư mục:
1.UninformedSearch:
BreadthFirstSearch.py
DepthFirstSearch.py
IterativeDeepeningSearch.py
UniformCostSearch.py

2.InformedSearch:
AStarSearch.py (A*)
GreedySearch.py
IterativeDeepeningAStarSearch.py (IDA*)

3.LocalSearch:
HillClimbingSearch:
Simple.py
Stochastic.py
SteepestAscent.py
RandomRestart.py
LocalBeamSearch.py
SimulatedAnnealingSearch.py

4.SearchingInComplexEnvironments:
AndOrGraphSearch.py
UnobservableSearch:
BeliefStateSearch.py
PartiallyObservableSearch:
BeliefStateSearch.py

5.ConstraintSatisfactionProblems:
BacktrackingSearch.py
ForwardCheckingSearch.py
AC3Search.py
MinConflictSearch.py

6.AdversarialSearch:
MinimaxSearch.py
AlphaBetaSearch.py
ExpectimaxSearch.py
