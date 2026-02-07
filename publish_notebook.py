#!/usr/bin/env python3
"""
Publish Jupyter notebooks as Jekyll blog posts.

Converts .ipynb files to Markdown with proper front matter,
fixes image paths, and moves images to the right location.

Usage:
    # Publish a single notebook (uses today's date)
    python publish_notebook.py original_posts/my_analysis.ipynb

    # Publish with a specific date
    python publish_notebook.py original_posts/my_analysis.ipynb --date 2026-02-07

    # Publish with a custom title
    python publish_notebook.py original_posts/my_analysis.ipynb --title "My Custom Title"

    # Publish all notebooks in a directory
    python publish_notebook.py original_posts/

    # Dry run (preview what would happen)
    python publish_notebook.py original_posts/my_analysis.ipynb --dry-run
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
POSTS_DIR = REPO_ROOT / "docs" / "_posts"
IMAGES_DIR = REPO_ROOT / "images"
DEFAULT_AUTHOR = "nacho"
DEFAULT_LAYOUT = "post"


def notebook_title_from_filename(filename: str) -> str:
    """Derive a human-readable title from a notebook filename."""
    name = filename.replace("_", " ").replace("-", " ")
    return name.title()


def extract_title_from_notebook(nb_path: Path) -> str | None:
    """Try to extract a title from the notebook's front matter or first heading."""
    try:
        import json
        import yaml

        with open(nb_path) as f:
            nb = json.load(f)
        for cell in nb.get("cells", []):
            source = "".join(cell.get("source", []))
            # Check raw cells for YAML front matter (common pattern)
            if cell.get("cell_type") == "raw":
                match = re.match(r'^---\s*\n(.+?)\n---', source, re.DOTALL)
                if match:
                    try:
                        fm = yaml.safe_load(match.group(1))
                        if isinstance(fm, dict) and "title" in fm:
                            return fm["title"]
                    except Exception:
                        # Fall back to regex if yaml isn't available
                        title_match = re.search(r'title:\s*(.+)', match.group(1))
                        if title_match:
                            return title_match.group(1).strip().strip('"\'')
            # Check markdown cells for H1 headings
            if cell.get("cell_type") == "markdown":
                for line in cell.get("source", []):
                    line = line.strip()
                    if line.startswith("# "):
                        return line.lstrip("# ").strip()
        return None
    except Exception:
        return None


def build_front_matter(title: str, author: str = DEFAULT_AUTHOR,
                       layout: str = DEFAULT_LAYOUT) -> str:
    """Build Jekyll YAML front matter."""
    return f"""---
title: "{title}"
author: {author}
layout: {layout}
---
"""


def convert_notebook(nb_path: Path, pub_date: date | None = None,
                     title: str | None = None, author: str = DEFAULT_AUTHOR,
                     no_input: bool = True, dry_run: bool = False) -> Path | None:
    """
    Convert a Jupyter notebook to a Jekyll-ready markdown post.

    Returns the path to the generated post, or None on failure.
    """
    nb_path = nb_path.resolve()
    if not nb_path.exists():
        print(f"Error: {nb_path} does not exist")
        return None
    if nb_path.suffix != ".ipynb":
        print(f"Error: {nb_path} is not a .ipynb file")
        return None

    stem = nb_path.stem
    pub_date = pub_date or date.today()
    date_prefix = pub_date.strftime("%Y-%m-%d")
    post_stem = f"{date_prefix}-{stem}"
    post_filename = f"{post_stem}.md"
    img_dir_name = f"{post_stem}_files"

    # Resolve title
    if not title:
        title = extract_title_from_notebook(nb_path) or notebook_title_from_filename(stem)

    if dry_run:
        print(f"[DRY RUN] Would convert: {nb_path.name}")
        print(f"  -> Post:   docs/_posts/{post_filename}")
        print(f"  -> Images: images/{img_dir_name}/")
        print(f"  -> Title:  {title}")
        return POSTS_DIR / post_filename

    # Ensure output directories exist
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Run nbconvert
    cmd = [
        sys.executable, "-m", "nbconvert",
        "--to", "markdown",
        "--output-dir", str(POSTS_DIR),
        "--output", post_stem,
        str(nb_path),
    ]
    if no_input:
        cmd.append("--no-input")

    print(f"Converting {nb_path.name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running nbconvert:\n{result.stderr}")
        return None

    post_path = POSTS_DIR / post_filename
    if not post_path.exists():
        print(f"Error: expected output {post_path} was not created")
        return None

    # Read generated markdown
    content = post_path.read_text()

    # Fix image references: ![alt](post_stem_files/img.png) -> ![alt](/images/post_stem_files/img.png){: .center-image }
    # Handle both standard markdown images and any existing path formats
    img_pattern = re.compile(
        rf'!\[([^\]]*)\]\((?:\.\/)?({re.escape(img_dir_name)}/[^)]+)\)'
    )
    content = img_pattern.sub(
        rf'![\1](/images/\2){{: .center-image }}',
        content
    )

    # Strip any existing front matter (from raw cells in the notebook)
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, count=1, flags=re.DOTALL)

    # Add our front matter at the top
    front_matter = build_front_matter(title, author)
    content = front_matter + content

    # Write updated markdown
    post_path.write_text(content)
    print(f"  Post written: docs/_posts/{post_filename}")

    # Move image directory if it exists
    src_img_dir = POSTS_DIR / img_dir_name
    dst_img_dir = IMAGES_DIR / img_dir_name
    if src_img_dir.exists() and src_img_dir.is_dir():
        if dst_img_dir.exists():
            shutil.rmtree(dst_img_dir)
        shutil.move(str(src_img_dir), str(dst_img_dir))
        img_count = len(list(dst_img_dir.iterdir()))
        print(f"  Images moved: images/{img_dir_name}/ ({img_count} files)")
    else:
        print("  No images generated.")

    print(f"  Done: {nb_path.name} -> {post_filename}")
    return post_path


def main():
    parser = argparse.ArgumentParser(
        description="Publish Jupyter notebooks as Jekyll blog posts."
    )
    parser.add_argument(
        "path",
        help="Path to a .ipynb file or a directory of notebooks",
    )
    parser.add_argument(
        "--date",
        type=lambda s: date.fromisoformat(s),
        default=None,
        help="Publication date (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Post title. Defaults to first H1 in notebook or filename.",
    )
    parser.add_argument(
        "--author",
        default=DEFAULT_AUTHOR,
        help=f"Post author (default: {DEFAULT_AUTHOR})",
    )
    parser.add_argument(
        "--include-input",
        action="store_true",
        help="Include code input cells in the output (excluded by default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without making changes",
    )
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_dir():
        notebooks = sorted(target.glob("*.ipynb"))
        if not notebooks:
            print(f"No .ipynb files found in {target}")
            sys.exit(1)
        print(f"Found {len(notebooks)} notebook(s) in {target}\n")
        results = []
        for nb in notebooks:
            result = convert_notebook(
                nb,
                pub_date=args.date,
                title=None,  # auto-detect per notebook
                author=args.author,
                no_input=not args.include_input,
                dry_run=args.dry_run,
            )
            results.append(result)
            print()
        success = sum(1 for r in results if r is not None)
        print(f"\n{success}/{len(notebooks)} notebooks published.")
    elif target.is_file():
        result = convert_notebook(
            target,
            pub_date=args.date,
            title=args.title,
            author=args.author,
            no_input=not args.include_input,
            dry_run=args.dry_run,
        )
        if result is None:
            sys.exit(1)
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
