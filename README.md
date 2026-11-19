# 100K Writers, One Key

A reproducible PostgreSQL experiment exploring hot-row
contention and sharded counters.

## Research question

How does distributing atomic counter increments across
multiple PostgreSQL rows affect throughput and latency?

## Environment

- macOS 27.2.1
- Apple Silicon, Mac16,1
- 10 CPU cores, 16 GiB RAM
- PostgreSQL 18.7 (Homebrew)
- fsync = on
- synchronous_commit = on
- shared_buffers = 128MB
- max_connections = 100

PostgreSQL and pgbench ran on the same Mac.

## Workloads

1. hotkey.sql: Every transaction increments row 1.
2. sharded_5.sql: Randomly increments one of 5 rows.
3. sharded_random.sql: Randomly increments one of 50 rows.

Each benchmark uses:
- 50 concurrent clients
- 5 pgbench worker threads
- 2,000 transactions per client
- 100,000 total transactions

These are 100,000 total increments, NOT 100,000
simultaneous database connections.

## Reproduce the experiment

Create a fresh database:

    createdb hotkey_lab_repro
    psql -d hotkey_lab_repro -f schema.sql
    psql -d hotkey_lab_repro -f seed.sql

Reset counters before each benchmark:

    psql -d hotkey_lab_repro \
      -c "UPDATE counters SET value = 0;"

Example benchmark:

    pgbench -n -c 50 -j 5 -t 2000 \
      -f hotkey.sql -r -l -P 5 \
      --log-prefix=repro_hot \
      hotkey_lab_repro

Change the script and log prefix to test other workloads.

After each benchmark, verify:

    psql -d hotkey_lab_repro \
      -c "SELECT SUM(value) FROM counters;"

Expected result: 100000.
Expected failed transactions: 0.

## Controlled benchmark results

| Workload | Round 1 TPS | Round 2 TPS | Round 3 TPS |
|---|---:|---:|---:|
| 1 hot row | 11270.270 | 11473.167 | 11412.742 |
| 5 random shards | 28518.962 | 27281.877 | 28615.439 |
| 50 random shards | 76814.237 | 79055.633 | 81913.499 |

## p99 transaction latency (milliseconds)

| Workload | Round 1 | Round 2 | Round 3 |
|---|---:|---:|---:|
| 1 hot row | 20.523 | 20.313 | 20.204 |
| 5 random shards | 11.001 | 12.083 | 10.950 |
| 50 random shards | 5.649 | 5.510 | 5.498 |

p99 values were calculated from raw pgbench transaction
logs using the nearest-rank percentile method.

## Summary

Median throughput:
- 1 hot row: 11,413 TPS
- 5 shards: 28,519 TPS
- 50 shards: 79,056 TPS

The 50-shard workload achieved approximately 6.93x
the median throughput of the single-hot-row workload.

Median of per-run p99 latencies:
- 1 hot row: 20.313 ms
- 5 shards: 11.001 ms
- 50 shards: 5.510 ms

The 50-shard workload reduced median-of-run p99
latency by approximately 72.9%.

## Limitations

- Local single-machine experiment.
- Load generator and database share system resources.
- Three controlled rounds per configuration.
- Tests ran sequentially, with workload order rotated.
- Results apply to this workload and environment.
- Sharded counters require aggregation to read the total.
- The experiment does not isolate every source of latency.

These are measured observations, not universal
PostgreSQL performance guarantees.
