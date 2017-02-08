#!/bin/bash
cd "$(dirname "$0")"

./gradlew clean build jar

for f in build/libs/*.jar;
    do java -jar  $f;
done
