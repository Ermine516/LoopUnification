

ret = "FUNCTION: h 2"+"\n" +"VARIABLE: x"+"\n"+"VARIABLE: y"+"\n"+"LOOP: ll"+"\n"
for i1 in range(1,5):
    for i2 in range(1,5):
        for i3 in range(1,5):
            for i4 in range(1,5):
                for i5 in range(1,5):
                    for i6 in range(1,5):
                        if i1 == 4 and i2 ==4 and i3 ==4 and i4 ==4 and i5 ==4 and i6 ==4:
                            ret = ret + "h(h(x({}),h(x({}),x({}))),ll) h(y({}),h(y({}),y({})))".format(i1,i2,i3,i4,i5,i6)
                        else: ret = ret + "h(h(x({}),h(x({}),x({}))),ll) h(y({}),h(y({}),y({})))\n".format(i1,i2,i3,i4,i5,i6)
f = open("Examples/large.txt", "w")
f.write(ret)
f.close()
