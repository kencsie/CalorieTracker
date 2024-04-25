find ../data/input/food_dataset -name "*_rgb.jpg" -exec cp {} ../data/input/images \;
rm ../data/input/images/full_size_rgb.jpg
find ../data/input/images -type f | wc -l