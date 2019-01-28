'''
Created on Nov 11, 2018

@author: ritesh
'''

from bs4 import BeautifulSoup
import requests
from espncricinfo.match import Match
from gtts import gTTS
import os
import speech_recognition as sr



cache1=""   #to hold team1 in cache
cache2=""   #to hold team2 in cache


#data request will collect all the html tags from cricinfo website
def data_request():
    url = "http://static.cricinfo.com/rss/livescores.xml"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features="html.parser")
    return soup

#get_matchliinks will fetch all matchlinks currently going on
def get_matchlinks(soup):
    
    data=soup.find_all("guid")
    match_links=[]
    for i in data:
        match_links.append(i.get_text())
    return match_links

#match_id to fetch all matchids currently going on
def get_match_id(soup):
    country_list=["AFGHANISTAN","AUSTRALIA","BANGLADESH","ENGLAND","INDIA","IRELAND","NEW ZEALAND","PAKISTAN","SOUTH AFRICA", "SRI LANKA", "WEST INDIES","ZIMBABWE","KENYA","SCOTLAND","UAE"]
    
    data=soup.find_all("description")
    data=data[1:]
    matchid=[]
    data1=soup.find_all("guid")
    for j in range(0,len(data)):
        
        for i in range(0,len(data[j].get_text())):
            if (ord(data[j].get_text()[i])>=48 and ord(data[j].get_text()[i])<=57) or data[j].get_text()[i-1:i+2]==" v ":
                endpoint=i-1
                break
        if  data[j].get_text()[0:endpoint].upper() in country_list and " A " not in data[j].get_text() and "Women" not in data[j].get_text():   
            
            matchid.append(data1[j].get_text()
                            [data1[j].get_text().find("match/")+6:data1[j].get_text().find(".html")])

    return matchid


#get_teamlist1 will collect all team1 in a list
def get_teamlist1(soup): 
    teamlist1=[]
    
    match_id=get_match_id(soup)
    
    country_list=["AFGHANISTAN","AUSTRALIA","BANGLADESH","ENGLAND","INDIA","IRELAND","NEW ZEALAND","PAKISTAN","SOUTH AFRICA", "SRI LANKA", "WEST INDIES","ZIMBABWE","KENYA","SCOTLAND","UAE"]
    
 
    
    for j in match_id:
        t1=Match(j).team_1_abbreviation
        
        if t1=='AFG':
            teamlist1.append("AFGHANISTAN")
        elif t1=='AUS':
            teamlist1.append("AUSTRALIA")
        elif t1=='BAN':
            teamlist1.append("BANGLADESH")
        elif t1=='ENG':
            teamlist1.append("ENGLAND")
        elif t1=='IND':
            teamlist1.append("INDIA")
        elif t1=='IRE' or t1=='IRL':
            teamlist1.append("IRELAND")
        elif t1=='NZ':
            teamlist1.append("NEW ZEALAND")
        elif t1=='PAK':
            teamlist1.append("PAKISTAN")
        elif t1=='SA' or t1=='RSA':
            teamlist1.append("SOUTH AFRICA")
        elif t1=='SL':
            teamlist1.append("SRI LANKA")
        elif t1=='WI':
            teamlist1.append("WEST INDIES")
        elif t1=='ZIM':
            teamlist1.append("ZIMBABWE")
        elif t1=='KEN':
            teamlist1.append("KENYA")
        elif t1=='SCO':
            teamlist1.append("SCOTLAND")
        elif t1=='UAE':
            teamlist1.append("UNITED ARAB EMIRTES")
    return teamlist1        
        
        

