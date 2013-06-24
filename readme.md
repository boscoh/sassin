
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

    ```python
    import indentedsass
    
    s = '''
    body
      width: 500px
    '''
    
    print indentedsass.compile(s)
    ```
    
### Line extensions

As per the original indented-SASS syntax, lines ending with `,` will be continued to the next line:

    #container, #article_container, #sidebar_container,
    #footer_container, #useless_container
      background-color: #DDD

That first line is treated is one whole line:

    #container, #article_container, #sidebar_container #footer_container, #useless_container {
      background-color: #DDD; }

### Comments

Comments are prefaced with `/` will be treated as a comment, and this is implemented on a per-line basis:

    / This is a comment
    / This is another comment
    body
      width: 50px

Will give:

    /* This is a comment */
    /* This is another comment */
    body {
      width: 500px; }

### Bells and whistles

But of course you want to take advantage of the extensions introduced by SASS. This will require that you install the `PySCSS` module, and the compilation to be called from:

    ```python
    import indentedsass
    
    s = '''
    @mixin box($width)
      width: $width px
    body
      @include box(500)
    '''
    ```

    print indentedsass.compile_with_scss(s)

### Variable substitution

You can use variables, prefaced by a `$`:

    $highlight-color: #999
    #big-box
      border: 1px solid $highlight-color
    #message
      color: $highlight-color 

Which makes it much easier to pass colors around, as in the resultant CSS: 

    #big-box {
      border: 1px solid #999999;
    }
    #message {
      color: #999999;
    }

### Expressions

Simple expressions:

    $big-width: 500
    #container
      width: $big-width px
    $panel-left
      float: left
      width: $big-width/2 px

And we get, in the CSS:

    #container {
      width: 500 px;
    }
    $panel-left {
      float: left;
      width: 250 px;
    }

### Mix-ins with arguments

Mix-ins that group common elements, and can take arguments, which are prefaced by '@':

    @mixin left($dist)
      float: left
      margin-left: $dist

    #sidebar
      @include left(10px) 
      width: 200px

Gives:

    #sidebar {
      float: left;
      margin-left: 10px;
      width: 200px;
    }

### Nesting

Handy nesting, and self reference `&` to save even more typing:

    #article
      a
        font:
          family: Garamond
        &:link
          text-decoration: none
        &:hover
          text-decoration: underline

Flattens out into:

    #article a {
      font-family: Garamond;
    }
    #article a:link {
      text-decoration: none;
    }
    #article a:hover {
      text-decoration: underline;
    }

### Class Extensions

Extend a class with a new twist:

    #message
      border: 1px solid red

    #bad-message
      @extend #message
      background-color: red

Creates a similar class quite easily:

    #bad-message, #message {
      border: 1px solid #ff0000;
    }
    #bad-message {
      background-color: #ff0000;
    }


Imports to be implemented




