import re

# def validate(Time):
#     Found_val = re.search("^[a-zA-Z0-9]+:\d\d:\d\d-\d\d:\d\d$", Time)
#     if Found_val is None:
#         return False
#     get_Vals = Found_val.string.split(":", 1)
#     times = get_Vals[1].split("-")
#     for time in times:
#         val = time.split(":")
#         if (int(val[0]) > 24) or (int(val[0]) == 24 and int(val[1]) > 0) or (int(val[1]) > 60):
#             return False
#     return True


def calculateTime(times):
    Avail_time_by_per = {}
    for t in times:
        state = t.split(":", 1)
        if state[0] not in Avail_time_by_per:
            Avail_time_by_per[state[0]] = []
        Avail_time_by_per[state[0]].append(state[1])

    Available_Times = ["00:00-24:00"]
    for per in Avail_time_by_per:
        Time = Avail_time_by_per[per]
        new_times = []
        for time_slot in Time:
            ts = time_slot.split("-")
            for avail_time in Available_Times:
                at = avail_time.split("-")
                if (ts[1] < at[0] or ts[0] > at[1]):
                    break
                else:
                    new_times.append(max(ts[0], at[0]) + "-" + min(ts[1], at[1]))
        Available_Times = new_times
        
    return Available_Times

def getAvailDic(e_time, times):
    """
        Given the time of an event and the available times, returns a dictionary of time slot to whoever's available.
        e_time should be in the format of "00:00-24:00" similarish time-zone.

        Note: Currently the e_time is expected to be starting at any hour but either 00 minute, 15 minute, 30 minute
        or 45 minute.
    """

    timezones = e_time.split("-")
    starter = timezones[0].split(":")
    ender = timezones[1].split(":")
    starttime = []
    starttime.append(int(starter[0]))
    starttime.append(int(starter[1]))

    endtime = []
    endtime.append(int(ender[0]))
    endtime.append(int(ender[1]))
    active_dict = {}

    sh = starttime[0]
    sm = starttime[1]
    while sh != endtime[0] or sm != endtime[1]:

        st_h = str(sh)
        st_h2 = str(sh)
        if sm == 45:
            st_h2 = str(sh+1)
        if len(st_h) == 1:
            st_h = '0' + st_h
        if len(st_h2) == 1:
            st_h2 = '0' + st_h2

        if sm == 0:
            st_m = '00'
            st_m2 = '15'
        else:
            st_m = str(sm)
            st_m2 = str((sm + 15) % 60)
            if st_m == "0":
                st_m = "00"
            if st_m2 == "0":
                st_m2 = "00"
        period = st_h+":"+st_m+"-"+st_h2+":"+st_m2
        active_dict[period] = []

        for time in times:
            act = time.split(":", 1)
            time_it = act[1].split("-")
            if time_it[0] < st_h+":"+st_m and time_it[1] > st_h2+":"+st_m2 and act[0] not in active_dict[period]:
                active_dict[period].append(act[0])

        sm = (sm + 15) % 60
        if sm == 0:
            sh = sh + 1
    return active_dict


