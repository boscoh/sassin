
# Indented-SASS

_This is a fork of [`RapydCSS`](https://bitbucket.org/pyjeon/rapydcss), with a modified API to work with projects like HAMLPY._

Indented-SASS is a beautiful space-indented format designed to express CSS stylesheets. It is, in spirit and syntax, similar to  Stylus. The difference is that indented-SASS can be compiled to CSS entirely within the Python ecosystem.



## What is indented-SASS?

Okay this gets confusing: there is a Ruby program called SASS which used to compile an indented syntax for stylesheets into CSS. Let's call this the indented-SASS format. 

Indented-SASS used to be known as the SASS format, but SASS, the program, found that it was losing market share to LESS, and thus, introduced the SCSS format, which has a curly braced syntax to appear more like LESS. This lead to the situation where SASS preferably compiles SCSS, and can also compile deprecated SASS, but would rather not do so.

However, indented-SASS is a lovely format that fits well with other space-indented formats, such as YAML, HAML, and of course, Python. But it gets rather complicated if you want to use indented-SASS in Python. The good news is that there are a few Python SCSS libraries (PySCSS, libsass, SASS). The bad news is that none of these modules can actually compile the indented-SASS format, even though confusingly some of these libraries are called SASS.

Happily, I found RapydCSS a handy indented-SASS compiler in Python. However, as the RapydCSS API is locked into the RapydScript project, I've forked it to provide an API to work easier with other Python projects.

## Installation

    pip install indentedsass

This installs the python module `indentedsass` in the standard default lbiraries. 

As well an executable script is installed:

    sass2css sass [css]

## Indented-SASS syntax

The compilation provided by indented-SASS is quite straightforward. It wraps indented spaces with curly braces, and adds semicolons at the end fields. What's great is that this is sufficient to turn indented-SASS into valid SCSS, and thus this module future-proofs indented-SASS from deprecation in the SASS/SCSS world.

### Flat mode to CSS

If your indented-SASS file does not use any of the bells and whistles below (variables, mixins, nesting, etc.), then the plain `indented-SASS` compilation will give you valid CSS, without needing the SCSS module.

    import indentedsass
    s = '''
    body
      width: 500px
    '''
    print indentedsass.compile(s)

As per the original indented-SASS syntax, lines ending with `,` will be continued to the next line:

    #container, #article_container, #sidebar_container,
    #footer_container, #useless_container
      background-color: #DDD

That first line is treated is one whole line.

Comments are prefaced with `/*` and only the front needs to be used. Currently, this is implemented on a per-line basis:

    /* this is a comment
    body
      width: 50px

### Bells and whistles

But of course you want to take advantage of the extensions of CSS provided by the indented-SASS format. 

    import indentedsass
    s = '''
    body
      width: 500px
    '''
    print indentedsass.compile_with_scss(s)

You can use variables, prefaced by a `$`:

    $highlight-color: #999
    #big-box
      border: 1px solid $highlight-color
    #message
      color: $highlight-color 

Simple expressions:

    $big-width: 500
    #container
      width: $big-width px
    $panel-left
      float: left
      width: $big-width/2 px

Mix-ins that group common elements, and can take arguments, which are prefaced by '@':

    @mixin left($dist)
      float: left
      margin-left: $dist

    #sidebar
      @include left(10px) 
      width: 200px

Handy nesting, and self reference `&` to save even more typing:

    #article
      a
        font:
          family: Garamond
        &:link
          text-decoration: none
        &:hover
          text-decoration: underline

Extend a class with a new twist:

    #message:
      border: 1px solid red

    #bad-message:
      @extends #message
      background-color: red

Imports and comments to be implemented




