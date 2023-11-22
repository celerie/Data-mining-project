import itertools
class HashTreeNode:
    def __init__(self, item=None, count=0):
        self.item = item
        self.count = count
        self.children = {}

def generate_candidates(frequent_items, k):

    #print(k, frequent_items)
    candidates = set([])
    for item1 in frequent_items:
        for item2 in frequent_items:
            if len(item1.union(item2)) == k:
                candidates.add(frozenset(item1.union(item2)))
    #print(candidates)
    return candidates

def calculate_support(transactions, itemset):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count

def apriori_algorithm(transactions, min_support, min_confidence):
    # Generate frequent 1-itemsets
    itemsets = [set([item]) for item in set.union(*[set(i) for i in transactions])]
    frequent_itemsets = [itemset for itemset in itemsets if calculate_support(transactions, itemset) >= min_support]

    # Dictionary to store support counts for frequent itemsets
    support_counts = {frozenset(itemset): calculate_support(transactions, itemset) for itemset in frequent_itemsets}

    k = 2
    while frequent_itemsets:
        # Build hash tree for frequent itemsets
        hash_tree = build_hash_tree(frequent_itemsets)


        # Generate candidate itemsets
        candidates = generate_candidates(frequent_itemsets, k)

        # Prune candidates using hash tree
        #candidates = prune_candidates(candidates, hash_tree, k - 1)

        # Calculate support for candidates
        frequent_itemsets = [itemset for itemset in candidates if calculate_support(transactions, itemset) >= min_support]

        support_counts.update({frozenset(itemset): calculate_support(transactions, itemset) for itemset in frequent_itemsets})

        # Generate association rules
        generate_association_rules(transactions, frequent_itemsets, min_confidence)
        print(k)
        k += 1

    return support_counts

def build_hash_tree(itemsets):
    root = HashTreeNode()
    for itemset in itemsets:
        current_node = root
        for item in itemset:
            if item in current_node.children:
                current_node.children[item].count += 1
            else:
                new_node = HashTreeNode(item, 1)
                current_node.children[item] = new_node
                current_node = new_node
    return root

def prune_candidates(candidates, hash_tree, k):
    pruned_candidates = set([])
    for candidate in candidates:
        subset = frozenset(candidate) - {next(iter(candidate))}
        if is_subset_in_hash_tree(subset, hash_tree, k):
            pruned_candidates.add(candidate)
    return pruned_candidates

def is_subset_in_hash_tree(subset, hash_tree, k):
    current_node = hash_tree
    for item in subset:
        if item in current_node.children:
            current_node = current_node.children[item]
        else:
            return False
    return current_node.count >= k

def generate_association_rules(transactions, frequent_itemsets, min_confidence):
    for itemset in frequent_itemsets:
        for i in range(1, len(itemset)):
            for subset in itertools.combinations(itemset, i):
                antecedent = frozenset(subset)
                consequent = itemset - antecedent
                support_itemset = calculate_support(transactions, itemset)
                support_antecedent = calculate_support(transactions, antecedent)
                confidence = support_itemset / support_antecedent
                if confidence >= float(min_confidence):
                    print(f"{set(antecedent)} => {set(consequent)}: Support = {support_itemset}, Confidence = {confidence}")

# Example usage
transactions = [    
    {"1", "2", "3", "3"},
    {"1", "2", "3"},
    {"1", "3"},
    {"1", "2", "3"},
    {"1", "2"},
    {"1", "2", "3"},
    {"3", "2"}
    ]
min_support = 2
min_confidence = 0.001


freq_itemsets = apriori_algorithm(transactions, min_support, min_confidence)
print('+'*100)
print()
for k,v in freq_itemsets.items():
    print(set(k), "Support = ", v)
