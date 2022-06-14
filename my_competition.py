

import sys
import datetime
from datetime import datetime



"""
Disscussion:

The most challenging aspect of the code were mainly the requirements found in the HD section of the specification. it took me a while to figure out how to 
write onto a text file ontop of the orginal information and reordering the table information after allready making the tables also proved tedius. That being said , to 
further imporve upon the code i would try to improve the readibility of the formatting by further separeting the table formation into seperate functions. Python libraries such 
as tabulate would also greatly imporve this code , as table formating makes up a large portion of the code lines. Additionally in order to save time 
i wrote and printed each table in the same methods, ideally i would do seperate these two functions.
"""


"""
Name: Matthew John Bentham
Student ID: S3923076
Completion level: HD

"""

class Competition:
    # I used an attribute called lines to save the information from the previous competition report so it can 
    # be written below the current one.
    lines = None

    # I saved a list of all the student and challenge objects as attributes in this class. I find indexing lists easier than dictionaries 
    # however a dictionary could also work
    def __init__(self,Students=[],Challenges=[]):
        self.Students = Students
        self.Challenges = Challenges

    def Beststudent(self):
        '''Computes the student with the highest average time
        '''
        current_no = 999999999
        best_student_Indx = 0
        
        for i,stu in enumerate(self.Students):
            # i used try loops to remove 444 from the avergae calculation 
            # to account for cases where a student has no in progress competitions
            try:
                results = stu.Results.copy()
                results.remove(444)
            except Exception:
                
                res = [i for i in results if type(i)==float]
                val = sum(res)/len(res)
                if val < current_no:
                    current_no = val
                    best_student_Indx = i
        best_student = [self.Students[best_student_Indx].ID,current_no]     
        return best_student
    
    def min_max(self,list,mm = 'min'):
        """simple method to compute the min or max of a list to 
        reduce code clutter 
        """
        if mm == 'min':
            m = min(list)
            indx = list.index(m)
        if mm == 'max':
            m = max(list)
            indx = list.index(m)
        return indx,m
    
    def Challengepnts(self):
        """Updates students wscore and score based on current results
        """
        Students = self.Students
        Challenges = self.Challenges
        for s in Students:
            indx,places = s.Placements(self)
            for i,p in enumerate(places):
                
                if p ==1:
                    s.Update_score(3)
                    s.Update_wscore(3*Challenges[indx[i]].Weight)
                if p ==2:
                    s.Update_score(2)
                    s.Update_wscore(2*Challenges[indx[i]].Weight)
                if p ==3:
                    s.Update_score(1)
                    s.Update_wscore(1*Challenges[indx[i]].Weight)
                if p == -1:
                    s.Update_score(-1)
                    s.Update_wscore(-1*Challenges[indx[i]].Weight)
        return
    


    def read_results(self,file_name,student_file=None):
        """Reads and stores information in the results and student files
        """

        # Results file:
        with open(file_name,"r") as txtfile:
            challenge_ids = []
            # Check if file is empty: i used read to check if there is anything in the 1 position to determine 
            #if file was empty
            one_char = txtfile.read(1)
            if not one_char:
                print('\nNO RESULTS AVAILABLE: Please check results file is not empty\n')
                exit()
            
            StudentIDs = []
            Studentresults = [[]]
            for i,line in enumerate(txtfile):
                currentline = line.split(",")
                strip_line = [item.strip() for item in currentline]
                # i used if commands and enumerate to determine which line the loop was up to
                # as it was the simplest solution 
                if i == 0:
                    Challenge_IDs = strip_line[0::]
                    for id in Challenge_IDs:
                        C = id
                        challenge_ids.append(C)
                        self.Challenges.append(Challenge(C))
                else:
                    StudentIDs.append(strip_line[0]) 
                    SR = strip_line[1::]
                    for w,result in enumerate(SR):
                        #I Used try and except loops for cases where non-numbers are
                        # present in the results file and an if else statement for 
                        # deal with tba or TBA cases 

                        try:
                             float(result)
                        except ValueError:
                            if result == 'TBA' or result == 'tba':
                                print('hi')
                                SR[w] = 444
                            else:
                                SR[w] = -1

                    Studentresults.append(SR)
                    self.Students.append(Student(strip_line[0],None,challenge_ids,SR))
                    
                    
        # Results file: STUDENT FILE
        if student_file != None:
            with open(student_file,'r') as file:
                self.Students = []
                # I used if statements to determine what subclass to make each student inserted the corresponding object into the students list 
                for row in file:
                    currentline = row.split(",")
                    strip_row = [item.strip() for item in currentline]
                    indx = StudentIDs.index(strip_row[0]) +1
                    if strip_row[2] == 'U':
                        S = Undergraduate(strip_row[0],strip_row[1],challenge_ids,Studentresults[indx])
                    if strip_row[2] =='P':
                        S = Postgraduate(strip_row[0],strip_row[1],challenge_ids,Studentresults[indx])
                    self.Students.append(S)
                txtfile.close()


    def display_results(self,files):
        '''Displays COMPETITION DASHBOARD and writes it to a txt file called 
        competition_report
        '''
        # GENERATE REQUIRED VARIABLES
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        s_no = len(self.Students)
        c_no = len(self.Challenges)
        topresult = self.Beststudent()
        # CONTENTS------------------------
        line1 = '\nCOMPETITION DASHBOARD'
        line2=['+','-'*12,'+']
        line3 = ['-'*6,'+']
        line4 = "{:<3} {:^8} {:>3}".format('|','Results','|')
        line8='There are %i students and %i challenges'%(s_no,c_no)
        line9='The top student is %s with an average time of %.2f minutes.'%(topresult[0],topresult[1])
        # DISPLAY-------------------------
        print(line1)
        print(*line2,end=' ')
        for i in range(0,c_no):
            print(*line3,end=' ')
        print('')
        print(line4,end=' ')
        
        for w in self.Students[0].Challenges:
            line5 = '{:^6} {:>1}'.format(w,'|')
            print(line5,end=' ')
        print('')
        print(*line2,end=' ')
        for i in range(0,c_no):
            print(*line3,end=' ')
        print('')
        for i in self.Students:
            ID = i.ID
            scores = i.Results
            for i,number in enumerate(scores):
                if number == -1:
                    scores[i] = ' '
                if number == 444:
                    scores[i] = '--'
            line6 = '{:<0} {:^12} {:>0}'.format('|',ID,'|')
            print(line6,end=' ')      
            for val in scores:
                line7 = '{:^6} {:>1}'.format(val,'|')
                print(line7,end=' ')
            print('')
        print(*line2,end=' ')
        for i in range(0,c_no):
            print(*line3,end=' ')
        print('')
        print(line8)
        print(line9)
        # WRITE TO FILE -------------------
        # I used try loop to determine the open format 
        # is i did not want to overwrite the file if 
        # it allready exists in the directory 
        try:
            open('competition_report.txt',"r")
            mode = 'r'
        except Exception:
            mode = 'w+'
        # I nested with statements so i could first read the prexisting file 
        # and save the information on it so i could then overwrite it and inserted
        # the old data at the bottom of the file --> i saved the old data as an attribute
        # in this class so i could call on it when writing the final table  
        with open('competition_report.txt',mode) as org:
            self.lines = org.read()
            with open('competition_report.txt',"w+") as txtfile:
                txtfile.write('-'*60)
                txtfile.write('Report generated on: %s'%date)
                txtfile.write('-'*60)
                txtfile.write(line1)
                txtfile.write('\n')
                txtfile.write(' '.join(line2))
                for i in range(0,c_no):
                    txtfile.write(' '.join(line3))  
                txtfile.write('\n')
                txtfile.write(line4)
                for w in self.Students[0].Challenges:
                    line5 = '{:^6} {:>1}'.format(w,'|')
                    txtfile.write(line5)
                txtfile.write('\n')
                txtfile.write(' '.join(line2))
                for i in range(0,c_no):
                    txtfile.write(' '.join(line3))
                txtfile.write('\n')
                # For all my tables i used .format and ^ in order to fromat the data in the center of each column 
                
                for i in self.Students:
                    ID = i.ID
                    scores = i.Results
                    line6 = '{:<0} {:^12} {:>0}'.format('|',ID,'|')
                    txtfile.write(line6)
                    for val in scores:
                        line7 = '{:^6} {:>1}'.format(val,'|')
                        txtfile.write(line7)
                    txtfile.write('\n')
                txtfile.write(' '.join(line2))
                for i in range(0,c_no):
                    txtfile.write(' '.join(line3))
                txtfile.write('\n')
                txtfile.write(line8)
                txtfile.write('\n')
                txtfile.write(line9)
                txtfile.write('\n')
                if len(files) == 1:
                    txtfile.writelines(self.lines)
                txtfile.close

    def read_challenges(self,file_name):
        """Reads challenges file as saves information in the challenge list attribute
        """
        with open(file_name,"r") as txtfile:
            
            self.Challenges = [0]*len(self.Students[0].Challenges)
            for line in txtfile:
                currentline = line.split(",")
                strip_line = [item.strip() for item in currentline]
                challenge_type = strip_line[1]
                # used if statements to detmine which subclass it belongs to so 
                # that i can save each student into the correct subclass
                if challenge_type == 'M':
                    C = MandatoryChallenge(strip_line[0],strip_line[2]+'(M)',strip_line[3])
                if challenge_type =='S':
                    C = SpecialChallenge(strip_line[0],strip_line[2]+'(S)',strip_line[3])
                challenge_indx = self.Students[0].Challenges.index(strip_line[0])
                self.Challenges[challenge_indx] = C      
            txtfile.close()

    def sorttable(self,sortitem,items ,tabletype,reverse=False):
        """ Sorts required lists based on the sort item--> this is done so that i can sort 
        items based on a specific variable (e.g. sort students based on highest to lowest w-score).
        Because this code is repeated and can be seperated from the table creation i decided to 
        place it in a seperate method to help with readability. 
        """
        item_sorted = sorted(sortitem,reverse=reverse)
        indxes = []
        count = 0
        for A in sortitem:
            indices = [i for i, x in enumerate(sortitem) if x == A]
            if len(indices) > 1:
                count += 1
                if count == (len(indices)):
                    count =0
                indxes.append(item_sorted.index(A)+count)
            else:
                indxes.append(item_sorted.index(A))
        item_slist=[]
        for item in items:
            item_s = [0]*len(tabletype)
            for i,ind in enumerate(indxes):
                item_s[ind]=item[i]
            item_slist.append(item_s)
        item_slist.append(item_sorted)
        return item_slist

    def Challengesummary(self,files):
        """Displays the CHALLENGE INFORMATION table and writes
        it to the competition_report file 
        """
        # GENERATE REQUIRED VARIABLES
        compfin = Challenge.Nofinished(self)
        Nongoing = Challenge.Nogoing(self)
        Averagetime = Challenge.Avgtime(self)
        maxtime = max(Averagetime)
        max_index = Averagetime.index(maxtime)
        S = self.sorttable(Averagetime,[compfin,Nongoing,self.Challenges],self.Challenges)
        # CONTENTS------------------------
        line1 = "\nCHALLENGE INFORMATION"
        line2= ['+','-'*12,'+','-'*18,'+','-'*10,'+','-'*10,'+','-'*10,'+','-'*18,'+']
        line3 = '{:<0} {:^11}  {:>0}   {:^14} {:>3} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^18} {:>0} '.format('|','Challenge','|','Name','|','Weight','|','Nfinish','|','Nongoing','|','AverageTime','|')
        line5 = 'The most difficult challenge is %s %s with an average time of %.2f minutes'%(self.Challenges[max_index].Name,self.Challenges[max_index].ID,maxtime)
        # DISPLAY-------------------------
        print(line1)
        print(*line2)
        print(line3)
        print(*line2)
        for i,challenge in enumerate(S[2]):
            line4 ='{:<0} {:^11}  {:>0}   {:^16} {:>0} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^18} {:>0} '.format('|',challenge.ID,'|',challenge.Name,'|',challenge.Weight,'|',S[0][i],'|',S[1][i],'|',S[3][i],'|')
            print(line4)
        print(*line2)
        print(line5)
        # WRITE TO FILE -------------------
        with open('competition_report.txt',"a+") as txtfile:
            txtfile.write(line1)
            txtfile.write('\n')
            txtfile.write(' '.join(line2))
            txtfile.write('\n')
            txtfile.write(line3)
            txtfile.write('\n')
            txtfile.write(' '.join(line2))
            txtfile.write('\n')
            for i,challenge in enumerate(S[2]):
                line4 ='{:<0} {:^11}  {:>0}   {:^16} {:>0} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^18} {:>0}'.format('|',challenge.ID,'|',challenge.Name,'|',challenge.Weight,'|',S[0][i],'|',S[1][i],'|',S[3][i],'|')
                txtfile.write(line4)
                txtfile.write('\n')
            txtfile.write(' '.join(line2))
            txtfile.write('\n')
            txtfile.write(line5)
            txtfile.write('\n')
            if len(files) ==2:
                txtfile.writelines(self.lines)
            txtfile.close()
            print('Report competition_report.txt generated!')

    def StudentSummary(self):
        """Displays the STUDENT INFORMATION table and writes
        it to the competition_report file 
        """
        # GENERATE REQUIRED VARIABLES
        # Update student scores:
        self.Challengepnts()
        # In order to sort each student by their w-score i calculated all the scores 
        # and averages required , placed them in indivdual lists and use thed the sorttable 
        # method to sort them in the correct order.
        Avgs = []
        wscores = []
        scores = []
        names = []
        ts = []
        Nofs = []
        Ngs = []
        for Student in self.Students:
            Nofs.append(Student.NoFinished())
            Avg = Student.Avgtime()
            Avgs.append(Avg)
            wscores.append(Student.Wscore)
            scores.append(Student.Score)
            Ngs.append(Student.Noongoing())
            check = Student.Meetrequirements(self)
            if type(Student) == Postgraduate:
                ts.append('P')
            if type(Student) == Undergraduate:
                ts.append('U')
            # i created a names list to save the altered names in cases where a student 
            # did not meet thier competition requirements 
            if check == False:
                names.append('!'+Student.Name)
            else:
                names.append(Student.Name)
        S = self.sorttable(wscores,[ts,names,Nofs,Avgs,Ngs,self.Students],self.Students,reverse=True)
        indx, fastest = self.min_max(Avgs,'min')
        indx1, score = self.min_max(scores,'max')
        indx2, wscore = self.min_max(wscores,'max')
    
        # CONTENTS------------------------
        line1 = '\nSTUDENT INFORMATION'
        line2 = ['+','-'*14,'+','-'*10,'+','-'*10,'+','-'*10,'+','-'*10,'+','-'*18,'+','-'*10,'+','-'*10,'+']
        line3 = '{:<0} {:^14} {:>0} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^18} {:>0} {:^10} {:>0} {:^11}{:>0} '.format('|','StudentID','|','Name','|','Type','|','Nfinish','|','Nongoing','|','AverageTime','|','Score','|','Wscore','|')
        line5 = 'The student with the fastest average time is %s (%s) with an average time of %.2f minutes.'%(self.Students[indx].ID,self.Students[indx].Name,fastest)
        line6 = 'The student with the highest score is %s (%s) with a score of %.2f.'%(self.Students[indx1].ID,self.Students[indx1].Name,score)
        line7 = 'The student with the highest weighted score is %s (%s) with a weighted score of %.2f.'%(self.Students[indx2].ID,self.Students[indx2].Name,wscore)
        # DISPLAY-------------------------
        print(line1)
        print(*line2)
        print(line3)
        print(*line2)
        for i,Student in enumerate(S[5]):
            line4 ='{:<0} {:^14} {:>0} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^7} {:>0} {:^18} {:>0} {:^10} {:>0} {:^11}{:>0} '.format('|',Student.ID,'|',S[1][i],'|',S[0][i],'|',S[2][i],'|',S[4][i],'   |',S[3][i],'|',Student.Score,'|',Student.Wscore,'|')
            print(line4)
        print(*line2)
        print(line5)
        print(line6)
        print(line7)
        # WRITE TO FILE -------------------
        with open('competition_report.txt',"a") as txtfile:
            txtfile.write(line1)
            txtfile.write('\n')
            txtfile.write(' '.join(line2))
            txtfile.write('\n')
            txtfile.write(line3)
            txtfile.write('\n')
            txtfile.write(' '.join(line2))
            txtfile.write('\n')
            for i,Student in enumerate(S[5]):
                line4 ='{:<0} {:^14} {:>0} {:^10} {:>0} {:^10} {:>0} {:^10} {:>0} {:^7} {:>0} {:^18} {:>0} {:^10} {:>0} {:^11}{:>0} '.format('|',Student.ID,'|',S[1][i],'|',S[0][i],'|',S[2][i],'|',S[4][i],'   |',S[3][i],'|',Student.Score,'|',Student.Wscore,'|')
                txtfile.write(line4)
                txtfile.write('\n')
            txtfile.write(' '.join(line2))
            txtfile.write('\n')
            txtfile.write(line5)
            txtfile.write('\n')
            txtfile.write(line6)
            txtfile.write('\n')
            txtfile.write(line7)
            txtfile.write('\n')
            txtfile.writelines(self.lines)
            txtfile.close()
            print('Report competition_report.txt generated!')

    def check_file(self,files):
        '''Checks if all required files are entered into the command line and 
        if each file has the correct format , in cases where an error occurs
        the user is notified which file caused it.
        '''
        # i used if statements to check files based in wether it was inputed as a command line argument 
        if len(files) >= 1:
            try:
                open(files[0],'r')
            except Exception:
                print('\nResults file cannot be found\n')
                exit()
        if len(files) >= 2:
            try:
                open(files[1],'r')
            except Exception:
                print('\nChallenges file cannot be found\n')
                exit()
        if len(files) >= 3:
            try:
                open(files[2],'r')
            except Exception:
                print('\nStudents file cannot be found\n')
                exit()
        
        # Check results file format:
        # to check ach file format i used nested if satements to determine if the files contain:
        # - the correct number of columns
        # - correct data type entered 
        # - all challenge and student ids are unique and have the right format 
        # - all mandatory challenges have the same weight 
        # RESULTS FILE CHECK 
        if len(files) >=1:
            with open(files[0],'r') as txtfile:
                cids= []
                sids = []
                check2 = True
                for i,line in enumerate(txtfile):
                    currentline = line.split(",")
                    strip_line= [item.strip() for item in currentline]
                    check1 = len(strip_line) == 6
                    
                    if i == 0:
                        for id in strip_line[1::]:
                            
                            cids.append(id)
                            if id[0] != 'C':
                                check2 = False
                            else:
                                try:
                                    int(id[1::])
                                except ValueError:
                                    check2 = False
                    else:
                        sids.append(strip_line[0])
                        if strip_line[0][0] != 'S':
                                check2 = False
                        else:
                            try:
                                int(strip_line[0][1::])
                            except ValueError:
                                
                                check2 = False
                check3= len(cids) == len(set(cids))
                check4 = len(sids) == len(set(sids))
                if check1 == False or check2 == False or check3 == False or check4 ==False:
                    print('+','-'*60,'+')
                    print('\nERROR: formatting issues found in results file\n ')
                    print('+','-'*60,'+')
                    exit()

        # Check Challenges file format:
        # made sure all ids in challenges files are the same as the ids in the results file 
        if len(files) >=2:
            with open(files[1],'r') as txtfile:
                cidsC= []
                mweights = []
                check2 = True
                for i,line in enumerate(txtfile):
                    currentline = line.split(",")
                    strip_line= [item.strip() for item in currentline]
                    check1 = len(strip_line) == 4
                    
                    cidsC.append(strip_line[0])
                    if strip_line[1] =='M':
                        mweights.append(strip_line[3])
                    if strip_line[1] != 'M' and strip_line[1] != 'S':
                        check2 =False
                    if strip_line[0][0] != 'C':
                            check2 = False
                    else:
                        try:
                            int(strip_line[0][1::])
                            float(strip_line[3])
                            
                        except ValueError:  
                            check2 = False
                check3= len(cidsC) == len(set(cidsC))
                
                check5 = sorted(cids)==sorted(cidsC)
                check4 = len(set(mweights)) ==1
                if check1 == False or check2 == False or check3 == False or check4 == False or check5 == False:
                    print('+','-'*60,'+')
                    print('\nERROR: formatting issues found in challenges file\n ')
                    print('+','-'*60,'+')
                    exit()
        if len(files) >=3:
        # Check students file format:
        # made sure all the ids in the students file is the same as the id in the challenges file
            with open(files[2],'r') as txtfile:
                sidsS= []
                check2 = True
                for i,line in enumerate(txtfile):
                    currentline = line.split(",")
                    strip_line= [item.strip() for item in currentline]
                    check1 = len(strip_line) == 3
                    sidsS.append(strip_line[0])
                    if strip_line[0][0] != 'S':
                            check2 = False
                    else:
                        try:
                            int(strip_line[0][1::])
                        except ValueError:  
                            check2 = False
                check3= len(sidsS) == len(set(sidsS))
                check4 = sorted(sidsS) == sorted(sids)
                if check1 == False or check2 == False or check3 == False or check4 == False:
                    print('+','-'*60,'+')
                    print('\nERROR: formatting issues found in students file\n ')
                    print('+','-'*60,'+')
                    exit()
            
                              

