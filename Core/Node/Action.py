def actions(state):
    n=len(state)
    result=[]
    for src in range(n):
        for dst in range(n):
            if can_pour(state,src,dst):
                result.append((src,dst))
    return result