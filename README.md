# Purpose


The purpose of this little project is to show how easy it is to generate many iterations of hashes.  It is also proving a point that if you're say doing "thousands" of iterations of rehashing a password (as I've heard a few times in PR blog posts for companies who get compromised) with a salt it simply is not enough.  And if you're not using hashing or using hashing without a salt that's just plain irresponsible.  If you catch someone doing that you should email [Plain Text Offenders][1] to disclose this bad practice.  If you want to learn more about password hashing in applications I recommend reading this [Crack Station article][2].

That being said here I'll show you some simple benchmarks as well as make a proposal for a better password hashing system which will dynamically evolve over time as websites are upgraded over time.

# Simple benchmarks

These benchmarks are the output of the `pword_hash_benchmark.py` script.

```
Algorithm: md5
Benchmark run time (seconds): 5.68
Iterations: 422267
End user calcuted time for iterations (microseconds): 501284
Hex Digest: 36e0a31298e02aef78f9e81709e4a357
Base64 Digest: NuCjEpjgKu94+egXCeSjVw==

Algorithm: sha1
Benchmark run time (seconds): 3.99
Iterations: 377438
End user calcuted time for iterations (microseconds): 507053
Hex Digest: ce064e13bebe7704e45519b4fef283f62f6cff73
Base64 Digest: zgZOE76+dwTkVRm0/vKD9i9s/3M=

Algorithm: sha224
Benchmark run time (seconds): 1.63
Iterations: 208756
End user calcuted time for iterations (microseconds): 502383
Hex Digest: ce9e1e8eb057df7f2a385268238a992553b6392a72d3864890623a7b
Base64 Digest: zp4ejrBX338qOFJoI4qZJVO2OSpy04ZIkGI6ew==

Algorithm: sha256
Benchmark run time (seconds): 4.41
Iterations: 217354
End user calcuted time for iterations (microseconds): 500243
Hex Digest: a82f37ea2ccdecd5d78a66e6419cb825a9a1cd92a0d6419b2f9762f80173b673
Base64 Digest: qC836izN7NXXimbmQZy4JamhzZKg1kGbL5di+AFztnM=

Algorithm: sha384
Benchmark run time (seconds): 8.20
Iterations: 343489
End user calcuted time for iterations (microseconds): 499149
Hex Digest: f2e360ef380b3c211a109828718181d312999abc050556bf8a061862e96b32b2e29d68bb92637d5431c87009221d904e
Base64 Digest: 8uNg7zgLPCEaEJgocYGB0xKZmrwFBVa/igYYYulrMrLinWi7kmN9VDHIcAkiHZBO

Algorithm: sha512
Benchmark run time (seconds): 2.19
Iterations: 210719
End user calcuted time for iterations (microseconds): 506117
Hex Digest: f24cf9419c725b2e0fad47d92fcf217b67de353c930f48a168425114fce2a30497f37d2c1fb3defd39d74721b6cc2da866031d1091dd3a5249876ad9d5776eb3
Base64 Digest: 8kz5QZxyWy4PrUfZL88he2feNTyTD0ihaEJRFPziowSX830sH7Pe/TnXRyG2zC2oZgMdEJHdOlJJh2rZ1Xdusw==

```

# A proposal for key stretching

So normally a decent password hashing function in an application will have:

* Use a well known cryptographic hash algorithm that doesn't have any known or proven collisions and has been adequately peer reviewed by the security community.
* Hash multiple iterations of the hash it is using.
* The function will use a salt to generate unique hashes.  A salt is basically just a random string of characters to append to the input password which will then be hashed.
* The salt will be different for each password hash in the database.
* The salt is stored in a field with the password hash so that calculating the hash is repeatable.
* Encrypted hashes in the database with the key to the encryption stored on the local filesystem (not in the database) with local filesystem access disabled for the database if it supports it (in case of an SQL injection attack only).

So a pretend database entry for a user will look something like the following.

```
Username | Password (hashed+encrypted) | Salt
```

I propose updating said pretend database entry.

```
Username | Password (hashed+encrypted) | Salt | Iterations
```

The reason why the iterations are stored in the database is because it should be updated as performance in your service is upgraded.  This means if you get more robust hardware (i.e. replace it every few years) you'll get stronger password storage out of the box with little effort.

So I propose doing the following.  When your application first starts up it runs a quick benchmark on the number of password hash iterations it can perform in say `500ms` (or some arbitrary time you're willing to wait for the hash to be computed on your hosted system).  This will be the estimated performance metric for the number of iterations the password should be hashed.  All new passwords will be be created with this number of hashes.

If your application restarts then the benchmark calculation for number of iterations is run during startup.  This will be the new value.  If an existing user is logging in and the number of iterations their stored password is hashed is different beyond a threshold then their hash will be recalculated with the new system benchmark for number of hash iterations.  In addition to the user login hash recalculation there should be an external job that periodically runs to adjust the hashes of the users based on the benchmarked number of iterations stored in the database for the current runtime.

With this method the strength of your password hashing should increase as the performance of the systems your service lies on increases at no extra cost to you.

[1]: http://plaintextoffenders.com/
[2]: https://crackstation.net/hashing-security.htm
