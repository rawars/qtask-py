-- Extract a message from the beginning of the queue
local queue = KEYS[1]

local message = redis.call("LPOP", queue)
if message then
    return message
else
    return nil
end