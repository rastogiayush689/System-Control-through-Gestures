num = input('number: ').split()

dic = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14,
       'fifteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18, 'nineteen':19, 'twenty':20, 'thirty':30, 'fourty':40, 'fifty':50, 'sixty':60, 'seventy':70,
       'eighty':80, 'ninety':90, 'hundred':100, 'hundreds':100, 'thousand':1000, 'thousands':1000, 'lakh':100000, 'lakhs':100000, 'crore':10000000, 'crores':10000000,
       'arab':1000000000, 'arabs':1000000000}

factor = ['arab', 'crore', 'lakh', 'thousand', 'hundred']

valid_two = {'twenty':20, 'thirty':30, 'fourty':40, 'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90}


def word_to_number(num):
    global dic, factor, valid_two
    
    flag = True
    for i in num:
        if i not in dic.keys():
            flag = False
            
    if flag:
        c = 0
        for fac in factor:
            #print(num, fac)
            if fac in num:
                ind = num.index(fac)
            elif fac+'s' in num:
                ind = num.index(fac+'s')
            else:
                continue
            
            if ind>2:
                return (-1)
            
            else:
                #print('else')
                t = 0
                flag = False
                for i in range(ind):
                    t+=dic[num[i]]
        
                c+=t*dic[num[ind]]
                num = num[ind+1:]

        if len(num)==0:
            pass
        elif len(num)>2:
            return (-1)
        elif len(num)==2:
            if num[0] in valid_two.keys():
                c+=dic[num[0]]+dic[num[1]]
                
            else:
                return (-1)
        else:
            c+=dic[num[0]]
        return c
    else:
        return (-1)

print(word_to_number(num))
