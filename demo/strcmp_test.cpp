
#include <iostream>
#include "string.h"
#include <stdio.h>
using namespace std;  
//该demo对应AgileFuzz进行约束拆分，并能进行快速的路径探索

int main(int argc, char **argv)
{  

    int i=0;
    int c;
    freopen(argv[1], "r", stdin); 
    char str[1000];
    while ((c = cin.get()) != EOF){
        if(i==1000){
            break;
        } 
        str[i]=c;
        i+=1;
    } 
    if(i<200){
        cout<<"文件的长度必须大于200!"<<endl;
        return 0;
    }

    char str1[11];
    char str2[11];
    char str3[11]; 
   

    for(int i=0;i<10;i++){
        str1[i]=str[i];
        str2[i]=str[i+14];
        str3[i]=str[i+35];
    } 
    str1[10]='\0';  
    str2[10]='\0';  
    str3[10]='\0';  

    char *key1="abcdefghij";
    char *key2="1234567890";
    char *key3="ABCDEFGHIJ";

    int num=5;

    if(strcmp(key1,str1)==0){ 

        num=num-2;
        cout<<"找到了关键的字符串-1!"<<endl;
        
        if(strcmp(key2,str2)==0){ 

            num=num-2;

            cout<<"找到了关键的字符串-2!"<<endl;

            if(strcmp(key3,str3)==0){ 

                num=num-1; 
                cout<<"找到了关键的字符串-3!"<<endl; 
                throw "Division by zero condition!";
            } 
        
        }  
        
    } 
 

   return 0;
}
