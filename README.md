# Purpose


The purpose of this little project is to show how easy it is to generate many iterations of hashes.  It is also proving a point that if you're say doing "thousands" of iterations of rehashing a password (as I've heard a few times in PR blog posts for companies who get compromised) with a salt it simply is not enough.  And if you're not using hashing or using hashing without a salt that's just plain irresponsible.  If you catch someone doing that you should email [Plain Text Offenders][1] to disclose this bad practice.  If you want to learn more about password hashing in applications I recommend reading this [Crack Station article][2].

That being said here I'll show you some simple benchmarks as well as make a proposal for a better password hashing system which will dynamically evolve over time as websites are upgraded over time.

# Simple benchmarks

These benchmarks are the output of the `pword_hash_benchmark.py` script.

```
Algorithm: md5
Benchmark run time (seconds): 4.07
Iterations: 427237
End user calcuted time for iterations (microseconds): 503287
Hex Digest: 49f5a9ea663cc188befdb629a101342c
Base64 Digest: SfWp6mY8wYi+/bYpoQE0LA==
AES Encrypted Base64 Digest: Ytht5Njgz5vJ0m9feiG7Ml7KK87bU9n2fKRbMelEThs=
AES Decrypted Base64 Digest: SfWp6mY8wYi+/bYpoQE0LA==

Algorithm: sha1
Benchmark run time (seconds): 5.06
Iterations: 397563
End user calcuted time for iterations (microseconds): 502847
Hex Digest: 31ce5993abcc72fdad00f7e9a32647e5457cb7fe
Base64 Digest: Mc5Zk6vMcv2tAPfpoyZH5UV8t/4=
AES Encrypted Base64 Digest: KCxuOEXk/p0AaUAb9XL7nsfHEIupYnpzCOgYi1bMheU=
AES Decrypted Base64 Digest: Mc5Zk6vMcv2tAPfpoyZH5UV8t/4=

Algorithm: sha224
Benchmark run time (seconds): 1.65
Iterations: 228805
End user calcuted time for iterations (microseconds): 502781
Hex Digest: b9e023977d9bed335090fc4bad1a900c6db3dfca3e18fb2b2e3b8cfc
Base64 Digest: ueAjl32b7TNQkPxLrRqQDG2z38o+GPsrLjuM/A==
AES Encrypted Base64 Digest: aXX2NXY2dCfX6KnGaJioLJ3DBOX+STLeTvYv6eo0swZlEOC8yEhtSBttvufv6zQMTYaL556alI1nQKzZMmW2WA==
AES Decrypted Base64 Digest: ueAjl32b7TNQkPxLrRqQDG2z38o+GPsrLjuM/A==

Algorithm: sha256
Benchmark run time (seconds): 1.67
Iterations: 223934
End user calcuted time for iterations (microseconds): 509683
Hex Digest: dd1cc4871d6251fd9ba95cce346b623941e3ca855a8099e36f0eb0d728614de0
Base64 Digest: 3RzEhx1iUf2bqVzONGtiOUHjyoVagJnjbw6w1yhhTeA=
AES Encrypted Base64 Digest: Oz5PfUwcmPXaRjAHgOkDlPtlPxVGfFV24gyqVZDWy3v88sXV7zvkhIZ5JY1g9PuBTYaL556alI1nQKzZMmW2WA==
AES Decrypted Base64 Digest: 3RzEhx1iUf2bqVzONGtiOUHjyoVagJnjbw6w1yhhTeA=

Algorithm: sha384
Benchmark run time (seconds): 2.68
Iterations: 226513
End user calcuted time for iterations (microseconds): 501515
Hex Digest: 6090e804a325fef6f687f999400a13f800147488bd31ebb99a3dfe68157ad07a903ee22f7fd5a80c397ea12e641421f6
Base64 Digest: YJDoBKMl/vb2h/mZQAoT+AAUdIi9Meu5mj3+aBV60HqQPuIvf9WoDDl+oS5kFCH2
AES Encrypted Base64 Digest: mMRNHCw5XjWi5Z9xkATv+5Zcb9vHWC32b6U317PslAtGDQgSfeKDN0DRwS+fOmaS1Kz6RssZUd2AuntEoxv24k2Gi+eempSNZ0Cs2TJltlhNhovnnpqUjWdArNkyZbZY
AES Decrypted Base64 Digest: YJDoBKMl/vb2h/mZQAoT+AAUdIi9Meu5mj3+aBV60HqQPuIvf9WoDDl+oS5kFCH2

Algorithm: sha512
Benchmark run time (seconds): 2.75
Iterations: 202731
End user calcuted time for iterations (microseconds): 505061
Hex Digest: 025520812d7a4f08b4d0e54787b8fd7e8ed25c8ae90780c58de3293635f8c52cda9051c93a342d1e739cd9cfd06b59608fd5a27e635a9af1dd47d02d623a8c35
Base64 Digest: AlUggS16Twi00OVHh7j9fo7SXIrpB4DFjeMpNjX4xSzakFHJOjQtHnOc2c/Qa1lgj9WifmNamvHdR9AtYjqMNQ==
AES Encrypted Base64 Digest: U+uqI8RJT1awLS2lYVEqDA7jJL8LxAmbF87lg87J90gSei0ntUHJLHw3isb/x4cASCpbUfKdKeOhDyrtgbwd+OZcTgOuA1abBLMjmO57If3D15db7G7rdP1ToOFTJcll
AES Decrypted Base64 Digest: AlUggS16Twi00OVHh7j9fo7SXIrpB4DFjeMpNjX4xSzakFHJOjQtHnOc2c/Qa1lgj9WifmNamvHdR9AtYjqMNQ==

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
