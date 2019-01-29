---
title: Jupyter Notebook driven blog post
author: nacho
date: 2019-01-29
layout: post
---
Jupyter notebook is a great tool for data science, and with effective use of `nbconvert` it's also great for blogging static pages such as by using [Jekyll](https://github.com/jekyll/jekyll).

[`nbconvert`](https://github.com/jupyter/nbconvert), under [Project Jupyter](https://jupyter.org/documentation), allows you to easily convert `.ipynb` notebook files to various static formats such as markdown, HTML, PDF, LaTeX etc...

For example, to convert a Jupyter notebook to markdown, it's as simple as:
```bash
jupyter nbconvert --to markdown PATH_TO_YOURFILE.ipynb
```

This saves a converted **markdown file** and a **folder** named after the original notebook with a "_files" suffix that collects images etc.. included in the notebook.  All plots (e.g. matplotlib) embedded in the notebook get automatically saved as separate `.png` images and automatically linked in the markdown file generated.

In order to further leverage `nbconvert` for clean and fairly automated markdown generation which can then be directly used as a blog post right away, I need to add on some additional flags and features:

1. **`--no-input`**: Suppress print out of all code-blocks.
2. **`--output-dir`**:  Specify directory to save markdown and "_files" folder.
3. **`--output`**:  Name of markdown file to be saved in `--output-dir`
4. Move the "_files" folder to an appropriate location for compatibility with Jekyll (since Jekyll seems unable to render images saved in the same directory as where markdown is saved) using `rsync` and edit markdown using `sed`.

Below is a simple bash script that puts all of the above together:
```bash
#!/bin/bash

# capture input passed to bash script
FILE="$1"

# extract filename and attach date prefix
FILENAME=`basename $FILE .ipynb`
NEW_FILENAME=`date "+%Y-%m-%d-"`${FILENAME}

# construct markdown filename and dirname including images
POST_NAME="${NEW_FILENAME}.md"
IMG_DIR="${NEW_FILENAME}_files"
 
# call nbconvert
jupyter nbconvert --to markdown $FILE --output-dir ~/git/blog/_posts --output $NEW_FILENAME --no-input

# rename image files in markdown to moved /images folder (to be moved)
for fp in ~/git/blog/_posts/$IMG_DIR/*; do
    FN=$IMG_DIR/`basename $fp`;
    # change image path and center image
    sed -i '' "s#($FN)#(/images/$FN){: .center-image }#g" ~/git/blog/_posts/$POST_NAME;
done

# move image folder automatically created under _post to /image folder
rsync -a ~/git/blog/_posts/${IMG_DIR} ~/git/blog/images
rm -rf ~/git/blog/_posts/${IMG_DIR}
```

I save this script as [`nbconvert.sh`](https://github.com/ncho-sqd/ncho-sqd.github.io/blob/master/nbconvert.sh) and use:

```bash
bash nbconvert.sh PATH_TO_YOURFILE.ipynb
```

This automatically saves a converted markdown file to `~/git/blog/_posts` and the embedded image files to `~git/blog/images`.  This markdown file can then directly be use as a Jekyll blog post with all the right links to the image/embedded files automatically in place.