class Student:
    # Constructor: 
    def __init__(self,ID,Name,Challenges,Results,Score=0,Wscore=0):
        self.ID = ID
        self.Name = Name
        self.Challenges = Challenges
        self.Results = [float(i) for i in Results]
        self.Score = Score
        self.Wscore=Wscore

    #METHODS:
    def Meetrequirements(self,comp):
        '''Checks if a student has completed all mandatory challeneges'''
        challenges = comp.Challenges
        Met = True
        for i,challenge in enumerate(challenges):
            if type(challenge) == MandatoryChallenge:
                if self.Results[i] == '--' or self.Results[i] == ' ':
                    Met = False
        return Met

    def NoFinished(self):
        '''Calculates the total number of challenges a student has completed
        '''
        Results = self.Results
        count = 0 
        for Result in Results:
            if Result != 444 and Result != -1:
                count +=1
        return count

    def Noongoing(self):
        """Calculates the total number of ongoing challenges for a student 
        """
        Results = self.Results
        count = 0 
        for Result in Results:
            if  Result == 444:
                count +=1
        return count

    def Avgtime(self):
        """Calculates the average time a student takes to 
        over all completed challenges 
        """
        Results = self.Results
        Cleaned_res = [i for i in Results if type(i)==float and i !=-1 and i !=444]
        Avg = round(sum(Cleaned_res)/len(Cleaned_res),2)
        return Avg

    def Update_score(self,score):
        """Setter function to update student score
        """
        self.Score = self.Score + score
        return self.Score
    def Update_wscore(self,score):
        """Setter function to update student w score
        """
        self.Wscore = self.Wscore + score
        return self.Wscore
    def Placements(self,comp):
        """This function is used to determie where a student places in a given compeition 
        """
        Students = comp.Students
        s_indx = Students.index(self)
        c_results = []
        placements = []
        c_indx = []
        # i used one for loop to save all the results for a given challenge , 
        # used nested ifs to exclude challeneges that have not been completed by all students ,
        # then a foor loop to get the index of those challeneges , 
        # then if statments follwed by del to determine the placements of each student  
        for i in range(0,len(self.Challenges)):
            res = []
            for student in Students:
                res.append(student.Results[i])
            c_results.append(res)
            
        c_cleaned=[i for i in c_results if len(i) == len([w for w in i if type(w)==float])]
        c_cleaned = [i for i in c_cleaned if len(i) == len([w for w in i if w != 444 and w!=-1])]
        for c in c_cleaned:
            c_indx.append(c_results.index(c))
        # del is used after each min() command so that the second and third smallest times 
        # can be found by subsequent min() commands

        for c in c_cleaned:
            d = c.copy()
            if len(c) > 3:
                if c[s_indx] == max(c):
                    placements.append(-1)
            if c[s_indx] == min(c):
                placements.append(1)
            del d[d.index(min(d))]
            if c[s_indx] == min(d):
                placements.append(2)
            del d[d.index(min(d))]
            if c[s_indx] == min(d):
                placements.append(3)
        return c_indx, placements
            
