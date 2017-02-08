#!/bin/bash
cd "$(dirname "$0")"

# ifconfig lo0
# route add -net 224.0.0.3/32 -interface lo0

./gradlew clean build jar

for f in build/libs/*.jar;
    do java -jar  $f;
done

# route delete 224.0.0.3/32