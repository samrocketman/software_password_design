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
  endtime1=datetime.timedelta()
  endtime2=datetime.timedelta()
  #Calculate the initial value to start benchmark
  starttime1=datetime.datetime.now()
  iterations=1
  hash_obj=hashlib.new(name=algorithm,string=password+salt)
  while True:
    #only calculate the time every other iteration
    if iterations & 1 == 0:
      time=datetime.datetime.now()-starttime1
      if time.seconds > 0 or time.microseconds >= hash_target_time:
        endtime1=time
        break
    #update hash using the hexdigest and salt
    hash_obj.update(hash_obj.hexdigest()+salt)
    iterations+=1
  #calculate time to do iterations without tracking time
  while endtime2.microseconds < hash_target_time:
    hash_obj2=hashlib.new(name=algorithm,string=password+salt)
    starttime=datetime.datetime.now()
    i=1
    while i<iterations:
      hash_obj2.update(hash_obj2.hexdigest()+salt)
      i+=1
    endtime2=datetime.datetime.now()-starttime
    if endtime2.microseconds < hash_target_time:
      iterations+=int(float(endtime2.microseconds)/float(hash_target_time)*float(iterations))/10

  return {"name": hash_obj.name,"iterations":iterations,"hexdigest":hash_obj.hexdigest(),"b64digest":base64.b64encode(hash_obj.digest()).strip(),"actualtime":endtime2.microseconds}

algs=["md5","sha1","sha224","sha256","sha384","sha512"]

for alg in algs:
  results=bench_hash_iterations(algorithm=alg,password=password,salt=salt,hash_target_time=hash_target_time)
  print "Algorithm: %(name)s\nIterations: %(iterations)s\nCalcuted time for iterations (microseconds): %(actualtime)s\nHex Digest: %(hexdigest)s\nBase64 Digest: %(b64digest)s" % results
  print ""
