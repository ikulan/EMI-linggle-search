#!/bin/bash

# 設定根目錄
ROOT_DIR="/home/nlplab/atwolin/EMI-repo/yale-ocw"
RESULT_DIR="/home/nlplab/atwolin/EMI-repo/"
OUTPUT_FOLDER_NAME="yale-ocw-nc-pos"

if [ ! -d "$RESULT_DIR/$OUTPUT_FOLDER_NAME" ]; then
  mkdir "$RESULT_DIR/$OUTPUT_FOLDER_NAME"
  echo "Created directory: $RESULT_DIR/$OUTPUT_FOLDER_NAME"
else
  echo "Directory already exists: $RESULT_DIR/$OUTPUT_FOLDER_NAME"
fi

# 移動到目標目錄
cd "$ROOT_DIR" || exit

# 遍歷目標目錄中的所有文件夾
for DEPT_NAME in */; do
  # 去掉文件夾名稱後面的斜杠
  DEPT_NAME=${DEPT_NAME%/}

  # 移動到每個文件夾
  cd "$DEPT_NAME" || continue
  if [ ! -d "$RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME" ]; then
      mkdir "$RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME"
      echo "Created directory: $RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME"
    else
      echo "Directory already exists: $RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME"
    fi
  # 遍歷該文件夾中的所有課程文件夾
  for COURSE_NAME in */; do
    # 去掉課程文件夾名稱後面的斜杠
    COURSE_NAME=${COURSE_NAME%/}

    # 移動到每個課程文件夾
    cd "$COURSE_NAME" || continue
    if [ ! -d "$RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME/$COURSE_NAME" ]; then
      mkdir "$RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME/$COURSE_NAME"
      echo "Created directory: $RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME/$COURSE_NAME"
    else
      echo "Directory already exists: $RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME/$COURSE_NAME"
    fi
    # 遍歷該課程文件夾中的所有講座文件
    for LECTURE_FILE in *.txt; do
      echo "LECTURE_FILE: $LECTURE_FILE"
      # 檢查文件是否存在
      if [ -f "$LECTURE_FILE" ]; then
        # 組合完整路徑
        FILE_PATH="$ROOT_DIR/$DEPT_NAME/$COURSE_NAME/$LECTURE_FILE"
        echo "FILE_PATH: $FILE_PATH"
        OUTPUT_FILE_PATH="$RESULT_DIR/$OUTPUT_FOLDER_NAME/$DEPT_NAME/$COURSE_NAME/${LECTURE_FILE%.txt}_pos.txt"
        echo "OUTPUT_FILE_PATH: $OUTPUT_FILE_PATH"
        # 執行命令
        # python /home/nlplab/atwolin/Linggle-EMI/nc_map.py "$FILE_PATH" | sort -k 1,1 -t $'\t' | python /home/nlplab/atwolin/Linggle-EMI/nc_reduce.py > $OUTPUT_FILE_PATH
        python /home/nlplab/atwolin/EMI-repo/linggle-core/linggle/ngram/ngram_count.py < "$FILE_PATH" > $OUTPUT_FILE_PATH
        # echo "Processed $FILE_PATH"
      fi
    done

    # 回到上一級目錄
    cd ..
  done

  # 回到根目錄
  cd ..
done
