#python3 kadai5.py 〇〇.txt n m
#〇〇.txtのm行からn行以外(n行,m行を含む)の行数を表示する。(n<mの場合はその間)
import sys
args=sys.argv
file=args[1]
with open(file,"r") as f:
    lines=[]
    i=0
    for line in f:
        line=line.rstrip()
        lines.append(line)
        i+=1


if int(args[2]) > i or int(args[3]) < 1: #エラー処理(text内の行数を指していないとき)
    print('python3 kadai5.py 〇〇.txt n m')
    print('1<=m','and n<=%d' %i)
elif int(args[2]) < int(args[3]): #n<mのとき
    lowest = int(args[2]) - 1
    highest = int(args[3])
    for appear_num in range(lowest, highest):
        line_num = appear_num + 1
        print("\n%d行目:" % line_num)
        print(lines[appear_num])

else: #n>mのとき
    blank_lowest=int(args[3])
    blank_highest=int(args[2])-1
    txt_highest=i-1
    for appear_num in range(0,blank_lowest):
        line_num=appear_num+1
        print('\n%d行目' %line_num)
        print(lines[appear_num])

    for appear_num in range(blank_highest,txt_highest):
        line_num=appear_num+1
        print('\n%d行目:' %line_num)
        print(lines[appear_num])

