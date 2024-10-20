#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2018-2022 Sunaina Pai
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""Make static website/blog with Python."""


import os
import shutil
import re
import glob
import sys
import json
import datetime


def fread(filename):
    """Read file and close the file."""
    with open(filename, 'r') as f:
        return f.read()


def fwrite(filename, text):
    """Write content to file and close the file."""
    basedir = os.path.dirname(filename)
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    with open(filename, 'w') as f:
        f.write(text)


def log(msg, *args):
    """Log message with specified arguments."""
    sys.stderr.write(msg.format(*args) + '\n')


def truncate(text, words=50):
    """Remove tags and truncate text to the specified number of words."""
    return ' '.join(re.sub('(?s)<.*?>', ' ', text).split()[:words])


def read_headers(text):
    """Parse headers in text and yield (key, value, end-index) tuples."""
    for match in re.finditer(r'\s*<!--\s*(.+?)\s*:\s*(.+?)\s*-->\s*|.+', text):
        if not match.group(1):
            break
        yield match.group(1), match.group(2), match.end()


def rfc_2822_format(date_str):
    """Convert yyyy-mm-dd date string to RFC 2822 format date string."""
    d = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return d.strftime('%a, %d %b %Y %H:%M:%S +0000')
    
def rfc_3339_format(date_str):
    """Convert yyyy-mm-dd date string to RFC 3339 format date string."""
    d = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return d.isoformat()+'Z'


def read_content(filename):
    """Read content and metadata from file into a dictionary."""
    # Read file content.
    text = fread(filename)

    # Read metadata and save it in a dictionary.
    date_slug = os.path.basename(filename).split('.')[0]
    match = re.search(r'^(?:(\d\d\d\d-\d\d-\d\d)-)?(.+)$', date_slug)
    content = {
        'date': match.group(1) or '1970-01-01',
        'slug': match.group(2),
    }

    # Read headers.
    end = 0
    for key, val, end in read_headers(text):
        content[key] = val

    # Separate content from headers.
    text = text[end:]

    # Convert Markdown content to HTML.
    if filename.endswith(('.md', '.mkd', '.mkdn', '.mdown', '.markdown')):
        try:
            if _test == 'ImportError':
                raise ImportError('Error forced by test')
            import commonmark
            text = commonmark.commonmark(text)
        except ImportError as e:
            log('WARNING: Cannot render Markdown in {}: {}', filename, str(e))

    # Update the dictionary with content and RFC 2822 date.
    content.update({
        'content': text,
        'rfc_2822_date': rfc_2822_format(content['date']),
        'rfc_3339_date': rfc_3339_format(content['date'])
    })

    return content


def render(template, **params):
    """Replace placeholders in template with values from params."""
    return re.sub(r'{{\s*([^}\s]+)\s*}}',
                  lambda match: str(params.get(match.group(1), match.group(0))),
                  template)


def make_pages(src, dst, layout, **params):
    """Generate pages from page content."""
    items = []

    for src_path in glob.glob(src):
        content = read_content(src_path)

        page_params = dict(params, **content)
        
        # Populate placeholders in content if content-rendering is enabled.
        if page_params.get('render') == 'yes':
            rendered_content = render(page_params['content'], **page_params)
            page_params['content'] = rendered_content
            content['content'] = rendered_content

        items.append(content)

        dst_path = render(dst, **page_params)
        output = render(layout, **page_params)

        log('Rendering {} => {} ...', src_path, dst_path)
        fwrite(dst_path, output)

    return sorted(items, key=lambda x: x['date'], reverse=True)

def make_collection(src, **params):
	"""Generate a collection of objects from content in a list of files."""
	items = []
	
	for src_path in glob.glob(src):
		content = read_content(src_path)
		
		page_params = dict(params, **content)
		
		# Populate placeholders in content if content-rendering is enabled.
		if page_params.get('render') == 'yes':
			rendered_content = render(page_params['content'], **page_params)
			page_params['content'] = rendered_content
			content['content'] = rendered_content
		
		items.append(content)
	
	return sorted(items, key=lambda x: x['date'], reverse=True)

def make_list(posts, dst, list_layout, item_layout, **params):
    """Generate list page for a blog."""
    items = []
    for post in posts:
        item_params = dict(params, **post)
        if 'summary' in post:
            item_params['summary'] = post['summary']
        else:
            item_params['summary'] = truncate(post['content'])
        item_params['full_content'] = post['content']
        item = render(item_layout, **item_params)
        items.append(item)

    params['content'] = ''.join(items)
    dst_path = render(dst, **params)
    output = render(list_layout, **params)

    log('Rendering list => {} ...', dst_path)
    fwrite(dst_path, output)

def get_latest_post_path():
    posts_dir = 'content/posts/*.html'
    sorted_post_paths = sorted(glob.glob(posts_dir), reverse=True)
    return sorted_post_paths[0]

def get_latest_post_date_rfc_3339():
    latest_post_path = get_latest_post_path()
    content = read_content(latest_post_path)
    latest_post_date = render('{{ date }}', **content)
    return rfc_3339_format(latest_post_date)

def make_latest_post_blurb(**params):
    latest_post_path = get_latest_post_path()
    content = read_content(latest_post_path)
    page_params = dict(params, **content)
    blurb_format = '<a href="/posts/{{ slug }}">{{ title }}</a>. Published on {{ date }}. {{ summary }}'
    rendered_blurb = render(blurb_format, **page_params)
    return rendered_blurb

def main():
    # Clear out the old contents of the _site directory, leaving the git info unchanged.
    if os.path.isdir('_site'):
        fileList = os.listdir('_site')
        for fileName in fileList:
            if '.git' not in fileName and os.path.isdir('_site/' + fileName):
                shutil.rmtree('_site/' + fileName)
            elif '.git' not in fileName:
                os.remove('_site/' + fileName)
    # Copy in static content to the _site directory
    shutil.copytree('static', '_site', dirs_exist_ok=True)

    # Default parameters.
    params = {
        'base_path': '',
        'subtitle': 'Emma Juettner',
        'author': 'Emma Juettner',
        'site_url': 'https://emmajuettner.com',
        'current_year': datetime.datetime.now().year,
        'current_month': datetime.datetime.now().strftime('%B'),
        'current_day': datetime.datetime.now().day
    }

    # If params.json exists, load it.
    if os.path.isfile('params.json'):
        params.update(json.loads(fread('params.json')))

    # Find the latest post and generate a blurb for it
    params['latest_post_blurb'] = make_latest_post_blurb(**params)
    
    # Find the latest post and save the date for the feeds
    params['latest_post_date'] = get_latest_post_date_rfc_3339()

    # Load layouts.
    # Main blog
    page_layout = fread('layout/page.html')
    post_layout = fread('layout/post.html')
    list_layout = fread('layout/list.html')
    item_layout = fread('layout/item.html')
    rss_xml = fread('layout/rss.xml')
    atom_xml = fread('layout/atom.xml')
    rss_item_xml = fread('layout/rss_item.xml')
    atom_item_xml = fread('layout/atom_item.xml')
    # Short stories
    short_story_page_layout = fread('layout/short-story-recommendations.html')
    short_story_item_layout = fread('layout/story_item.html')
    stories_rss_xml = fread('layout/stories_rss.xml')
    stories_rss_item_xml = fread('layout/stories_rss_item.xml')
    # Tech stories
    tech_story_page_layout = fread('layout/tech-stories.html')
    tech_story_item_layout = fread('layout/story_item.html')
    tech_stories_rss_xml = fread('layout/tech_stories_rss.xml')
    tech_stories_rss_item_xml = fread('layout/stories_rss_item.xml')
	
    # Combine layouts to form final layouts.
    post_layout = render(page_layout, content=post_layout)
    list_layout = render(page_layout, content=list_layout)
    short_story_layout = render(page_layout, content=short_story_page_layout)
    tech_story_layout = render(page_layout, content=tech_story_page_layout)

    # Create site pages.
    make_pages('content/_index.html', '_site/index.html',
               page_layout, **params)
    make_pages('content/_404.html', '_site/404.html',
               page_layout, **params)
    make_pages('content/[!_]*.html', '_site/{{ slug }}/index.html',
               page_layout, **params)
    
    # Create short story recommendations page.
    short_story_recommendations = make_collection('content/short-story-recommendations/*.txt', **params)
    make_list(short_story_recommendations, '_site/short-story-recommendations/index.html',
    		  short_story_layout, short_story_item_layout, title='Short Story Recommendations', **params)
    
    # Create short stories RSS feed.
    make_list(short_story_recommendations, '_site/feed/short-story-recommendations-rss.xml',
    		  stories_rss_xml, stories_rss_item_xml, blog='short-story-recommendations', 
    		  title='Short Story Recommendations', **params)
    
    # Create tech story recommendations page.
    tech_story_recommendations = make_collection('content/tech-stories/*.txt', **params)
    make_list(tech_story_recommendations, '_site/tech-stories/index.html',
    		  tech_story_layout, tech_story_item_layout, title='Tech Stories', **params)
    
    # Create tech stories RSS feed.
    make_list(tech_story_recommendations, '_site/feed/tech-stories-rss.xml',
    		  tech_stories_rss_xml, stories_rss_item_xml, blog='tech-stories', 
    		  title='Tech Stories', **params)

    # Create blogs.
    blog_posts = make_pages('content/posts/*.html',
                            '_site/posts/{{ slug }}/index.html',
                            post_layout, blog='posts', **params)
    
    # Create blog list pages.
    make_list(blog_posts, '_site/posts/index.html',
              list_layout, item_layout, blog='posts', title='Posts', **params)

    # Create RSS feed.
    make_list(blog_posts, '_site/feed/rss.xml',
              rss_xml, rss_item_xml, blog='posts', title='Posts', **params)
              
    # Create Atom feed.
    make_list(blog_posts, '_site/feed/atom.xml',
              atom_xml, atom_item_xml, blog='posts', title='Posts', **params)

# Test parameter to be set temporarily by unit tests.
_test = None


if __name__ == '__main__':
    main()
