import re
import pandas

rule_lengths = {}
rule_manifests = {}
rules_raw = {}


def load_rule(rule_id, rule_str):
    g = [re.findall(r"([0-9]+)", opt_rule) for opt_rule in rule_str.split("|")]
    if g == [[]]:
        rule_lengths[rule_id] = 1
        rule_manifests[rule_id] = [str(rule_str.strip().replace('"', ''))]
    elif rule_id in rule_manifests:
        return
    else:
        manifests = []
        for opt_rule in g:
            temp_manifest = []
            for opt_id in opt_rule:
                load_rule(opt_id, rules_raw.get(opt_id))
                new_ends = rule_manifests[opt_id]
                if not temp_manifest:
                    temp_manifest = new_ends
                else:
                    temp_manifest = ["".join(x + y) for x in temp_manifest for y in new_ends]
            manifests.extend(temp_manifest)
        rule_manifests[rule_id] = manifests


def load_rules():
    data_rules = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_19_rules.csv",
                                 header=None)
    data_msg = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_19_msgs.csv",
                               header=None)
    rules_raw.update({d.split(":")[0]: d.split(":")[1] for d in data_rules[0].tolist()})
    for r_id, rule in rules_raw.items():
        load_rule(r_id, rule)
    load_rule("final", "11 | 11 31")
    assert (rule_manifests['3'] == ["bb", "aa"])
    total = 0
    part_two_total = 0
    l_42 = [len(i) == 8 for i in rule_manifests["42"]]
    l_31 = [len(i) == 8 for i in rule_manifests["31"]]
    assert all(l_42) and all(l_31)
    for msg_rec in data_msg[0].tolist():
        if divmod(len(msg_rec), 8)[1] != 0:
            continue
        if msg_rec in rule_manifests["0"]:
            total += 1
            continue
        msg_parts = [msg_rec[8 * i:8 * i + 8] for i in range(int(len(msg_rec) / 8))]
        match_31 = True
        match_42 = False
        switcher = None
        for i in reversed(range(len(msg_parts))):
            if match_31:
                if msg_parts[i] in rule_manifests["31"]:
                    if all([x in rule_manifests["42"] for x in msg_parts[:i + 1]]):
                        switcher = i
                        break
                    continue
                else:
                    match_31 = False
                    match_42 = True
                    switcher = i
            if match_42:
                if msg_parts[i] in rule_manifests["42"]:
                    continue
                else:
                    match_42 = False
        if (match_31 or match_42) and (switcher or 0) > -1 + len(msg_parts) / 2:
            assert (all([x in rule_manifests["42"] for x in msg_parts[:switcher + 1]]))
            assert (all([x in rule_manifests["31"] for x in msg_parts[switcher + 1:]]))
            part_two_total += 1

    print(total)
    print(part_two_total)
    print(total + part_two_total)


if __name__ == '__main__':
    load_rules()
