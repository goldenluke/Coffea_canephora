def kaplan_yorke_dimension(lyap):

    lyap = sorted(lyap, reverse=True)

    total = 0
    j = 0

    for i, val in enumerate(lyap):
        if total + val > 0:
            total += val
            j = i
        else:
            break

    if j+1 < len(lyap) and lyap[j+1] != 0:
        return j + total / abs(lyap[j+1])

    return j
