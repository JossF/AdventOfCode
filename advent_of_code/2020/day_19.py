import re
import pandas
import math

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


def load_rules(rules, msgs):
    rules_raw.update({d.split(":")[0]: d.split(":")[1] for d in rules[0].tolist()})
    for r_id, rule in rules_raw.items():
        load_rule(r_id, rule)
    load_rule("final", "11 | 11 31")
    # assert (rule_manifests['3'] == ["bb", "aa"])
    total = 0
    part_two_total = 0
    l_42 = [len(i) == len(rule_manifests["42"][0]) for i in rule_manifests["42"]]
    l_31 = [len(i) == len(rule_manifests["31"][0]) for i in rule_manifests["31"]]
    split_len = len(rule_manifests["31"][0])
    assert all(l_42) and all(l_31)
    listed_msgs = msgs[0].tolist()
    for msg_rec in listed_msgs:
        if divmod(len(msg_rec), split_len)[1] != 0:
            print(msg_rec)
            continue
        if msg_rec in rule_manifests["0"]:
            total += 1
            continue
        msg_parts = [msg_rec[split_len * i:split_len * i + split_len] for i in range(int(len(msg_rec) / split_len))]
        test31 = [m in rule_manifests["31"] for m in msg_parts]
        test42 = [m in rule_manifests["42"] for m in msg_parts]
        i = None
        for i in range(math.ceil(len(msg_parts) / 2), len(msg_parts)):
            combined_trues = test42[:i] + test31[i:]
            if all(combined_trues) and len(test31[i:]) < len(test42[:i]):
                assert (len(test31[i:]) < len(test42[:i]))
                part_two_total += 1
                print(f"Valid message from {i}: {msg_rec} \n 42: {test42} \n 31: {test31}")
                i = None
                break
        if i is not None:
            print(f"Not valid message: {msg_rec} \n 42: {test42} \n 31: {test31}")
        # print(i)

    print(total)
    print(part_two_total)
    print(total + part_two_total)


if __name__ == '__main__':
    # data_rules = pandas.read_csv(
    #     r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_19_rules_test.csv",
    #     header=None)
    # data_msg = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_19_msg_test.csv",
    #                            header=None)
    # load_rules(rules=data_rules, msgs=data_msg)
    # 277 is wrong
    data_rules = pandas.read_csv(
        r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_19_rules.csv",
        header=None)
    data_msg = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_19_msgs.csv",
                               header=None)
    load_rules(rules=data_rules, msgs=data_msg)
