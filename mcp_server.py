import sys
import json
from client import ABSStreamOperator

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "snapshot_check":
        op = ABSStreamOperator("test_op", num_inputs=2)
        op.process_element(0, params.get("val1", 5))
        op.process_element(1, params.get("val2", 15))
        op.process_barrier(0, 1)
        res = op.process_barrier(1, 1)
        return res
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