#get_teamlist1 will collect all team1 in a list
def get_teamlist2(soup):
    country_list=["AFGHANISTAN","AUSTRALIA","BANGLADESH","ENGLAND","INDIA","IRELAND","NEW ZEALAND","PAKISTAN","SOUTH AFRICA", "SRI LANKA", "WEST INDIES","ZIMBABWE","KENYA","SCOTLAND","UAE"]
    teamlist2=[]
    match_id=get_match_id(soup)
    for j in match_id:
        t2=Match(j).team_2_abbreviation
        if t2=='AFG':
            teamlist2.append("AFGHANISTAN")
        elif t2=='AUS':
            teamlist2.append("AUSTRALIA")
        elif t2=='BAN':
            teamlist2.append("BANGLADESH")
        elif t2=='ENG':
            teamlist2.append("ENGLAND")
        elif t2=='IND':
            teamlist2.append("INDIA")
        elif t2=='IRE' or t2=='IRL':
            teamlist2.append("IRELAND")
        elif t2=='NZ':
            teamlist2.append("NEW ZEALAND")
        elif t2=='PAK':
            teamlist2.append("PAKISTAN")
        elif t2=='SA' or t2=='RSA':
            teamlist2.append("SOUTH AFRICA")
        elif t2=='SL':
            teamlist2.append("SRI LANKA")
        elif t2=='WI':
            teamlist2.append("WEST INDIES")
        elif t2=='ZIM':
            teamlist2.append("ZIMBABWE")
        elif t2=='KEN':
            teamlist2.append("KENYA")
        elif t2=='SCO':
            teamlist2.append("SCOTLAND")
        elif t2=='UAE':
            teamlist2.append("UNITED ARAB EMIRTES")
    return teamlist2

    

    
#speech_output will give output of the query in form of speech    
def speech_output(mytext):
    
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3") 
    os.system("welcome.mp3") 
    

#voice_input uses google API to process input voice
def voice_input():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    with mic as source:
        #r.adjust_for_ambient_noise(source)
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        audio = r.listen(source)
    print(r.recognize_google(audio))
    return r.recognize_google(audio)
        

#after fetching voice, all the keywords of voice are processed in voice_processing and 
#generate suitable string as output
def voice_processing(vstr):
    soup=data_request()
    wordlist=[]
    vstr=vstr.upper()
    
    wordlist=vstr.split()
    returnstr=""
    match_id=get_match_id(soup)
    get_cache1(wordlist)
    get_cache2(wordlist)
        
    team1=get_team1(wordlist)  
    team2=get_team2(wordlist)  
    
    if "HELLO" in wordlist or "HI" in wordlist or ("GOOD" in wordlist and ("DAY" in wordlist or "MORNING" in wordlist or "EVENING" in wordlist)):
        returnstr= "Hello. This is Meera. What do you want to know?"
    elif ("HOW" in wordlist and "ARE" in wordlist and "YOU" in wordlist) or ("HOW" in wordlist and "DOING" in wordlist):
        returnstr="I am doing good"   
    elif "MATCH" in wordlist or "MATCHES" in wordlist or ("CURRENT" in wordlist or "LIVE" in wordlist or "ONGOING" in wordlist or "ALL" in wordlist ):
        if match_id==[]:
            returnstr="there are no live matches going on right now."
        else:
            print(match_id)
            returnstr="Here is the list of all ongoing matches. "
            for i in match_id:
                print(i)
                print(Match(i).description)
                
                returnstr=returnstr+" "+Match(i).description
                returnstr=returnstr.replace(" v "," versus ")
                returnstr=returnstr+". " 
                
            returnstr=returnstr
    
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) and "SCORE" in wordlist:
        returnstr=get_score(team1, team2)
        
    elif team1=="" and team2=="" and "SCORE" in wordlist:
        returnstr=get_score(cache1,cache2)
    
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) and ("RUNRATE" in wordlist or("RUN" in wordlist and "RATE" in wordlist)):
        returnstr=get_runrate(team1, team2)
        
    elif team1=="" and team2=="" and ("RUNRATE" in wordlist or("RUN" in wordlist and "RATE" in wordlist)):
        returnstr=get_runrate(team1, team2)    
        
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) and "FORMAT" in wordlist:
        returnstr=get_match_format(team1, team2)
        
    elif team1=="" and team2=="" and "FORMAT" in wordlist:
        returnstr=get_match_format(cache1,cache2)
    
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) and ("VENUE" in wordlist or "PLACE" in wordlist):
        returnstr=get_groundname(team1, team2)
        
    elif team1=="" and team2=="" and ("VENUE" in wordlist or "PLACE" in wordlist):
        returnstr=get_groundname(cache1,cache2)
        
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) and ("RESULT" in wordlist or "WON" in wordlist or  "WIN" in wordlist):
        returnstr=get_result(team1, team2)
        
    elif team1=="" and team2=="" and ("RESULT" in wordlist or "WON" in wordlist or "WIN" in wordlist):
        returnstr=get_result(cache1,cache2)    
    
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) and ("STATUS" in wordlist):
        returnstr=get_status(team1, team2)
        
    elif team1=="" and team2=="" and ("STATUS" in wordlist):
        returnstr=get_status(cache1,cache2)
    
    
    elif "YOUR" in wordlist and "NAME" in wordlist:
        returnstr="My name is Meera"
        
    elif "LAZY" in wordlist or "SLOW" in wordlist:
        returnstr="No, Its your internet which is slow"
        
    elif (team1!="" or team2!="" or (team1!="" and team2!="")) :
        if team1!="" and team2=="":
            returnstr="what do you want to know about "+team1
        elif team2!="" and team1=="":
            returnstr="what do you want to know about "+team1
        elif team1!="" and team2!="":
            returnstr="what do you want to know about "+team1+" and "+team2
        returnstr=get_score(team1, team2)
    elif "BYE" in wordlist:
        returnstr="BYE BYE HAVE A NICE DAY"
    elif ("GET" in wordlist and "LOST" in wordlist)  or "LOST" in wordlist:
        returnstr="You too" 
    elif team1=="" and team2=="" and "SCORE" in wordlist :
        returnstr=get_score(cache1,cache2)
    
    else:
        returnstr="I did not understand what you said "
    
    print(returnstr)
    return returnstr


