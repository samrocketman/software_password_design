#!/usr/bin/env python
#this is a benchmark for iterations of a sha256 base64 encoded to compact the hash
import hashlib
import datetime
import base64
import time

password="mypretendpassword"
salt="some-crappy-salt-that-should-be-random-in-practice-and-stored-with-the-hash-for-calculating-later"
#Generate as many iterations as possible near the following time constraint (microseconds)
hash_target_time=500000
#advanced settings
#highest time threshold allowed to be over hash_target_time (microseconds)
#note the more strict the threshold is the longer the benchmark could take
threshold=10000
#To avoid an infinite loop set a cancel count for the loop going above and below the hash_target_time
cancelcount_threshold=100

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
      intermediate_time=datetime.datetime.now()-starttime1
      if intermediate_time.seconds > 0 or intermediate_time.microseconds >= hash_target_time:
        endtime1=intermediate_time
        break
    #update hash using the hexdigest and salt
    hash_obj.update(hash_obj.hexdigest()+salt)
    iterations+=1
  #calculate time to do iterations without tracking time
  lastiterations=0
  cancelcount=0
  startcancelcount=False
  while endtime2.microseconds < hash_target_time or endtime2.microseconds - hash_target_time > threshold:
    hash_obj2=hashlib.new(name=algorithm,string=password+salt)
    starttime=datetime.datetime.now()
    i=1
    while i<iterations:
      hash_obj2.update(hash_obj2.hexdigest()+salt)
      i+=1
    endtime2=datetime.datetime.now()-starttime
    if endtime2.microseconds < hash_target_time:
      iterations+=int(float(endtime2.microseconds)/float(hash_target_time)*float(iterations))/2
    else:
      startcancelcount=True
      iterations-=int((float(endtime2.microseconds)/float(hash_target_time)-1)*float(iterations))/2
    #debug to show the cancelcount in action
    #print cancelcount,iterations-lastiterations,lastiterations,iterations,endtime2.microseconds
    lastiterations=iterations
    #logic to break out of infinite loop if going back and forth between greater and lesser than hash_target_time
    if startcancelcount and cancelcount > cancelcount_threshold:
      break
    if startcancelcount and endtime2.microseconds > hash_target_time:
      cancelcount+=1

  return {"name": hash_obj.name,"iterations":iterations,"hexdigest":hash_obj.hexdigest(),"b64digest":base64.b64encode(hash_obj.digest()).strip(),"actualtime":endtime2.microseconds}

algs=["md5","sha1","sha224","sha256","sha384","sha512"]

for alg in algs:
  start=time.clock()
  results=bench_hash_iterations(algorithm=alg,password=password,salt=salt,hash_target_time=hash_target_time)
  end=time.clock()-start
  results["benchtime"]=float(end)
  print "Algorithm: %(name)s\nBenchmark run time (seconds): %(benchtime).2f\nIterations: %(iterations)s\nEnd user calcuted time for iterations (microseconds): %(actualtime)s\nHex Digest: %(hexdigest)s\nBase64 Digest: %(b64digest)s" % results
  print ""
