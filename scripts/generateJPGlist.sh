# this shell commad is used to create a complte JPG files' list under one kind of fonts' root path
find $* -name "*.jpg" | grep -v invalid > $*/JPG_list.txt