#get_team1 will find out name of team1 from input voice
def get_team1(wordlist):
    team1=""
    country_list=["AFGHANISTAN","AUSTRALIA","BANGLADESH","ENGLAND","INDIA","IRELAND","ZEALAND","PAKISTAN","SOUTH AFRICA", "SRI LANKA", "WEST INDIES","ZIMBABWE","KENYA","SCOTLAND","UAE"]
    if list(set(wordlist) & set(country_list))!=[]:
        team1=list(set(wordlist) & set(country_list))[0]
        team1=team1.replace("ZEALAND", "NEW ZEALAND")
    return team1


#get_team1 will find out name of team1 from input voice
def get_team2(wordlist):
    team2=""
    country_list=["AFGHANISTAN","AUSTRALIA","BANGLADESH","ENGLAND","INDIA","IRELAND","ZEALAND","PAKISTAN","SOUTH AFRICA", "SRI LANKA", "WEST INDIES","ZIMBABWE","KENYA","SCOTLAND","UAE"]
    if list(set(wordlist) & set(country_list))!=[] and  len(list(set(wordlist) & set(country_list)))==2:
        team2=list(set(wordlist) & set(country_list))[1]
        team2=team2.replace("ZEALAND","NEW ZEALAND")
    return team2

# get_score will return live score of match between team1 and team2
def get_score(team1,team2):
    score=""
    print(team1)
    print(team2)
    soup=data_request()
    teamlist1=get_teamlist1(soup)
    teamlist2=get_teamlist2(soup)
    print(teamlist1)
    print(teamlist2)
    match_id=get_match_id(soup)
    if team1!="" and team2!="" and team1 in teamlist1:
        ind=teamlist1.index(team1)
        if teamlist2[ind]==team2:
            match=match_id[ind]
            score=Match(match).current_summary
            score=score[0:score.index("(")]
            if score.find("/")==-1:
                score=score+" all out "
                score=score+" "+Match(match).result
            else:
                score=score.replace("/"," for ")
                score=score+" wickets" 
                score=score+" "+Match(match).result
        else:
            score="there is no match between "+team1+" and "+team2 
          
    elif team1!="" and team2!="" and team1 in teamlist2:  
        ind=teamlist2.index(team1) 
        if teamlist1[ind]==team2:
            match=match_id[ind]
            score=Match(match).current_summary
            score=score[0:score.index("(")]
            if score.find("/")==-1:
                score=score+" all out "
                score=score+" "+Match(match).result
            else:
                score=score.replace("/"," for ")
                score=score+" wickets" 
                score=score+" "+Match(match).result
        else:
            score="there is no match between "+team1+" and "+team2 
        
    elif team1!="" and team2=="":   
        if team1 in teamlist1:
            ind=teamlist1.index(team1) 
            match=match_id[ind]
            score=Match(match).current_summary
            score=score[0:score.index("(")]
            if score.find("/")==-1:
                score=score+" all out "
                score=score+" "+Match(match).result
            else:
                score=score.replace("/"," for ")
                score=score+" wickets" 
                score=score+" "+Match(match).result
        elif team1 in teamlist2:
            ind=teamlist2.index(team1) 
            match=match_id[ind]
            score=Match(match).current_summary
            score=score[0:score.index("(")]
            if score.find("/")==-1:
                score=score+" all out "
                score=score+" "+Match(match).result
            else:
                score=score.replace("/"," for ")
                score=score+" wickets" 
                score=score+" "+Match(match).result
        else:
            score="there is no match going on for "+team1  
        
    elif team1=="" and team2!="":   
        if team2 in teamlist1:
            ind=teamlist1.index(team2) 
            match=match_id[ind]
            score=Match(match).current_summary
            score=score[0:score.index("(")]
            if score.find("/")==-1:
                score=score+" all out "
                score=score+" "+Match(match).result
            else:
                score=score.replace("/"," for ")
                score=score+" wickets" 
                score=score+" "+Match(match).result
        elif team2 in teamlist2:
            ind=teamlist2.index(team2) 
            match=match_id[ind]
            score=Match(match).current_summary
            score=score[0:score.index("(")]
            if score.find("/")==-1:
                score=score+" all out "
                score=score+" "+Match(match).result
            else:
                score=score.replace("/"," for ")
                score=score+" wickets" 
                score=score+" "+Match(match).result
        else:
            score="there is no match going on for "+team2
           
    elif team1=="" and team2=="":
        score="Please tell me the team name, whose score you want to know"
    return score

