---
title: "How This Blog Is Now Ran by Modern GitHub Actions Thanks to AI"
author: nacho
layout: post
---
Publishing Jupyter notebooks as blog posts on this site used to be a tedious, multi-step manual process.  After not updating this blog for a while, I asked Claude (yes, an AI) to take a look at the old workflow and make it better.  It read through my janky bash script, understood the whole Jekyll setup, and built a replacement that honestly makes me wonder why I spent all those hours doing it by hand.  Here's the before and after.

<br>

## The Old Way: Death by a Thousand Manual Steps

The original workflow relied on a short bash script (`nbconvert.sh`) that did the bare minimum:

1. Run `jupyter nbconvert --to markdown` on a notebook
2. Use `sed` to rewrite image paths
3. Use `rsync` to move the image folder

Sounds simple enough, but in practice there were several pain points:

* **Hardcoded paths** - The script pointed to `~/git/blog/`, so it only worked on one machine with that exact directory structure.
* **macOS-only `sed`** - The `sed -i ''` syntax is a macOS-ism that breaks on Linux.
* **No front matter management** - You had to manually embed Jekyll front matter (`title`, `author`, `layout`) as a raw cell inside the notebook *before* converting. Forget it and you'd get a post with no title.
* **No batch processing** - One notebook at a time, every time.
* **No automation** - Every publish meant: convert, check the output, fix paths, move images, git add, git commit, git push. Manually. Every. Single. Time.

<br>

## The New Way: One Command (or Zero)

The new setup has two components:

### 1. `publish_notebook.py` - A smarter local script

A Python script that replaces the old bash script with proper handling of all the edge cases:

```bash
# Publish a single notebook
python publish_notebook.py original_posts/my_analysis.ipynb

# Publish with a specific date and title
python publish_notebook.py original_posts/my_analysis.ipynb --date 2026-02-07 --title "My Post"

# Batch-publish every notebook in the folder
python publish_notebook.py original_posts/

# Preview what would happen without changing anything
python publish_notebook.py original_posts/my_analysis.ipynb --dry-run
```

**What it handles automatically:**

| Concern | Old | New |
|---|---|---|
| Image path rewriting | `sed` with hardcoded paths | Regex with repo-relative paths |
| Front matter | Must be manually embedded in notebook | Auto-extracted from notebook or filename |
| Duplicate front matter | Not handled (could break) | Detected and stripped before adding clean version |
| Cross-platform | macOS only (`sed -i ''`) | Pure Python, works everywhere |
| Batch mode | No | Yes, pass a directory |
| Dry run | No | `--dry-run` flag |
| Date control | Always today's date | `--date` flag or defaults to today |

### 2. GitHub Actions Workflow - Zero-touch publishing

The real quality-of-life improvement is a GitHub Actions workflow (`.github/workflows/publish-notebooks.yml`) that makes the whole thing **hands-free**:

* **Push trigger**: Drop a `.ipynb` file into `original_posts/`, push to `master`, and the workflow automatically converts it to a blog post and commits the result. That's it. Done.
* **Manual trigger**: Go to the Actions tab on GitHub, click "Run workflow", optionally specify a notebook name and date. Useful for re-publishing or backdating posts.

The workflow installs Python and `nbconvert`, detects which notebooks changed in the push, runs `publish_notebook.py` on each one, and commits the generated markdown + images back to the repo.  GitHub Pages picks up the new commit and the blog updates itself.

<br>

## The New Publishing Workflow

Here's what publishing a new post looks like now:

1. Write a Jupyter notebook as usual
2. Save it to `original_posts/`
3. `git add`, `git commit`, `git push`
4. There is no step 4. The blog post publishes itself.

Or if you prefer local control:

1. Write a Jupyter notebook
2. Run `python publish_notebook.py original_posts/my_notebook.ipynb`
3. Review the generated post in `docs/_posts/`
4. Commit and push everything

Either way, no more fighting with `sed`, no more forgetting front matter, no more copying image folders around by hand.

<br>

## Closing Thoughts

The friction of the old process was honestly the main reason this blog went quiet for so long.  Removing that friction won't magically generate content, but it removes the excuse.  Now the only hard part is the writing itself - which is how it should be.

Oh, and this very post?  It was written as a Jupyter notebook, dropped into `original_posts/`, and published automatically by the pipeline it describes.  The AI built the tool, then the tool published the story about the AI building the tool.  We're through the looking glass here.

If you have a similar Jekyll + Jupyter setup and want to steal this approach, the full script and workflow are in the [repo](https://github.com/ncho-sqd/ncho-sqd.github.io).  Happy publishing.
