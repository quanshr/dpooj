import random, sys, json

user_path = sys.argv[1]
json_path = f"{user_path}/runargs.json"
with open(json_path, 'r') as file:
    run_args = json.load(file)

num_instr = run_args['num_instr']
mx_id = random.randint(1, 10)

for i in range(num_instr):
    op = random.randint(0, 26)
    if op == 0:
        id = random.randint(0, mx_id)
        print(f"ap {id} 0 0")
    elif op == 1:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        value = random.randint(1, 100)
        print(f"ar {id1} {id2} {value}")
    elif op == 2:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        print(f"qv {id1} {id2}")
    elif op == 3:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        print(f"qci {id1} {id2}")
    elif op == 4:
        print("qbs")
    elif op == 5:
        print("qts")
    elif op == 6:
        id = random.randint(0, mx_id)
        print(f"ag {id}")
    elif op == 7:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        print(f"atg {id1} {id2}")
    elif op == 8:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        print(f"dfg {id1} {id2}")
    elif op == 9:
        id = random.randint(0, mx_id)
        print(f"qgvs {id}")
    elif op == 10:
        id = random.randint(0, mx_id)
        print(f"qgav {id}")
    elif op == 11:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        value = random.randint(-100, 100)
        print(f"mr {id1} {id2} {value}")
    elif op == 12:
        id = random.randint(0, mx_id)
        print(f"qba {id}")
    elif op == 13:
        print(f"qcs")
    elif op == 14:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        id3 = random.randint(0, mx_id)
        value = random.randint(-1000, 1000)
        type = random.randint(0, 1)
        print(f"am {id1} {value} {type} {id2} {id3}")
    elif op == 15:
        id = random.randint(0, mx_id)
        print(f"sm {id}")
    elif op == 16:
        id = random.randint(0, mx_id)
        print(f"qsv {id}")
    elif op == 17:
        id = random.randint(0, mx_id)
        print(f"qrm {id}")
    elif op == 18:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        id3 = random.randint(0, mx_id)
        money = random.randint(0, 200)
        type = random.randint(0, 1)
        print(f"arem {id1} {money} {type} {id2} {id3}")
    elif op == 19:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        id3 = random.randint(0, mx_id)
        string_length = random.randint(1, 100)
        string = 'a' * string_length
        type = random.randint(0, 1)
        print(f"anm {id1} {string} {type} {id2} {id3}")
    elif op == 20:
        id = random.randint(0, mx_id)
        print(f"cn {id}")
    elif op == 21:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        id3 = random.randint(0, mx_id)
        emoji_id = random.randint(0, mx_id)
        type = random.randint(0, 1)
        print(f"aem {id1} {emoji_id} {type} {id2} {id3}")
    elif op == 22:
        id = random.randint(0, mx_id)
        print(f"sei {id}")
    elif op == 23:
        id = random.randint(0, mx_id)
        print(f"qp {id}")
    elif op == 24:
        id = random.randint(0, mx_id)
        print(f"dce {id}")
    elif op == 25:
        id = random.randint(0, mx_id)
        print(f"qm {id}")
    elif op == 26:
        id = random.randint(0, mx_id)
        print(f"qlm {id}")
        