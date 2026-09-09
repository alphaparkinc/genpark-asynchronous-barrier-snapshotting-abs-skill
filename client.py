class ABSStreamOperator:
    """Asynchronous Barrier Snapshotting (ABS) Stream Operator."""
    def __init__(self, op_id, num_inputs=1):
        self.op_id = op_id
        self.num_inputs = num_inputs
        self.state = 0
        self.barriers_received = {}
        self.blocked_channels = set()
        self.snapshots = {}

    def process_element(self, channel_id, element):
        if channel_id in self.blocked_channels:
            return None
        self.state += element
        return self.state

    def process_barrier(self, channel_id, checkpoint_id):
        if checkpoint_id not in self.barriers_received:
            self.barriers_received[checkpoint_id] = set()

        self.barriers_received[checkpoint_id].add(channel_id)
        self.blocked_channels.add(channel_id)

        if len(self.barriers_received[checkpoint_id]) == self.num_inputs:
            self.snapshots[checkpoint_id] = self.state
            self.blocked_channels.clear()
            return {'status': 'SNAPSHOT_COMPLETE', 'checkpoint_id': checkpoint_id, 'state': self.state}
        return {'status': 'WAITING_ALIGNMENT', 'received': len(self.barriers_received[checkpoint_id])}
