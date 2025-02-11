#!/bin/bash

# To do pos tagging and ngram counting
# python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/process/pos_v2.py /home/nlplab/atwolin/EMI-linggle-search/vocab/data/cambridge/cambridge.examples.txt > /home/nlplab/atwolin/EMI-linggle-search/data/dictionaries/cambridge.examples.pos.txt
# python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/process/pos_v2.py /home/nlplab/atwolin/EMI-linggle-search/vocab/data/mw/mw.examples.txt > /home/nlplab/atwolin/EMI-linggle-search/data/dictionaries/mw.examples.pos.txt


# Ngram conut after check and delete if the target directory exists
# DIR="/home/nlplab/atwolin/EMI-linggle-search/data/nc-out-cambridge"
# if [ -d "$DIR" ]; then
#   echo "Directory $DIR exists. Deleting..."
#   rm -r "$DIR"
#   echo "Directory $DIR has been deleted."
# else
#   echo "Directory $DIR does not exist."
# fi
# cat /home/nlplab/atwolin/EMI-linggle-search/data/dictionaries/cambridge.examples.pos.txt /home/nlplab/atwolin/EMI-linggle-search/data/dictionaries/mw.examples.pos.txt | lmr 5m 16 'python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/process/ngramcount_map.py' 'python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/process/ngramcount_reduce.py' /home/nlplab/atwolin/EMI-linggle-search/data/nc-out-dict


# Do linngle format ngram conut after check and delete if the target directory exists
DIR="/home/nlplab/atwolin/EMI-linggle-search/data/linggle-nc-out-dict"
if [ -d "$DIR" ]; then
  echo "Directory $DIR exists. Deleting..."
  rm -r "$DIR"
  echo "Directory $DIR has been deleted."
else
  echo "Directory $DIR does not exist."
fi

# Merge the ngram counting result and transfer the format of ngram counting result
cat /home/nlplab/atwolin/EMI-linggle-search/data/nc-out-dict/* | lmr 16m 5 'python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/process/linggle_map.py' 'python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/process/linggle_reduce.py' /home/nlplab/atwolin/EMI-linggle-search/data/linggle-nc-out-dict


DB="/home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/database/dictionary.db"
if [ -f "$DB" ]; then
  echo "Database file $DB exists. Deleting..."
  rm "$DB"
  echo "Database file $DB has been deleted."
else
  echo "Database file $DB does not exist."
fi
# Store the ngram counting result in the database
python /home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/database/emi_linggle_sqlite.py /home/nlplab/atwolin/EMI-linggle-search/data/linggle-nc-out-dict/*
