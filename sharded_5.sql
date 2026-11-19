\set counter_id random(1, 5)

UPDATE counters
SET value = value + 1
WHERE id = :counter_id;
