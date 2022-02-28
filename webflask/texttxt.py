data = "ผลิตภัณฑ์สบู่แข็ง ดีโด พลัส"
ans = ""
aeiou= "ิ,ื,่,้,ั,ี,ึ,ุ,ู,์,็"
for i in range(0,len(data)):
    if data[i] in aeiou:
        ans += data[i]+" "
    else:
        ans += data[i]

print(ans)