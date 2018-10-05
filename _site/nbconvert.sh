# capture input passed to bash script
FILE="$1"

# extract filename and attach date prefix
FILENAME=`basename $FILE .ipynb`
NEW_FILENAME=`date "+%Y-%m-%d-"`${FILENAME}

# construct markdown filename and dirname included images
POST_NAME="${FILENAME}.md"
IMG_DIR="${FILENAME}_files"
 
# call nbconvert
jupyter nbconvert --to markdown $FILE --output-dir ~/git/blog/_posts --output $NEW_FILENAME