# I created two seperate child classes of the Student class --> Undergraduate and Postgraduate
# so that the additional requirements of these classes can be computed without the needing to 
#redo all the above methods.

   
class Undergraduate(Student):
    # Only additional requirment for undergraduate class is that the meetrequirements method is altered 
    # so that the student also has to complete one special challenge in addition to the compulsory challenges 
    def __init__(self,ID,Name, Challenges, Results,Score=0,Wscore=0):
        super().__init__(ID, Name,Challenges, Results,Score,Wscore)
    
    def Meetrequirements(self, comp):
        challenges = comp.Challenges
        Met = True
        count = 0
        for i,challenge in enumerate(challenges):
            if type(challenge) == SpecialChallenge:
                if self.Results[i] != '--' and self.Results[i] != ' ':
                    count += 1 
        if count >= 1:
            Met = super().Meetrequirements(comp)
        else: 
            Met = False
        return Met


class Postgraduate(Student):
    # Only additional requirment for undergraduate class is that the meetrequirements method is altered 
    # so that the student also has to complete two special challenge in addition to the compulsory challenges 

    def __init__(self, ID,Name, Challenges, Results,Score=0,Wscore=0):
        super().__init__(ID,Name ,Challenges, Results,Score,Wscore)
    
    def Meetrequirements(self, comp):
        challenges = comp.Challenges
        Met = True
        count = 0
        for i,challenge in enumerate(challenges):
            if type(challenge) == SpecialChallenge:
                if self.Results[i] != '--' and self.Results[i] != ' ':
                    count += 1
        if count >= 2:
            Met = super().Meetrequirements(comp)
        else: 
            Met = False
        return Met

        

