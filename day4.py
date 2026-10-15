uptime=97.5
bill=50000
if uptime>=99.9:
    refund=0
elif uptime>=98:
    refund=bill*0.10
else:
    refund=bill*0.25
print("refund amount : ",refund)