from client import ABSStreamOperator

def main():
    print("=== Testing Asynchronous Barrier Snapshotting ===")
    op = ABSStreamOperator(op_id="agg_op", num_inputs=2)
    op.process_element(0, 10)
    op.process_element(1, 20)

    # Barrier from channel 0 arrives
    res1 = op.process_barrier(0, checkpoint_id=42)
    print("Channel 0 barrier:", res1)
    assert res1['status'] == 'WAITING_ALIGNMENT'

    # Barrier from channel 1 arrives -> alignment complete & snapshot saved
    res2 = op.process_barrier(1, checkpoint_id=42)
    print("Channel 1 barrier:", res2)
    assert res2['status'] == 'SNAPSHOT_COMPLETE'
    assert op.snapshots[42] == 30

    print("ABS Stream Operator verified successfully!")

if __name__ == '__main__':
    main()
