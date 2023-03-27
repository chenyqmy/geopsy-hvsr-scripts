# Select the longest 3 components traces for loaded stream, so hvsrpy can process such data.
# TargetStream's trace number is 3.
# check if traces length are the same. If not, trim traces to match the shortes one.

from obspy import Stream

def TraceSelect(st):
    if st.count() > 3:
        print('more than 3 traces')
        length = []
        for i in range(int(st.count()/3)):
            length.append(len(st.traces[i]))
        #print(length)
        max_value = max(length)
        max_index = length.index(max_value)
        #print(max_index)

        TargetStream = Stream()
        index = [max_index, int(max_index + st.count()/3), int(max_index + 2*st.count()/3)] #select target traces which are longest traces
        for i in index:
            TargetStream.append(st[i])
        st = TargetStream
    
    if not len(st[0]) == len(st[1]) == len(st[2]):
        length = []
        for i in range(3):
            length.append(len(st.traces[i]))
            #print(length)
            min_value = min(length)
            min_index = length.index(min_value)
            st.trim(st[min_index].stats.starttime, st[min_index].stats.endtime)
    
    return st