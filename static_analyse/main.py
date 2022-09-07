import os
import time 
  
# 存在一些基本块没有成功插桩，影响结果 

def main():  
    script_path=os.getcwd()+"\\branch_extract_llvm.py"
    ida_file_path=os.getcwd()+"\\software\\"

    software_list=os.listdir(ida_file_path)
    for software in software_list:
        if ".i64" in software:
            continue
        start_time=time.time()
        print("[*] 正在对"+software+"进行静态分析!")
        command="ida64.exe -A -S\\\""+script_path+"\\\" "+ida_file_path+software
        os.system(command)
        # os.remove(ida_file_path+software+".i64") 
        end_time=time.time()
        print("[+] 静态分析完成,耗时"+str(round(end_time-start_time, 2))+"秒!")

main()