import sys
from Scripts.init import init
from Scripts.build import build
from Scripts.add_repo import add_package
from Scripts.remove_repo import remove_package
from Scripts.remove_db import remove_db
# assume these are already imported
# from commands import add, remove, init, build
def help_menu():
    print("""
Crucible Commands:
  add {--db} <repo>
  remove {--db} <name>
  init
  build {--output <path>}
""")

def main():
    args = sys.argv[1:]

    if not args:
        help_menu()
        return

    cmd = args[0]

    if cmd == "add":
        use_db = "--db" in args
        silent = "--silent" in args

        args = [a for a in args[1:] if a not in ["--db", "--silent"]]

        if len(args) != 1:
            help_menu()
            return

        repo = args[0]
        if use_db:
            # add_db(repo, silent)
            print(f"Adding repo: {repo} to database")
        elif use_db == False:
            repstring = str(repo)
            print(f"Adding repo: {repo} to config file")
            add_package(repstring, silent)
            
        else:
            raise ValueError("Script could not determine whether to use db or not. Please specify --db or omit it.")
        # add(repo, db=use_db)
        print(f"Adding repo: {repo} with db={use_db}")
        
    elif cmd == "remove":
        use_db = "--db" in args
        silent = "--silent" in args

        args = [a for a in args[1:] if a not in ["--db", "--silent"]]

        if len(args) != 1:
            help_menu()
            return

        name = args[0]
        if use_db:
            remove_db(name, silent)
        elif use_db == False:
            remove_package(name, silent)
            print(f"Removing repo: {name} with db={use_db}")

    elif cmd == "init":
        silent = "--silent" in args
        
        args = [a for a in args[1:] if a != "--silent"]
        
        init(silent)

    elif cmd == "build":
        if "--output" in args:
            i = args.index("--output")
            try:
                path = args[i + 1]
            except IndexError:
                help_menu()
                return
            build(path)
        else:
            build()

    else:
        help_menu()


if __name__ == "__main__":
    main()