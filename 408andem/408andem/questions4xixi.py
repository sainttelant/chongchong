
import time
import random
import msvcrt 
dadui=0 

guli = ["溪溪牛啊，可以啊","这小孩可以的~~~","答对了,对你来说很简单啊","值得鼓励","哟，不错","厉害溪溪，马上答完了"]
piping =["溪溪看仔细点","别粗心大意啊","着啥急呢","你再想想","慌啥呢~~","小蜡扎看清题目再输入"]
 
ops=['+','-']
random.shuffle(ops)
ops1=ops[0]
numbers=1
numbers1=0
stop = False

numberoftimu = int(input("家长环节，选择给溪溪出多少题："))

ready = input("溪溪准备好%d题的答题环节了吗？准备好了按1，没准备好按2，最多再给你1分钟的玩耍时间！！"%(numberoftimu))

if ready == "1":
    print("好了，开始答题！")
    while stop is not True:
        add1=random.randint(1,20)
        add2=random.randint(1,20)
        ops1=ops[0]
        print('第',numbers,'题')
        if add1-add2<0:
            eq =str(add2)+ops[0]+str(add1)
            time.sleep(1)
            print(add2,ops1,add1,'=')
        else:
            eq=str(add1)+ops[0]+str(add2)
            time.sleep(1)
            print(add1,ops1,add2,'=')
        val=eval(eq)
    
        try:
            ask=int(input('答案是几：'))
        except:
            print("请输入数字，不要按其他按键！")
            continue

        if ask==val:
            huashu = guli[random.randint(0,5)]
            print(huashu)
            print()
            numbers+=1
            dadui+=1
            random.shuffle(ops)
        else:
            print('答错了，正确答案是',val)
            huashu = piping[random.randint(0,5)]
            print(huashu)
            numbers+=1
            random.shuffle(ops)
        if numbers == numberoftimu+1:
            stop = True
else:
    jishu:int = 0
    count = input("你还想玩多少秒钟，最多只能输入60秒哦~~~~：")
    if int(count) > 60:
        count = 60
    jishu = int(count)
    for i in range(0,int(count)):
        
        print("倒计时开始，你还有%s秒钟开始"%(jishu))
        jishu-=1
        time.sleep(1)
    print("好了，1分钟结束，开始答题~~~~~加油！")
    while stop is not True:
        add1=random.randint(1,20)
        add2=random.randint(1,20)
        ops1=ops[0]
        print('第',numbers,'题')
        if add1-add2<0:
            eq =str(add2)+ops[0]+str(add1)
            time.sleep(1)
            print(add2,ops1,add1,'=')
        else:
            eq=str(add1)+ops[0]+str(add2)
            time.sleep(1)
            print(add1,ops1,add2,'=')
        val=eval(eq)
    
        try:
            ask=int(input('答案是几：'))
        except:
            print("请输入数字，不要乱按其他按键！")
            continue

        if ask==val:
            print('恭喜你，答对了')
            print()
            numbers+=1
            dadui+=1
            random.shuffle(ops)
        else:
            print('答错了，正确答案是',val)
            print()
            numbers+=1
            random.shuffle(ops)
        if numbers == numberoftimu+1:
            stop = True
print("溪溪，你已经完成%d题练习！"%(numberoftimu))
bilu = (dadui/numberoftimu)*100
print("溪溪，%d题，你共答对了%d题，正确率为百分之%.2f"%(numberoftimu,dadui,bilu))

if(bilu > 95):
    print("溪溪正确率为百分之%.2f，相当于考试在95分以上，奖励一朵小花~~~！"%(bilu))
else:
    print("这么简单的题目都能做错这么多，扣除小花一朵~~~~~！")

print("Press 'D' to exit...")
 
while True:
 if ord(msvcrt.getch()) in [68, 100]:
  break