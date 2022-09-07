import os
import sys
import json

def triggered_analyse(msg_path="temp.txt"):
    f=open(msg_path,"r")
    line=f.readline()
    while line:
        if "Successfully triggered bug" in line: 
            bug_id=int(line.split("Successfully triggered bug ")[1].split(",")[0]) 
            f.close() 
            return bug_id
        line=f.readline()
    f.close()
    return -1

def get_validated_bugs(path):

    bug_ids=[]
    f=open(path,"r")
    line=f.readline()
    while line:
        line=line.replace("\n","")
        bug_ids.append(int(line))
        line=f.readline()
    return bug_ids


def main():

    if len(sys.argv)<3:
        print("[-] usage: python3 lava_analyse.py setting_path result.txt")
        exit(0)

    analyse_results={}

    validated_bugs={}

    setting_file_path=sys.argv[1]
    with open(setting_file_path) as f:
        setting = json.load(f)

    result_file=open(sys.argv[2],"w")

    for software in setting:
        analyse_results[software]={} 
        command=setting[software]["command"]
        fuzz_configs=setting[software]["results"]
        validated_bugs[software]=get_validated_bugs(setting[software]["validated_bugs_path"])
        for fuzz_config in fuzz_configs:
            fuzz_name=fuzz_config["fuzz_name"]
            analyse_results[software][fuzz_name]={}
            analyse_results[software][fuzz_name]["validated_bug_id"]=[]
            analyse_results[software][fuzz_name]["none_validated_bug_id"]=[]
            analyse_results[software][fuzz_name]["none_id"]=0
            crashes_path=os.listdir(fuzz_config["crashes_path"]) 
            for crash_path in crashes_path:
                if "README" in crash_path:
                    continue 
                os.system('''timeout 3s bash -c "'''+command+''' '''+fuzz_config["crashes_path"]+crash_path+''' > temp.txt"''')
                bug_id=triggered_analyse() 
                if bug_id!=-1:
                    if bug_id in validated_bugs[software]:
                        if bug_id not in analyse_results[software][fuzz_name]["validated_bug_id"]:
                            analyse_results[software][fuzz_name]["validated_bug_id"].append(bug_id)
                    else:
                        if bug_id not in analyse_results[software][fuzz_name]["none_validated_bug_id"]:
                            analyse_results[software][fuzz_name]["none_validated_bug_id"].append(bug_id)
                else:
                    analyse_results[software][fuzz_name]["none_id"]+=1

    result_file.write("============== lava bug statistics! =========================\n")

    fuzz_total_result_ids={}
    fuzz_total_result_noneids={}
    for software in analyse_results: 
        result_file.write(software+"(validated_bug,none_validated_bug_id):\n")
        fuzz_result=analyse_results[software]
        for fuzz_name in fuzz_result: 
            
            result_file.write("\t"+fuzz_name+"\t"+str(len(fuzz_result[fuzz_name]["validated_bug_id"]))+"\t"+str(len(fuzz_result[fuzz_name]["none_validated_bug_id"]))+"\n")
            if fuzz_name in fuzz_total_result_ids:
                fuzz_total_result_ids[fuzz_name]+=len(fuzz_result[fuzz_name]["validated_bug_id"])
                fuzz_total_result_noneids[fuzz_name]+=len(fuzz_result[fuzz_name]["none_validated_bug_id"])

            else:
                fuzz_total_result_ids[fuzz_name]=len(fuzz_result[fuzz_name]["validated_bug_id"])
                fuzz_total_result_noneids[fuzz_name]=len(fuzz_result[fuzz_name]["none_validated_bug_id"])

    result_file.write("\n\ntotal crash num:\n") 

    for fuzz_name in fuzz_total_result_ids:
        result_file.write("\t"+fuzz_name+":"+str(fuzz_total_result_ids[fuzz_name])+","+str(fuzz_total_result_noneids[fuzz_name])+"\n") 

    result_file.close()

if __name__=="__main__":
    main()