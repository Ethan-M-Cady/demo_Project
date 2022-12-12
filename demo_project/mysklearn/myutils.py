import itertools
from tabulate import tabulate
import csv


def prepend_attribute_label(table, header):
    for row in table:
        for i in range(len(row)):
            row[i] = header[i] + "=" + str(row[i])


def count_in_table(rule, table):
    count = 0
    for row in table:
        count_to_len = 0
        for item in row:
            if item in rule:
                count_to_len += 1
                if count_to_len == len(rule):
                    count += 1
                    break
    return count


def compute_rule_support(rule, table, minsup):
    Nboth = 0
    for row in table:
        j = 0
        for i in range(len(rule)):
            if rule[i] in row:
                j += 1
            else:
                break
        if j == len(rule):
            Nboth += 1
    if(Nboth / len(table)) >= minsup:
        return True
    else:
        return False


def make_Lnew(Ccurr, L_prev, k, table, minsup):
    L_new = []
    for i in range(0, len(Ccurr)):
        arr_count = 0
        subset_C = []
        subset_C.extend(itertools.combinations(Ccurr[i], k-1))
        for subset_C_item in subset_C:
            for L_prev_item in L_prev:
                if list(subset_C_item) == list(L_prev_item):
                    arr_count += 1
                    break
        if len(Ccurr[i]) == arr_count and compute_rule_support(Ccurr[i], table, minsup) is True:
            L_new.append(Ccurr[i])
    return L_new


def union(arr1, arr2):
    main_arr = arr1 + arr2
    seen_vars = []
    unique_val_arr = []
    i = len(main_arr)-1
    while i > -1:
        if seen_vars.count(main_arr[i]) == 0:
            unique_val_arr.append(main_arr[i])
            seen_vars.append(main_arr[i])
        i -= 1
    return sorted(unique_val_arr)


def unique_vals(arr):
    i = len(arr)-1
    while i > -1:
        if arr.count(arr[i]) > 1:
            del arr[i]
        i -= 1
    return arr


def make_Cnew(L_old):
    C_new = []
    L_old_copy = L_old
    for i in range(0, len(L_old)):
        for j in range(0, len(L_old_copy)):
            if L_old[i][:-1] == L_old_copy[j][:-1] and L_old[i] != L_old_copy[j]:
                C_new.append(union(L_old[i], L_old_copy[j]))
    return unique_vals(C_new)


def make_Cinit_and_Linit(_table, minsup):
    unique_items = []
    for row in _table:
        for item in row:
            if unique_items.count(item) == 0:
                unique_items.append(item)
    unique_items = sorted(unique_items)

    # making it into a list of lists
    Cinit = []
    for item in unique_items:
        new_list = item.split(', ')
        Cinit.append(new_list)

    # checking support of each item
    i = len(Cinit)-1
    Linit = Cinit.copy()
    while i > -1:
        if compute_rule_support(Linit[i], _table, minsup) is False:
            del Linit[i]
        i -= 1
    return Cinit, Linit


def join_supported_itemsets(L, k):
    total_union_set = []
    for i in range(1, k-2-1):
        total_union_set.extend(union(L[i], L[i+1]))
    return total_union_set


def difference(list1, list2):
    i = len(list2)-1
    list2_copy = list2.copy()
    while i > -1:
        if list1.count(list2_copy[i]) > 0:
            del list2_copy[i]
        i -= 1
    return list2_copy


def generate_rules(table, supported_itemset, minconf):
    confidence, rules, LHS, RHS = [], [], [], []
    j = 0
    for item_set in supported_itemset:
        for i in range(1, len(item_set)):
            _list = list(itertools.combinations(item_set, i))
            for list_item in _list:
                LHS.append(list((list_item)))
                RHS.append(difference(list_item, item_set))
    for i in range(0, len(LHS)):
        Nboth = count_in_table(union(LHS[i], RHS[i]), table)
        NLeft = count_in_table(LHS[i], table)
        confidence.append(Nboth/NLeft)
        # if confidence[-1] >= 0.8:
        if confidence[-1] >= minconf:
            rules.append([])
            rules[j].append(LHS[i])
            rules[j].append(RHS[i])
            j += 1
    return unique_vals(rules) # this makes sure all of them are unique


def compute_stats(rule, table):
    Nleft, Nright, Nboth = 0, 0, 0
    Ntotal = len(table)

    left_target = rule[0]
    right_target = rule[1]
    both_target = union(rule[0], rule[1])

    for row in table:
        j = 0
        for i in range(0, len(left_target)):
            if left_target[i] in row:
                j += 1
            if j == len(left_target):
                Nleft += 1

        j = 0
        for i in range(0, len(right_target)):
            if right_target[i] in row:
                j += 1
            if j == len(right_target):
                Nright += 1

        j = 0
        for i in range(0, len(both_target)):
            if both_target[i] in row:
                j += 1
            if j == len(both_target):
                Nboth += 1
    if Nleft == 0:
        confidence = 0
    else:
        confidence = Nboth / Nleft

    support = Nboth / Ntotal

    if Nright == 0:
        lift = 0
    else:
        lift = Nboth / Nright

    return confidence, support, lift


def pretty_print_rules(rules, table):
    string_rules = []
    for i in range(0, len(rules)):
        string_rules.append([])
    i = 0
    for item in rules:
        string_rules[i] = "IF "
        for sub_item in item:
            if sub_item == item[-1]:
                string_rules[i] = (string_rules[i]) + " THEN "
            for sub_sub_item in sub_item:
                string_rules[i] = (string_rules[i]) + sub_sub_item
                if sub_sub_item != sub_item[-1]:
                    string_rules[i] = (string_rules[i]) + " AND "
        i += 1

    new_table = []
    for i in range(0, len(rules)):
        confidence, support, lift = compute_stats(rules[i], table)
        new_table.append(
            [str(i+1), string_rules[i], support, confidence, lift])

    print(tabulate(new_table, headers=[
          "#", "Rule", "Support", "Confidence", "Lift"]))


def apriori(table, minsup, minconf):
    C, L = [], []
    Cinit, Linit = make_Cinit_and_Linit(table, minsup)
    C.append(Cinit)
    L.append(Linit)
    k = 2
    keep_going = True
    for i in range(0, 999999):
        if len(L[-1]) == 0:  # if last element is empty set
            L.pop()
            break
        C.append(make_Cnew(L[i]))
        L.append(make_Lnew(C[i+1], L[-1], k, table, minsup))
        k += 1

    all_supported_itemsets = join_supported_itemsets(L, k)
    rules = generate_rules(table, all_supported_itemsets, minconf)
    return(rules)


def get_header(filename):
    with open(filename, 'r') as file:
        header = []
        header = next(csv.reader(file))
    return header