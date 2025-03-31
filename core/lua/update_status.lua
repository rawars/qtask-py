-- Update the status of a message in a hash
local key = KEYS[1]
local field = ARGV[1]
local value = ARGV[2]

redis.call("HSET", key, field, value)
return "updated"