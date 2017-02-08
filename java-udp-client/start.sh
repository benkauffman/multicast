#!/usr/bin/env bash

./gradlew clean build jar

for f in build/libs/*.jar;
    do java -jar  $f;
done
