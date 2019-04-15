#!/bin/bash

# capture input passed to bash script
FILE="$1"

# extract filename and attach date prefix
FILENAME=`basename $FILE .ipynb`
NEW_FILENAME=`date "+%Y-%m-%d-"`${FILENAME}

# construct markdown filename and dirname included images
POST_NAME="${NEW_FILENAME}.md"
IMG_DIR="${NEW_FILENAME}_files"
 
# call nbconvert
jupyter nbconvert --to markdown $FILE --output-dir ~/git/blog/docs/_posts --output $NEW_FILENAME --no-input

# rename image files in markdown to moved /images folder (to be moved)
for fp in ~/git/blog/docs/_posts/$IMG_DIR/*; do
    FN=$IMG_DIR/`basename $fp`;
    # change image path and center image
    sed -i '' "s#($FN)#(/images/$FN){: .center-image }#g" ~/git/blog/docs/_posts/$POST_NAME;
done

# move image folder automatically created under _post to /image folder
rsync -a ~/git/blog/docs/_posts/${IMG_DIR} ~/git/blog/images
rm -rf ~/git/blog/docs/_posts/${IMG_DIR}
