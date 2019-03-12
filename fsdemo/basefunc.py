from datetime import datetime


def GetDurationString(duration=0):
    dlist = [
        [365 * 24 * 60 * 60, ' year'],
        [30 * 24 * 60 * 60, ' month'],
        [7 * 24 * 60 * 60, ' week'],
        [24 * 60 * 60, ' day'],
        [60 * 60, ' hour'],
        [60, ' minute'],
        [1, ' second'],
    ]
    duration_str = ''
    for ditem in dlist:
        dvalue = int(duration / ditem[0])
        if dvalue > 0:
            duration_str = str(dvalue) + ditem[1]
            if dvalue > 1:
                duration_str += 's'
            break
    return duration_str


def ConvertTimesDiff(base_time=datetime.now(), dest_time=datetime.now()):
    # print(base_time, dest_time)  # print for test
    timed = dest_time - base_time
    if base_time < dest_time:
        durationsuffix = ' later'
    elif base_time > dest_time:
        durationsuffix = ' ago'
    else:
        return 'Just now'
    try:
        duration = abs(timed.total_seconds())
        duration_str = GetDurationString(duration)
    except OverflowError:
        pass
    return duration_str + durationsuffix


def StringToArrayWithoutSpace(str):
    retarr = []
    if str != '':
        arr = str.split(' ')
        for a in arr:
            if a != '':
                retarr.append(a)
    return retarr


def HighlightSearchTerms(content, terms):
    up_content = content.upper()
    for term in terms:
        up_term = term.upper()
        pos = up_content.find(up_term)
        if pos >= 0:
            repl_term = content[pos:pos + len(term)]
            content = content.replace(
                repl_term,
                '<span class="custom-search-highlight">'+repl_term+'</span>',
                1
            )
            break
    return content