# get_match_format will return format(T20I, test, ODI) of match between team1 and team2
def get_match_format(team1,team2):
    matchformat=""
    soup=data_request()
    teamlist1=get_teamlist1(soup)
    teamlist2=get_teamlist2(soup)
    match_id=get_match_id(soup)
    if team1!="" and team2!="" and team1 in teamlist1:
        ind=teamlist1.index(team1)
        if teamlist2[ind]==team2:
            match=match_id[ind]
            matchformat="The format of the match is "+Match(match).match_class+" match"
            
    elif team1!="" and team2!="" and team1 in teamlist2:
        ind=teamlist2.index(team1)
        if teamlist1[ind]==team2:
            match=match_id[ind]
            matchformat="The format of the match is "+Match(match).match_class+" match"
    
    elif team1!="" and team2=="":   
        if team1 in teamlist1:
            ind=teamlist1.index(team1) 
            match=match_id[ind]
            matchformat="The format of the match is "+Match(match).match_class+" match"
            
        elif team1 in teamlist2:
            ind=teamlist2.index(team1) 
            match=match_id[ind]
            matchformat="The format of the match is "+Match(match).match_class+" match"
            
        else:
            matchformat="there is no match going on for "+team1
    
    
    elif team1=="" and team2!="":   
        if team2 in teamlist1:
            ind=teamlist1.index(team2) 
            match=match_id[ind]
            matchformat="The format of the match is "+Match(match).match_class+" match"
            
        elif team2 in teamlist2:
            ind=teamlist2.index(team2) 
            match=match_id[ind]
            matchformat="The format of the match is "+Match(match).match_class+" match"
            
        else:
            matchformat="there is no match going on for "+team2
    
    elif team1=="" and team2=="":
        matchformat="Please tell me the team name, whose format you want to know"
    return matchformat
    
