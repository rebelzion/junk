opp_you_to_score = {
    ("A", "X"): 3,
    ("A", "Y"): 6,
    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("B", "Y"): 3,
    ("B", "Z"): 6,
    ("C", "X"): 6,
    ("C", "Y"): 0,
    ("C", "Z"): 3
}

scores_to_op_you = {}
for k, v in opp_you_to_score.items():
    if v not in scores_to_op_you:
        scores_to_op_you[v] = []
    scores_to_op_you[v].append(k)



# Read the strategy guide from the input
total_score = 0
for line in open("input.txt"):
    opponent, you = line.strip().split(" ")

    # >>> This is for Level 2. Comment out if you want to solve Level 1.
    if you == "X":
        outcome = 0
    elif you == "Y":
        outcome = 3
    elif you == "Z":
        outcome = 6
    for _op,_you in scores_to_op_you[outcome]:
        if _op == opponent:
            you = _you
            break
    # <<<

    if you == "X":
        total_score += 1
    elif you == "Y":
        total_score += 2
    elif you == "Z":
        total_score += 3
    total_score += opp_you_to_score[(opponent, you)]

    # print(f"{total_score=}")

print(total_score)
