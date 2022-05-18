import json
import re
import sys


def calc_capacity_bps(num, unit):
  capacity_bps = 0

  if 'Bits/sec' in unit:
    capacity_bps = num
  elif 'Kbits/sec' in unit:
    capacity_bps = num * 1000
  elif 'Mbits/sec' in unit:
    capacity_bps = num * 1000000
  elif 'Gbits/sec' in unit:
    capacity_bps = num * 1000000000
  else:
    print('Unknown unit for bandwidth')

  return capacity_bps


def calc_jitter_ms(num, unit):
  jitter_ms = 0

  if 'us' in unit:
    jitter_ms = num / 1000
  elif 'ms' in unit:
    jitter_ms = num
  elif 's' in unit:
    jitter_ms = num * 1000
  else:
    print('Unknown unit for jitter')

  return jitter_ms


def main():
  args = sys.argv[1:]
  trace_log_name = args[0]
  trace_input_name = args[1]

  duration = 0.0

  trace_dict = dict()
  trace_dict['type'] = 'video'
  trace_dict['downlink'] = dict()
  trace_dict['uplink'] = dict()
  trace_dict['uplink']['trace_pattern'] = []
  trace_pattern = trace_dict['uplink']['trace_pattern']

  with open(trace_log_name) as trace_log:
    lines = [line.strip() for line in trace_log.readlines()]
    # ignore the last line (summary of iperf test):
    lines = lines[:-1]

    for line in lines:
      if 'sec' in line:
        interval_dict = dict()

        split_others = re.split(r'\s{2,}', line)
        dur = split_others[2]
        capacity = split_others[4]
        jitter = split_others[5]

        split_loss = line.split('(')
        loss_rate = int(split_loss[1].split('%'[0])[0])

        # Duration of each interval is uniform
        if duration == 0.0:
          dur_list = dur.split(' ')
          begin_sec = float(dur_list[0].split('-')[0])
          end_sec = float(dur_list[1])
          duration = end_sec - begin_sec

        # Capacity
        num = float(capacity.split(' ')[0])
        unit = capacity.split(' ')[1]
        capacity_bps = calc_capacity_bps(num, unit)

        # Jitter
        num = float(jitter.split(' ')[0])
        unit = jitter.split(' ')[1]
        jitter_ms = calc_jitter_ms(num, unit)

        # Add network statistics during current interval
        interval_dict['duration'] = duration
        interval_dict['capacity'] = capacity_bps
        interval_dict['jitter'] = jitter_ms
        interval_dict['loss'] = loss_rate
        trace_pattern.append(interval_dict)

  # Save the trace in a json format
  with open(f'{trace_input_name}', 'w') as trace_input:
      trace_input.write(json.dumps(trace_dict, indent = 4))


if __name__ == '__main__':
  main()
