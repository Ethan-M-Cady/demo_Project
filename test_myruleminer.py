import numpy as np
import itertools
from mysklearn import myutils

from mysklearn.myruleminer import MyAssociationRuleMiner

# toy market basket analysis dataset
transactions = [
    ["b", "c", "m"],
    ["b", "c", "e", "m", "s"],
    ["b"],
    ["c", "e", "s"],
    ["c"],
    ["b", "c", "s"],
    ["c", "e", "s"],
    ["c", "e"]
]

# interview datasset
header = ["level", "lang", "tweets", "phd", "interviewed_well"]
table = [
        ["Senior", "Java", "no", "no", "False"],
        ["Senior", "Java", "no", "yes", "False"],
        ["Mid", "Python", "no", "no", "True"],
        ["Junior", "Python", "no", "no", "True"],
        ["Junior", "R", "yes", "no", "True"],
        ["Junior", "R", "yes", "yes", "False"],
        ["Mid", "R", "yes", "yes", "True"],
        ["Senior", "Python", "no", "no", "False"],
        ["Senior", "R", "yes", "no", "True"],
        ["Junior", "Python", "yes", "no", "True"],
        ["Senior", "Python", "yes", "yes", "True"],
        ["Mid", "Python", "no", "yes", "True"],
        ["Mid", "Java", "yes", "no", "True"],
        ["Junior", "Python", "no", "yes", "False"]
]


transactions_expected = [
                        [['m'], ['b', 'c']],
                        [['b', 'm'], ['c']],
                        [['c', 'm'], ['b']],
                        [['b', 's'], ['c']],
                        [['m'], ['b']],
                        [['e'], ['c']],
                        [['e', 's'], ['c']],
                        [['m'], ['c']],
                        [['s'], ['c']]
]

table_expected = [
    [['interviewed_well=False'], ['tweets=no']],
    [['level=Mid'], ['interviewed_well=True']],
    [['phd=no', 'tweets=yes'], ['interviewed_well=True']],
    [['tweets=yes'], ['interviewed_well=True']],
    [['lang=R'], ['tweets=yes']]
]

# table_expected

# note: order is actual/received student value, expected/solution
myutils.prepend_attribute_label(table, header)


def test_association_rule_miner_fit():
    test_fit = MyAssociationRuleMiner()

    test_fit.fit(transactions)
    print(test_fit.rules)
    assert len(test_fit.rules) == len(transactions_expected)
    for i in range(0, len(test_fit.rules)):
        assert transactions_expected.count(test_fit.rules[i]) == 1

    test_fit.fit(table)
    assert len(test_fit.rules) == len(table_expected)
    for i in range(0, len(test_fit.rules)):
        assert table_expected.count(test_fit.rules[i]) == 1



#MyAssociationRuleMiner().print_association_rules(transactions)
