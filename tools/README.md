# Trace collection

1. Run iperf on both sender and receiver sides.

- `-s`: server side
- `-c`: client side
- `-u`: UDP
- `-i 5`: 5 second uniform interval

```bash
# Sender side:
# (interval should be fine-grained: at least 1 second)
iperf -s -u -i 1 2>&1 | tee [trace log]
# Receiver side:
iperf -c [sender's ip] -u
```

2. Format `trace.log` into .json format trace input to simulator.

```bash
parse_iperf_trace_log.py [trace log] [trace input]
```

For example:
- trace log name: trace.log
- trace input name: LZ\_to\_AH.json

```bash
parse_iperf_trace_log.py trace.log ../traces/LZ_to_AH.json
```




