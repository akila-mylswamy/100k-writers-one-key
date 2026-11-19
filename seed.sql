-- Initialize 50 counter rows for the benchmark.
-- Run only after creating the table in a fresh database.

INSERT INTO public.counters (id, value)
SELECT id, 0
FROM generate_series(1, 50) AS id;
