

from collections import defaultdict



grammar = {
    "S'": [["E"]],
    "E": [["E", "+", "T"], ["T"]],
    "T": [["T", "*", "F"], ["F"]],
    "F": [["(", "E", ")"], ["id"]]
}

non_terminals = list(grammar.keys())


def closure(items):
    closure_set = set(items)

    while True:
        new_items = set(closure_set)

        for (head, body, dot_pos) in closure_set:
            if dot_pos < len(body):
                symbol = body[dot_pos]

                if symbol in grammar:  
                    for prod in grammar[symbol]:
                        item = (symbol, tuple(prod), 0)
                        if item not in new_items:
                            new_items.add(item)

        if new_items == closure_set:
            break
        closure_set = new_items

    return closure_set


def goto(items, symbol):
    moved = set()

    for (head, body, dot_pos) in items:
        if dot_pos < len(body) and body[dot_pos] == symbol:
            moved.add((head, body, dot_pos + 1))

    return closure(moved)


def canonical_collection():
    start_item = closure({("S'", tuple(grammar["S'"][0]), 0)})

    C = [start_item]
    transitions = []

    symbols = set()
    for head in grammar:
        for prod in grammar[head]:
            symbols.update(prod)

    while True:
        new_states = []

        for i, state in enumerate(C):
            for symbol in symbols:
                g = goto(state, symbol)
                if g and g not in C:
                    new_states.append(g)
                    transitions.append((i, symbol, len(C) + len(new_states) - 1))
                elif g:
                    transitions.append((i, symbol, C.index(g)))

        if not new_states:
            break

        C.extend(new_states)

    return C, transitions


def print_items(states):
    for i, state in enumerate(states):
        print(f"\nI{i}:")
        for (head, body, dot_pos) in state:
            body = list(body)
            body.insert(dot_pos, "•")
            print(f"{head} -> {' '.join(body)}")



states, transitions = canonical_collection()

print("LR(0) Item Sets:")
print_items(states)

print("\nTransitions:")
for t in transitions:
    print(f"I{t[0]} -- {t[1]} --> I{t[2]}")