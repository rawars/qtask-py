-- Returns the length of the queue
local queue = KEYS[1]

local len = redis.call("LLEN", queue)
return tostring(len)