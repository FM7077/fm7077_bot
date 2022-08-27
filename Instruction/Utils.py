class Utils():
    def MinusTime(self, featureTime, passTime): # datetime.time - datetime-time
        featureTime = str(featureTime)
        passTime = str(passTime)
        hour1 = int(featureTime.split(":")[0])
        hour2 = int(passTime.split(":")[0])
        min1 = int(featureTime.split(":")[1])
        min2 = int(passTime.split(":")[1])
        sec1 = int(featureTime.split(":")[2])
        sec2 = int(passTime.split(":")[2])

        if(hour1 < hour2):
            hour1 += 24
        diffHour = hour1 - hour2
        if(min1 < min2):
            diffHour -= 1
            min1 += 60
        diffMin = diffHour * 60 + min1 - min2
        # if(sec1 < sec2):
        #     diffMin -= 1
        #     sec1 += 60
        # diffSec = diffMin * 60 + sec1 - sec2
        return diffMin