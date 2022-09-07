# -*- coding: UTF-8 -*-
from idaapi import *
from idautils import *
from idc import *
import os 

block_instrument_map={}

class branch_msg:
    def __init__(self,branch,block_addr_from,block_addr_to):
        self.block_addr_from=block_addr_from 
        self.block_addr_to=block_addr_to
        self.branch=branch 
        self.next=None
        self.son_branch1=65537
        self.son_branch2=65537
        self.count=1

    def set_son_branch(self,son_branch,id):
        if id ==1:
            self.son_branch1=son_branch
        else:
            self.son_branch2=son_branch

    def add_next_branch(self,branch_msg):
        next_branch=self
        while not next_branch.next is None: 
            next_branch=next_branch.next
        self.count+=1
        next_branch.next=branch_msg
    
    def get_branch_msg(self):
        count_n=1
        branch_msg_n=self
        branch_str_msg=""
        while branch_msg_n: 
            branch_str_msg+=str(branch_msg_n.branch)+"\t"+str(branch_msg_n.son_branch1)+"\t"+str(branch_msg_n.son_branch2)+"\t"+str(count_n)+"\t"+str(hex(branch_msg_n.block_addr_from))+"\t"+str(hex(branch_msg_n.block_addr_to))+"\n"
            count_n+=1
            branch_msg_n=branch_msg_n.next
        return branch_str_msg

class block_msg:
    def __init__(self,block_addr,block_id):
        self.block_id=block_id
        self.block_addr=block_addr
        self.son_addr1=0
        self.son_addr2=0
        self.branch1=65537
        self.branch2=65537

    def set_son(self,son_addr,id):
        if id==1:
            self.son_addr1=son_addr
        else:
            self.son_addr2=son_addr

    def update_branch(self): 
        global block_instrument_map 
        if self.son_addr1 in block_instrument_map: 
            if self.block_id!=65538 and block_instrument_map[self.son_addr1].block_id!=65538:
                self.branch1=(self.block_id>>1)^block_instrument_map[self.son_addr1].block_id
            else:
                self.branch1=65538
        if self.son_addr2 in block_instrument_map:
            if self.block_id!=65538 and block_instrument_map[self.son_addr2].block_id!=65538:
                self.branch2=(self.block_id>>1)^block_instrument_map[self.son_addr2].block_id
            else:
                self.branch2=65538


def analyse_block(block): 

    front_instr=None 
    for head in Heads(block.start_ea, block.end_ea):  
        instr=print_insn_mnem(head)
        if "call" in instr: 
            if "afl_maybe_log" in print_operand(head,0):
                if front_instr is None:
                    return
                block_id=get_operand_value(front_instr,1)  
                global block_instrument_map
                block_n=block_msg(block.start_ea,block_id)
                
                succs_num=1
                for succ_block in block.succs():
                    block_n.set_son(succ_block.start_ea,succs_num)
                    succs_num+=1

                block_instrument_map[block.start_ea]=block_n 
                return
        front_instr=head 
    block_n=block_msg(block.start_ea,65538)
    block_instrument_map[block.start_ea]=block_n

    return


if __name__ == "__main__": 

    func_addrs=Functions()
    for fun_addr in func_addrs:
        fun=get_func(fun_addr) 
        blocks=FlowChart(fun)  
        for block in blocks:
            analyse_block(block)

    binname=GetInputFile()
    bin_path=os.getcwd()
    result_path=bin_path[:len(bin_path)-8]
    file=open(result_path+"result\\".decode('utf-8')+binname+".txt","w")
    file.write("id\tson1_id\tson2_id\tson_num\taddr_from\taddr_to\n")

    for block_msg in block_instrument_map.values():
        block_msg.update_branch() 

    branch_map={}
    for block_msg in block_instrument_map.values():

        if block_msg.branch1!=65537: 
            branch_msg_n=branch_msg(block_msg.branch1,block_msg.block_addr,block_msg.son_addr1) 
            if block_msg.son_addr1 in block_instrument_map:
                son_block_msg1=block_instrument_map[block_msg.son_addr1]
                branch_msg_n.set_son_branch(son_block_msg1.branch1,1)
                branch_msg_n.set_son_branch(son_block_msg1.branch2,2) 

            if block_msg.branch1 in branch_map:
                branch_map[block_msg.branch1].add_next_branch(branch_msg_n)
            else:
                branch_map[block_msg.branch1]=branch_msg_n

        if block_msg.branch2!=65537:
            branch_msg_n=branch_msg(block_msg.branch2,block_msg.block_addr,block_msg.son_addr2)  
            if block_msg.son_addr2 in block_instrument_map:
                son_block_msg2=block_instrument_map[block_msg.son_addr2]
                branch_msg_n.set_son_branch(son_block_msg2.branch1,1)
                branch_msg_n.set_son_branch(son_block_msg2.branch2,2)

            if block_msg.branch2 in branch_map:
                branch_map[block_msg.branch2].add_next_branch(branch_msg_n)
            else:
                branch_map[block_msg.branch2]=branch_msg_n  

    count_diff=0
    count_same=0
    count_same2=0
    for branch_msg in branch_map.values(): 
        if branch_msg.branch==65538:
            continue
        elif branch_msg.son_branch1==65537 and branch_msg.son_branch2==65537:
            count_same2+=1
        elif branch_msg.son_branch1==65537 or branch_msg.son_branch2==65537:
            count_same+=1
        count_diff+=1 
        file.write(branch_msg.get_branch_msg())  

    file.close()

    idc.Exit(0)
