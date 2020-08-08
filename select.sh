#!/bin/bash

################
# Select lables and images from ./labels and ./images
# Save to ./selected/labels and ./selected/images (both directories must be present)
# Translate class numbers while copying labels
################

class_name="$1"

if [ "$class_name" == "" ]; then
  echo "Usage: $0 \"class_name\""
  exit
fi

class=$(grep -n "$class_name" labels/classes.txt | cut -f1 -d:)
class=$((class - 1))

echo "Class number: " $class

if [ "$class" == "" ]; then
  echo $class_name not found
  exit
fi

class_path="selected/labels/classes.txt"
if [ ! -f $class_path ]; then
  new_class_number=0
else
  new_class_number=$(wc -l selected/labels/classes.txt | awk '{print $1;}')
fi
new_class_number=$((new_class_number + 1))
echo "New class number: " $new_class_number

read -p "Do you wish to continue? (y/n)" yn

if [ "$yn" != "y" ]; then
  exit
fi

echo $class_name >> $class_path

IFS=$'\n'
cd labels
for f in $(grep -E "^$class " -l *.txt); do
  a="${f%.txt}"
  n=$(ls ../images/$a.* 2>/dev/null | wc -l)
  if [ "$n" == "0" ]; then
    echo $f has not image
    exit
  fi
  if [ $n -gt 1 ]; then
    echo $f has multiple images
    exit
  fi
done

for f in $(grep -E "^$class " -l *.txt); do
  a="${f%.txt}"
  grep -E "^$class " $f | sed "s/^$class /$new_class_number /" >> ../selected/labels/"$f"
  /bin/cp -f ../images/$a.* ../selected/images/
done
