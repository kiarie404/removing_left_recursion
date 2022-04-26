from sly import Lexer
import json

# Removes '<' and '>' from a string
def stringify_nt(nt):
    txt = ""
    for ch in nt:
        if ch != '<' and ch != '>':
            txt += ch
    return txt

# Checks whether an item is in an array
def check_arr(item,arr):
    for val in arr:
        if val == item:
            return True
    return False

# Scans the input file and determines whether its contents are
# terminals or non_terminals
def get_rules(in_file):
    class CalcLexer(Lexer):
        tokens = { TERMINAL, NON_TERMINAL }

        ignore = ' \t'
        ignore_rule = '::='
        ignore_newline = '\n'

        TERMINAL      = r'[a-zA-Z_]+'
        NON_TERMINAL  = r'(<\w+>)+'
    lexer = CalcLexer()
    rules = []
    for line in in_file:
        rule = []
        for tok in lexer.tokenize(line):
            my_dict = {"token_type":tok.type,"token_value":tok.value}
            rule.append(my_dict)
        rules.append(rule)
    return rules

# Returns an array for productions associated with a
# given non_terminal
def productions(val,rules):
    arr_1 = []
    for rule in rules:
        arr_2 = []
        if len(rule) != 0:
            my_dict = rule[0]
            if my_dict["token_value"] == val:
                for i in range(1,len(rule)):
                    arr_2.append(rule[i])
                arr_1.append(arr_2)
    return arr_1

# Returns a dictionary containing the productions
# of a particular non_terminal
def jsonify(non_terminal,prod_list):
    main_dict = {
        "token_value":"{}".format(stringify_nt(non_terminal)),
        "productions": []
    }
    main_ls = []
    for prod in prod_list:
        if len(prod) != 0:
            sec_ls = []
            for item in prod:
                sec_dict = {
                    "token_type":"{}".format(item["token_type"].lower()),
                    "token_value":"{}".format(stringify_nt(item["token_value"]))
                }
                sec_ls.append(sec_dict)
            main_ls.append(sec_ls)
    main_dict["productions"] = main_ls
    return main_dict

# Returns a list of dictionaries containing the rules
# from the bnf
def left_nt(rules):
    arr = []
    out_arr = []
    for rule in rules:
        if len(rule) != 0:
            non_terminal = rule[0]
            if not check_arr(non_terminal["token_value"],arr):
                arr.append(non_terminal["token_value"])
                prod_list = productions(non_terminal["token_value"],rules)
                out_arr.append(jsonify(non_terminal["token_value"],prod_list))
    return out_arr

def bnf_to_json(in_file,out_file):
    out = {"bnf": []}
    out["bnf"] = left_nt(get_rules(in_file))
    json_object = json.dumps(out,indent=4)
    out_file.write(json_object)

if __name__ == '__main__':
    in_file = open("bnf.txt","r")
    out_file = open("bnf.json","w")

    bnf_to_json(in_file,out_file)
