# my_competition

Objected oreintated python program that generates a competition report with  results , students an challenges files as command line arguments into order to generate the respective tables in the competition_report.txt

**NOTE:** files must be supplied in correct order (results , challenges then students) 
### FILES
- challenegs.txt: sample file showing correct format of challenges file input (ID , challenge type , Name , weight)
- results.txt: sample file showing correct format of challenges file input : matrix showing time it took each student completed a challenge (-1/any string = not completed , 'tba'/'TBA'/444 = in progress)
- students.txt: sample file showing correct format of challenges file input (ID , Name , student type)
- Class diagram.pdf: class diagram of classes present in the program 
- compeition_report.txt: sample output file that gets appeneded from top of file with curret date and time everytime the program is run 


example if results file is suplied:
COMPETITION DASHBOARD
+ ------------ +------ +------ +------ +------ +------ +
|   Results    | C03   | C04   | C09   | C12   | C15   |
+ ------------ +------ +------ +------ +------ +------ +
|     S001     | 12.5  | 6.8   | 17.6  |  --   |       |
|     S052     | 10.6  | 7.0   | 20.1  |       |  --   |
|     S125     | 9.4   | 6.2   | 18.2  |       |       |
|     S098     | 13.8  |       | 19.5  | 25.3  |  --   |
|     S246     | 9.9   | 5.9   | 17.9  | 20.1  |       |
|     S012     | 11.2  |  --   | 19.5  |       |       |
+ ------------ +------ +------ +------ +------ +------ +
There are 6 students and 5 challenges
The top student is S125 with an average time of 6.36 minutes.

example if challenge file is suplied:

CHALLENGE INFORMATION
+ ------------ + ------------------ + ---------- + ---------- + ---------- + ------------------ +
|  Challenge   |        Name        |   Weight   |  Nfinish   |  Nongoing  |    AverageTime     | 
+ ------------ + ------------------ + ---------- + ---------- + ---------- + ------------------ +
|     C15      |      Select(M)     |    1.0     |     0      |     2      |         0          |
|     C04      |       Sort(M)      |    1.0     |     4      |     1      |        6.47        |
|     C03      |      Search(M)     |    1.0     |     6      |     0      |       11.23        |
|     C09      |    Compression(S)  |    1.0     |     6      |     0      |        18.8        |
|     C12      |       Vote(S)      |    2.0     |     2      |     1      |        22.7        |
+ ------------ + ------------------ + ---------- + ---------- + ---------- + ------------------ +
The most difficult challenge is Vote(S) C12 with an average time of 22.70 minutes

example if student file is supplied:
STUDENT INFORMATION
+ -------------- + ---------- + ---------- + ---------- + ---------- + ------------------ + ---------- + ---------- +
|   StudentID    |    Name    |    Type    |  Nfinish   |  Nongoing  |    AverageTime     |   Score    |   Wscore   | 
+ -------------- + ---------- + ---------- + ---------- + ---------- + ------------------ + ---------- + ---------- +
|      S246      |   Louise   |     U      |     4      |    0       |       13.45        |     4      |     4.0    | 
|      S125      |    Tim     |     U      |     3      |    0       |       11.27        |     4      |     4.0    | 
|      S001      |    John    |     U      |     3      |    1       |        12.3        |     3      |     3.0    | 
|      S052      |    Mary    |     P      |     3      |    1       |       12.57        |     0      |     0.0    | 
|      S012      |   Harry    |     P      |     2      |    1       |       15.35        |     0      |      0     | 
|      S098      |   Scott    |     P      |     3      |    1       |       19.53        |     -1     |    -1.0    | 
+ -------------- + ---------- + ---------- + ---------- + ---------- + ------------------ + ---------- + ---------- +
The student with the fastest average time is S125 (Tim) with an average time of 11.27 minutes.
The student with the highest score is S125 (Tim) with a score of 4.00.
The student with the highest weighted score is S125 (Tim) with a weighted score of 4.00.