def get_cache1(wordlist):
    global cache1
    new=get_team1(wordlist)
    if new!=cache1 and new!="":
        cache1=new
    
def get_cache2(wordlist):
    global cache2
    new=get_team2(wordlist)
    if new!=cache2 and new!="":
        cache2=new    
# get_runrate will return runrate of match between team1 and team2    
def get_runrate(team1,team2):
    runrate=""
    soup=data_request()
    teamlist1=get_teamlist1(soup)
    teamlist2=get_teamlist2(soup)
    match_id=get_match_id(soup)
    if team1!="" and team2!="" and team1 in teamlist1:
        ind=teamlist1.index(team1)
        if teamlist2[ind]==team2:
            match=match_id[ind]
            runrate="The current run rate is "+str(Match(match).team_1_run_rate)
                                                  
    elif team1!="" and team2!="" and team1 in teamlist2:
        ind=teamlist2.index(team1)
        if teamlist1[ind]==team2:
            match=match_id[ind]
            runrate="The current run rate is "+str(Match(match).team_1_run_rate)
    elif team1!="" and team2=="":   
        if team1 in teamlist1:
            ind=teamlist1.index(team1) 
            match=match_id[ind]
            runrate="The current run rate is "+str(Match(match).team_1_run_rate)
            
        elif team1 in teamlist2:
            ind=teamlist2.index(team1) 
            match=match_id[ind]
            runrate="The current run rate is "+str(Match(match).team_1_run_rate)
            
        else:
            runrate="there is no match going on for "+team1
    elif team1=="" and team2!="":   
        if team2 in teamlist1:
            ind=teamlist1.index(team2) 
            match=match_id[ind]
            runrate="The current run rate is "+str(Match(match).team_1_run_rate)
            
        elif team2 in teamlist2:
            ind=teamlist2.index(team2) 
            match=match_id[ind]
            runrate="The current run rate is "+str(Match(match).team_1_run_rate)
            
        else:
            runrate="there is no match going on for "+team2
    
    elif team1=="" and team2=="":
        runrate="Please tell me the team name, whose run rate you want to know" 
        
    return runrate

# get_groundname will return groundname of match between team1 and team2
def get_groundname(team1, team2):
    ground=""
    soup=data_request()
    teamlist1=get_teamlist1(soup)
    teamlist2=get_teamlist2(soup)
    match_id=get_match_id(soup)
    if team1!="" and team2!="" and team1 in teamlist1:
        ind=teamlist1.index(team1)
        if teamlist2[ind]==team2:
            match=match_id[ind]
            ground="The match is being played at "+Match(match).ground_name
                                                  
    elif team1!="" and team2!="" and team1 in teamlist2:
        ind=teamlist2.index(team1)
        if teamlist1[ind]==team2:
            match=match_id[ind]
            ground="The match is being played at "+Match(match).ground_name
    elif team1!="" and team2=="":   
        if team1 in teamlist1:
            ind=teamlist1.index(team1) 
            match=match_id[ind]
            ground="The match is being played at "+Match(match).ground_name
            
        elif team1 in teamlist2:
            ind=teamlist2.index(team1) 
            match=match_id[ind]
            ground="The match is being played at "+Match(match).ground_name
            
        else:
            ground="there is no match going on for "+team1
    elif team1=="" and team2!="":   
        if team2 in teamlist1:
            ind=teamlist1.index(team2) 
            match=match_id[ind]
            ground="The match is being played at "+Match(match).ground_name
            
        elif team2 in teamlist2:
            ind=teamlist2.index(team2) 
            match=match_id[ind]
            ground="The match is being played at "+Match(match).ground_name
            
        else:
            ground="there is no match going on for "+team1
    
    elif team1=="" and team2=="":
        ground="Please tell me the team name, whose venue you want to know" 
        
    return ground
