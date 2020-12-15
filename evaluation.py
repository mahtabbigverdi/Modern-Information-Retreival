
def get_fscore(true, pred, alpha = 0.5):
    total = len(true)
    tn, fp, fn, tp = 0, 0,0,0
    for i in range(total):
        if true[i] == pred[i]:
            if true[i] == 1:
                tp +=1
            else:
                tn += 1
        else:
            if true[i] == 1:
                fn +=1
            else:
                fp += 1

    pr = tp / (tp + fp)
    rec = tp /(tp + fn)
    F = 1/ ( alpha*(1/pr) + (1 - alpha) * (1/rec))
    return F


def get_pr_rec (true,pred):
    total = len(true)
    tn, fp, fn, tp = 0, 0, 0, 0
    for i in range(total):
        if true[i] == pred[i]:
            if true[i] == 1:
                tp += 1
            else:
                tn += 1
        else:
            if true[i] == 1:
                fn += 1
            else:
                fp += 1

    pr = tp / (tp + fp)
    rec = tp / (tp + fn)
    result={}
    result[1]={'precision':pr, 'recall':rec}
    pr = tn / (tn + fn)
    rec = tn / (tn + fp)
    result[-1] = {'precision': pr, 'recall': rec}
    return result

def get_accuracy(true, pred):
    total = len(true)
    correct = 0
    for i in range(total):
        if true[i] == pred[i]:
            correct+=1
    return correct/total
