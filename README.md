# Purpose


The purpose of this little project is to show how easy it is to generate many iterations of hashes.  It is also proving a point that if you're say doing "thousands" of iterations of rehashing a password (as I've heard a few times in PR blog posts for companies who get compromised) with a salt it simply is not enough.  And if you're not using hashing or using hashing without a salt that's just plain irresponsible.  If you catch someone doing that you should email [Plain Text Offenders][1] to disclose this bad practice.  If you want to learn more about password hashing in applications I recommend reading this [Crack Station article][2].

That being said here I'll show you some simple benchmarks as well as make a proposal for a better password hashing system which will dynamically evolve over time as websites are upgraded over time.

# Simple benchmarks

Please understand that these benchmarks are indeed simple.  It calculates the time every other hash iteration so in practice slightly more hashes per second are possible without calculating the time.

```
Algorithm: md5
Run time (microseconds): 500000
Iterations: 180850
Hex Digest: 92dc5e5fe54f2caee528f04e2010e625
Base64 Digest: ktxeX+VPLK7lKPBOIBDmJQ==

Algorithm: sha1
Run time (microseconds): 500004
Iterations: 173812
Hex Digest: ba8feb69fa02c9e98ae68dc5bf0e1c6e4f2b95a2
Base64 Digest: uo/rafoCyemK5o3Fvw4cbk8rlaI=

Algorithm: sha224
Run time (microseconds): 500000
Iterations: 130622
Hex Digest: eb7b1d0b9bef805c57bf1460009a1047805fabb18cb003397708c49d
Base64 Digest: 63sdC5vvgFxXvxRgAJoQR4Bfq7GMsAM5dwjEnQ==

Algorithm: sha256
Run time (microseconds): 500004
Iterations: 129020
Hex Digest: ada8c7a66a8b43689d8ab41bc51ef0428087bd9368466b71a5464edbc0ce7474
Base64 Digest: rajHpmqLQ2idirQbxR7wQoCHvZNoRmtxpUZO28DOdHQ=

Algorithm: sha384
Run time (microseconds): 500005
Iterations: 126532
Hex Digest: a57013b87993679fc92a27522a26fe09b378be68488c124ee7f55757a897c306aa1f7d3f339711d627a5f399a263ee4b
Base64 Digest: pXATuHmTZ5/JKidSKib+CbN4vmhIjBJO5/VXV6iXwwaqH30/M5cR1iel85miY+5L

Algorithm: sha512
Run time (microseconds): 500097
Iterations: 118988
Hex Digest: e77285174dfa3aba639ae456038c329542b2d7741f84918b0d04fdc5ab2426ac7e66ad38c56498a914e7818118b09cc62d071fca9cf40ec0a79f4cb37611a6e5
Base64 Digest: 53KFF036OrpjmuRWA4wylUKy13QfhJGLDQT9xaskJqx+Zq04xWSYqRTngYEYsJzGLQcfypz0DsCnn0yzdhGm5Q==

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

So I propose doing the following.  When your application first starts up it runs a quick benchmark on the number of password hash iterations it can perform in say `500ms` (or some arbitrary time you're willing to wait for the hash to be computed on your hosted system).  This will be the estimated performance metric for the number of iterations the password should be hashed.  All new passwords will be

[1]: http://plaintextoffenders.com/
[2]: https://crackstation.net/hashing-security.htm
