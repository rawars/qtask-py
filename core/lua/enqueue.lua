-- Arguments:
-- KEYS[1]: counter_key - the counter key (e.g: counter:WHATSAPP:batch1)
-- KEYS[2]: task_prefix - prefix for the task key (e.g: task:WHATSAPP:batch1)
-- KEYS[3]: pending_queue - pending tasks queue (e.g: pending:WHATSAPP:batch1)
-- ARGV[1]: task_data - task data in JSON format

-- Generate new ID
local task_id = redis.call('INCR', KEYS[1])

-- Create the full task key
local task_key = KEYS[2] .. ":" .. task_id

-- Save the task
redis.call('HSET', task_key, 'data', ARGV[1])

-- Add to the pending queue
redis.call('RPUSH', KEYS[3], task_key)

-- Return the ID and the task key
return {task_id, task_key}