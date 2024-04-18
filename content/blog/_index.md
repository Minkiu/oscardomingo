+++
title = "Blog"

description = "Blog posts authored by Oscar Domingo"

# Used to sort pages by "date", "update_date", "title", "title_bytes", "weight", "slug" or "none". See below for more information.
sort_by = "date"

# Template to use to render this section page.
template = "blog.html"

# The given template is applied to ALL pages below the section, recursively.
# If you have several nested sections, each with a page_template set, the page
# will always use the closest to itself.
# However, a page's own `template` variable will always have priority.
# Not set by default.
page_template ="blog-page.html"

# This sets the number of pages to be displayed per paginated page.
# No pagination will happen if this isn't set or if the value is 0.
paginate_by = 10

# If set, this will be the path used by the paginated page. The page number will be appended after this path.
# The default is page/1.
paginate_path = "posts"

# If set to "true", the section pages will be in the search index. This is only used if
# `build_search_index` is set to "true" in the Zola configuration file.
in_search_index = true

# If set to "true", a feed file will be generated for this section at the
# section's root path. This is independent of the site-wide variable of the same
# name. The section feed will only include posts from that respective feed, and
# not from any other sections, including sub-sections under that section.
generate_feed = true

# Your own data.
[extra]
+++
