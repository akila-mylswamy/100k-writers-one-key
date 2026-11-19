\set counter_id random(1, 50)

UPDATE counters
SET value = value + 1
WHERE id = :counter_id;
