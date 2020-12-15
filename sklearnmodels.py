from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
result = {}
C = [0.5, 1, 1.5, 2]
for c in C :
    clf =SVC(C= c)
    clf.fit(train_X, train_y)
    pred = clf.predict(val_X)
    result[c] = accuracy_score(val_y,pred)

max_res = 0
best_c = None
for key,val in result.items():
    if val >= max_res :
        max_res = val
        best_c = key



clf =SVC(C= best_c)
clf.fit(train_X, train_y)
pred_svm = clf.predict(test_X)
test_result = accuracy_score(test_y,pred_svm)


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(max_depth= 20 , random_state=0)
clf.fit(train_X, train_y)
pred_rf = clf.predict(test_X)
test_result = accuracy_score(test_y,pred_rf)