# get_status will return current status of match between team1 and team2
def get_status(team1,team2):  
    
    status=""
    soup=data_request()
    teamlist1=get_teamlist1(soup)
    teamlist2=get_teamlist2(soup)
    match_id=get_match_id(soup)
    if team1!="" and team2!="" and team1 in teamlist1:
        ind=teamlist1.index(team1)
        if teamlist2[ind]==team2:
            match=match_id[ind]
            status="The status of the match is "+Match(match).status                                                  
    elif team1!="" and team2!="" and team1 in teamlist2:
        ind=teamlist2.index(team1)
        if teamlist1[ind]==team2:
            match=match_id[ind]
            status="The status of the match is "+Match(match).status
    elif team1!="" and team2=="":   
        if team1 in teamlist1:
            ind=teamlist1.index(team1) 
            match=match_id[ind]
            status="The status of the match is "+Match(match).status
            
        elif team1 in teamlist2:
            ind=teamlist2.index(team1) 
            match=match_id[ind]
            status="The status of the match is "+Match(match).status
            
        else:
            status="there is no match going on for "+team1
    elif team1=="" and team2!="":   
        if team2 in teamlist1:
            ind=teamlist1.index(team2) 
            match=match_id[ind]
            status="The status of the match is "+Match(match).status
            
        elif team2 in teamlist2:
            ind=teamlist2.index(team2) 
            match=match_id[ind]
            status="The status of the match is "+Match(match).status
            
        else:
            status="The status of the match is "+Match(match).status
    
    elif team1=="" and team2=="":
        status="Please tell me the team name, whose status you want to know" 
        
    return status
 
# get_result will return result of match between team1 and team2
def get_result(team1, team2):
    result=""
    soup=data_request()
    teamlist1=get_teamlist1(soup)
    teamlist2=get_teamlist2(soup)
    match_id=get_match_id(soup)
    if team1!="" and team2!="" and team1 in teamlist1:
        ind=teamlist1.index(team1)
        if teamlist2[ind]==team2:
            match=match_id[ind]
            result=Match(match).result                                                  
    elif team1!="" and team2!="" and team1 in teamlist2:
        ind=teamlist2.index(team1)
        if teamlist1[ind]==team2:
            match=match_id[ind]
            result=Match(match).result
    elif team1!="" and team2=="":   
        if team1 in teamlist1:
            ind=teamlist1.index(team1) 
            match=match_id[ind]
            result=Match(match).result
            
        elif team1 in teamlist2:
            ind=teamlist2.index(team1) 
            match=match_id[ind]
            result=Match(match).result
            
        else:
            result="there is no match going on for "+team1
    elif team1=="" and team2!="":   
        if team2 in teamlist1:
            ind=teamlist1.index(team2) 
            match=match_id[ind]
            result=Match(match).result
            
        elif team2 in teamlist2:
            ind=teamlist2.index(team2) 
            match=match_id[ind]
            result=Match(match).result
            
        else:
            result=Match(match).result
    
    elif team1=="" and team2=="":
        result="Please tell me the team name, whose result you want to know" 
        
    return result

    
           
def main():
    i=["your name","how are you","pakistan score","pakistan format"]
    
    soup=data_request()
    #print(get_team1(soup))
    #print(get_team2(soup))
    #print(match_id)
    print(get_match_id(soup))
    
    while(1): 
        try:   
            str1=voice_input()
            #print(str)
                
            returnstr=voice_processing(str1)
            speech_output(returnstr)
            #time.sleep(5)
        except:
            pass
    
        
   
   
main()
