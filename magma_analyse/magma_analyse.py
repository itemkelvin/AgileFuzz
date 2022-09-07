import os
import sys
import json

def convert_time(time):
    if time<60:
        return str(time)+"s"
    elif time<3600:
        return str(int(time/60.0))+"m"
    else:
        return str(int(time/3600.0))+"h"

def main():
    if len(sys.argv)<3:
        print("[-] usage: python3 managa_analyse.py bug_result.json result.txt")
        exit(0) 

    result_file=open(sys.argv[2],"w")

    result=None

    result_path=sys.argv[1]
    with open(result_path) as f:
        result = json.load(f) 

    for fuzz_name in result["results"]: 
        result_file.write(fuzz_name+":")
        sum=0
        triggered_list={}
        reached_list={}
        for software in result["results"][fuzz_name]:  
            for software_sigle in result["results"][fuzz_name][software]:
                for item in result["results"][fuzz_name][software][software_sigle]:
                    triggereds=result["results"][fuzz_name][software][software_sigle][item]["triggered"]
                    for triggered in triggereds:
                        if triggered in triggered_list:
                            if triggered_list[triggered]>triggereds[triggered]:
                                triggered_list[triggered]=triggereds[triggered]
                        else:
                            triggered_list[triggered]=triggereds[triggered]
                    reacheds=result["results"][fuzz_name][software][software_sigle][item]["reached"]
                    for reached in reacheds:
                        if reached in reached_list:
                            if reached_list[reached]>reacheds[reached]:
                                reached_list[reached]=reacheds[reached]
                        else:
                            reached_list[reached]=reacheds[reached] 
        result_file.write(str(len(triggered_list))+"\t"+str(len(reached_list))+"\n")
         
    result_file.close()

if __name__=="__main__":
    main()