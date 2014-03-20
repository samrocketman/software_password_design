# Purpose


The purpose of this little project is to show how easy it is to generate many iterations of hashes.  It is also proving a point that if you're say doing "thousands" of iterations of rehashing a password (as I've heard a few times in PR blog posts for companies who get compromised) with a salt it simply is not enough.  And if you're not using hashing or using hashing without a salt that's just plain irresponsible.  If you catch someone doing that you should email [Plain Text Offenders][1] to disclose this bad practice.  If you want to learn more about password hashing in applications I recommend reading this [Crack Station article][2].

That being said here I'll show you some simple benchmarks as well as make a proposal for a better password hashing system which will dynamically evolve over time as websites are upgraded over time.

# Simple benchmarks

These benchmarks are the output of the `pword_hash_benchmark.py` script.

```
Algorithm: md5
Benchmark run time (seconds): 3.82
Iterations: 434823
End user calcuted time for iterations (microseconds): 506467
Hex Digest: 77149fdf85a361b6b0365fab5f429c5a
Base64 Digest: dxSf34WjYbawNl+rX0KcWg==

Algorithm: sha1
Benchmark run time (seconds): 3.99
Iterations: 410879
End user calcuted time for iterations (microseconds): 508803
Hex Digest: fa4124bfdc924a7861efc260f889576c097d545b
Base64 Digest: +kEkv9ySSnhh78Jg+IlXbAl9VFs=

Algorithm: sha224
Benchmark run time (seconds): 1.64
Iterations: 228632
End user calcuted time for iterations (microseconds): 502472
Hex Digest: 65cd45e4afabfeef1436325a884de5434cf4b0de570ae7066c376914
Base64 Digest: Zc1F5K+r/u8UNjJaiE3lQ0z0sN5XCucGbDdpFA==

Algorithm: sha256
Benchmark run time (seconds): 4.49
Iterations: 231123
End user calcuted time for iterations (microseconds): 505635
Hex Digest: e022878f5ee557b63e75bc94d57b4534da7b9b48a5404a41f82012401d86894f
Base64 Digest: 4CKHj17lV7Y+dbyU1XtFNNp7m0ilQEpB+CASQB2GiU8=

Algorithm: sha384
Benchmark run time (seconds): 1.65
Iterations: 227277
End user calcuted time for iterations (microseconds): 505260
Hex Digest: 68fd320c11ec42c61f50c8bdf3c4b1d1b07d97e2d247f8d85aa75f4b4c80e9c8aa1c36f5ee0ac714d24c0d64899ba479
Base64 Digest: aP0yDBHsQsYfUMi988Sx0bB9l+LSR/jYWqdfS0yA6ciqHDb17grHFNJMDWSJm6R5

Algorithm: sha512
Benchmark run time (seconds): 1.66
Iterations: 206657
End user calcuted time for iterations (microseconds): 505808
Hex Digest: d295741215b7fb6a3228414686a5b851827f519724cd6aea6d812bf96b421e7839404c8ef74ab36afda87ec6396cc6217a4cb19995e5a92f581e3aeb1d81d3b5
Base64 Digest: 0pV0EhW3+2oyKEFGhqW4UYJ/UZckzWrqbYEr+WtCHng5QEyO90qzav2ofsY5bMYhekyxmZXlqS9YHjrrHYHTtQ==

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