class Challenge:
    #Constructor
    def __init__(self,ID,Name=None,Weight=0):
        self.ID = ID
        self.Name = Name
        self.Weight = float(Weight)

    @property
    # getter function for weight
    def get_Weight(self):
        return self.Weight
    # setter function for weight
    def set_Weight(self, Weight):
        self.Weight = round(float(Weight),2)
    # getter function for name
    @property
    def get_Name(self):
        return self.Name
   # setter function for name
    def set_Name(self, Name):
        self.Name = Name


# In order to compute varibales such as averages , Number finished , number on going throughout all my code 
# i merely saved all the data in 2D lists , for challeneges each list within the list correspond to each challenge 
# and for student calculations each list corresponds to a student. This could also be done with 2d dictionaries however i find 2d lists 
# esdier to work with. 

    def Nofinished(comp):
        """Computes the number students that have completed each challenge 
        """
        Students = comp.Students
        Challenge = Students[0].Challenges
        compfin = [0]*len(Challenge)
        for student in Students:
            for i,result in enumerate(student.Results):
                if type(result) == float:
                    compfin[i] += 1
        return compfin

    def Nogoing(comp):
        """Computes the number of students that are currently still 
        undergoing each challenge 
        """
        Students = comp.Students
        Challenge = Students[0].Challenges
        Nongoing = [0]*len(Challenge)
        for student in Students:
            for i,result in enumerate(student.Results):
                if result == '--':
                    Nongoing[i] += 1
        return Nongoing

    def Avgtime(comp):
        """Computes the average time students have spent on each challenge 
        """
        Students = comp.Students
        avgs = [0]*len(Students[0].Challenges)
        for i in range(0,len(Students[0].Challenges)):
            res = []
            for student in Students:
                res.append(student.Results[i])
            results = [i for i in res if type(i)==float and i != -1 and i != 444]
            # used if statement to account for cases where no students have completed a challenge 
            if len(results) == 0:
                avg = 0
            else:
                avg = sum(results)/len(results)
            avgs[i] = round(avg,2)
        return avgs


