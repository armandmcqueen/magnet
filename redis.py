import redis

# setting up redis-cli on ec2: https://gist.github.com/todgru/14768fb2d8a82ab3f436#gistcomment-2189155

r = redis.Redis(
    host='magnet-redis.usphqa.ng.0001.usw2.cache.amazonaws.com',
    port=6379)

members = r.smembers('set1')
print(members)