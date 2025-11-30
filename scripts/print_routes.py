import traceback

def main():
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from app import app
        rules = sorted([str(r) for r in app.url_map.iter_rules()])
        print('\n'.join(rules))
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
