def swap_first_last(num):
    temp=num
    count=0

    while temp>0:
        temp//=10
        count+=1

    last=num%10
    first=num//(10**(count-1))

    middle=(num%(10**(count-1)))//10
    # middle=middle//10

    result= last*(10**(count-1))+(middle*10)+first
    return result
