for file in *.txt; do
    echo $file
    iconv -f GBK -t utf-8 "$file" -o "utf/${file%.txt}.txt"
done
