#!/usr/bin/env python
#this is a benchmark for iterations of a sha256 base64 encoded to compact the hash
import hashlib
import datetime
import base64

password="mypretendpassword"
salt="some-crappy-salt-that-should-be-random-in-practice-and-stored-with-the-hash-for-calculating-later"
#Generate as many iterations as possible within the following time constraint (microseconds)
hash_target_time=500000

def bench_hash_iterations(algorithm,password,salt,hash_target_time):
  """
    Returns dictionary of results
  """
  iterations=1
  endtime=None
  hash_obj=hashlib.new(name=algorithm,string=password+salt)
  starttime=datetime.datetime.now()
  while True:
    #only calculate the time every other iteration
    if iterations & 1 == 0:
      time=datetime.datetime.now()-starttime
      if time.seconds > 0 or time.microseconds >= hash_target_time:
        endtime=time
        break
    #update hash using the hexdigest and salt
    hash_obj.update(hash_obj.hexdigest()+salt)
    iterations+=1

  return {"name": hash_obj.name,"iterations":iterations,"hexdigest":hash_obj.hexdigest(),"b64digest":base64.b64encode(hash_obj.digest()).strip(),"time":endtime.microseconds}

algs=["md5","sha1","sha224","sha256","sha384","sha512"]

for alg in algs:
  results=bench_hash_iterations(algorithm=alg,password=password,salt=salt,hash_target_time=hash_target_time)
  print "Algorithm: %(name)s\nRun time (microseconds): %(time)d\nIterations: %(iterations)s\nHex Digest: %(hexdigest)s\nBase64 Digest: %(b64digest)s" % results
  print ""
