# 1 AgileFuzz 使用介绍
    AgileFuzz是基于AFL的模糊测试工具，能够针对程序的关键位置进行细粒度变异。使用AgileFuzz测试程序，你需要以下步骤:

## 1.1 编译AgileFuzz
    apt-get install llvm clang
    cd fuzz
    make -j4
    cd llvm_mode
    make -j4

    ** 得到可执行程序 **
        afl-fuzz
        afl-clang-fast
        afl-clang-fast++

## 1.2 编译程序
### 方式1
    ./configure CC=path/afl-clang-fast CXX=path/afl-clang-fast++ --disable-shared
### 方式2
    export CC=path/afl-clang-fast CXX=path/afl-clang-fast++

# 2 文件夹介绍
- lava_analyse：
    lava_analyse.py：该文件可以分析lava测试集的结果
    reslut_24h.txt: 该文件主要

