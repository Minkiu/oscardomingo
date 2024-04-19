+++
title = "Hello World"
date = 2024-04-18
+++

This might be the third or fourth attempt at kickstarting a blog, I intend to make this one stick by participating in [100 Days To Offload](https://100daystooffload.com).

## Mynt

The previous iteration of this site was generated using [mynt](https://github.com/uhnomoli/mynt) a Python static site generator, but I did not really follow through on writing, and after trying to publish again, experienced some paper cuts trying to get it to generate my site (syntax highlighting stopped working, for example), went through a couple of weeks of overthinking to update `mynt`, forking it or developing a whole new static site generator in Python in the spirit of `mynt`; long story short, I procrastinated on writing, whether if I end up doing any of these remains to be seen, but goes without saying it's not a problem that I am particularly interested in solving [and it's pretty much solved](https://jamstack.org/generators/).

## Zola

Enter [zola](https://www.getzola.org), version 18 at the time of this writing, is a Rust powered static site generator, which I can vendor the binary in the project itself, which should make it more portable and durable.

The structure is not that different from what I had with `mynt` so transition has been quite easy, mostly reshuffling things around, so quite happy with that. Previous site used to have a "projects" section, with only two projects, which can be seen on my GitHub anyway, so decided to remove it, the other thing I am not adding in the first iteration are tags.

## Onwards

I am not sure what to write really, I will keep the blog as open ended topic, but most likely will fall in the technology realm, I have some stuff written already, so will start by polishing those and publishing it.
