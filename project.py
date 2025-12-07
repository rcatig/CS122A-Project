import sys
from db_utils import print_bool, normalize_arg
from data_operations import (
    import_data,
    insert_agent_client,
    add_customized_model,
    delete_base_model
)
from query_operations import (
    list_internet_service,
    count_customized_model,
    top_n_duration_config,
    list_base_model_keyword,
    print_nl2sql_result
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 project.py <function> [params...]")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "import":
        if len(args) != 1:
            print_bool(False)
            return
        ok = import_data(args[0])
        print_bool(ok)

    elif cmd == "insertAgentClient":
        ok = insert_agent_client(args)
        print_bool(ok)

    elif cmd == "addCustomizedModel":
        if len(args) != 2:
            print_bool(False)
            return
        mid = int(args[0])
        bmid = int(args[1])
        ok = add_customized_model(mid, bmid)
        print_bool(ok)

    elif cmd == "deleteBaseModel":
        if len(args) != 1:
            print_bool(False)
            return
        bmid = int(args[0])
        ok = delete_base_model(bmid)
        print_bool(ok)

    elif cmd == "listInternetService":
        if len(args) != 1:
            return
        bmid = int(args[0])
        list_internet_service(bmid)

    elif cmd == "countCustomizedModel":
        count_customized_model(args)

    elif cmd == "topNDurationConfig":
        if len(args) != 2:
            return
        uid = int(args[0])
        N = int(args[1])
        top_n_duration_config(uid, N)

    elif cmd == "listBaseModelKeyWord":
        if len(args) != 1:
            return
        keyword = normalize_arg(args[0])
        list_base_model_keyword(keyword)

    elif cmd == "printNL2SQLresult":
        print_nl2sql_result()

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