# I created two seperate child classes of the Challenge class --> Mandatory challenge and special challenge 
# so that the additional requirements of these classes can be computed without the needing to 
#redo all the above methods.

class MandatoryChallenge(Challenge):
    """ only additional requirements is that the default weight is 1.0
    """
    Weight = 1.0
    def __init__(self, ID, Name,Weight=Weight):
        super().__init__(ID, Name, Weight)   
    
class SpecialChallenge(Challenge):
    """ only additional requirements is that the weight must be 1.0 or larger
    """
    def __init__(self, ID, Name, Weight):
        super().__init__(ID, Name, Weight)

    
    def set_Weight(self,Weight):
        if float(Weight) <= 1:
            print("Weight must be larger than 1.0")
        else:
            super().set_Weight(self,Weight)
    

# I used class Main in order to call the competition class and run the respective methods 
# required for the function to run
class Main:
    Comp = Competition()
    files =[]
    # A for loop and sys.argv was to used to extract the command line
    # arguments as 
    for i,file in enumerate(sys.argv):
        if i != 0:
            files.append(file)
    
    # In order to accept the different number of command line inputs and only print out the respective tables i used 
    # if statements to check the length of the sys.argv list and read/display only the relevant information 
    Comp.check_file(files)
    if len(files) >=1:
        # READ RESULTS:
        Comp.read_results(files[0])
        # DISPLAY RESULTS
        Comp.display_results(files)
    if len(files) >=2:
        # READ CHALLANGES:
        Comp.read_challenges(files[1])
        # challange Summary:
        Comp.Challengesummary(files)
    if len(files)>=3:
        Comp.read_results(files[0],files[2])
        # student summary
        Comp.StudentSummary()
    
    
    
