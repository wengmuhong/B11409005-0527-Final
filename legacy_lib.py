import os

d2 = []
F_NAME = "lib_data.txt"

def load_proc():
    if os.path.exists(F_NAME):
        f = open(F_NAME, "r", encoding="utf-8")
        l1 = f.readlines()
        for x in l1:
            p = x.strip().split("@@")
            p2 = p[1].split("##")
            d2.append({"t": p[0], "i": p2[0], "s": p2[1]})
        f.close()

def c_res(v):
    for b in d2:
        if b['i'] == v:
            return True
    return False

def main():
    load_proc()
    print("=== 圖書管理系統 v0.1 (Legacy) ===")
    
    while True:
        op = input("> ").strip()
        
        if op == "exit":
            f = open(F_NAME, "w", encoding="utf-8")
            for b in d2:
                f.write(f"{b['t']}@@{b['i']}##{b['s']}\n")
            f.close()
            print("系統關閉")
            break
            
        elif op.startswith("add "):
            raw = op[4:].split("/")
            if len(raw) == 3:
                if not c_res(raw[1]):
                    d2.append({"t": raw[0], "i": raw[1], "s": raw[2]})
                    print("Success")
                else:
                    print("ISBN Exist")
            else:
                print("Format Error")
                
        elif op == "show":
            for b in d2:
                print(f"書名: {b['t']}, ISBN: {b['i']}, 狀態: {b['s']}")
                
        elif op.startswith("borrow "):
            target_isbn = op[7:]
            for b in d2:
                if b['i'] == target_isbn:
                    b['s'] = "borrowed"
                    print("Updated")
        else:
            print("Unknown Command")

if __name__ == "__main__":
    main()