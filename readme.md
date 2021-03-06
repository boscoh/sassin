
# sassin

`sassin` compiles SASS-indented-syntax into CSS. This is a beautiful space-indented format, similar to Javascript's [Stylus](http://learnboost.github.io/stylus/), but `sassin` works entirely in the Python ecosystem.

`sassin` turns this highly modifiable and easy-to-read fragment:

    $width: 900px

    @mixin grey-border($fr)
      border: 1px solid rgb($fr*256, $fr*256, $fr*256)
    
    #sidebar
      width: $width/3
      @include grey-border(0.5)
    
    #main
      width: $width/3*2
      @include grey-border(0.2)

Into CSS with its inscrutable hard-coded values:

    #sidebar {
      width: 300px;
      border: 1px solid #808080;
    }

    #main {
      width: 600px;
      border: 1px solid #333333;
    }

## Installation

    pip install sassin

This has one dependency `PySCSS` which should be automatically installed by pip. As well an executable script is installed:

    sassin sass [css]

SASS-indented-syntax files are recognized by a `.sass` extension.

## What is the SASS-indented-syntax?

Okay this gets confusing: there is a Ruby program called [SASS](http://sass-lang.com/) which used to compile an indented syntax for CSS, known also as SASS. However, SASS (the program) found itself losing market share to LESS, and thus, introduced the SCSS format, another curly braced syntax to compete with LESS. So SASS (the program) deprecated SASS (the old format) and focus on SCSS (the new format). 

For clarity, let's call the old SASS format, the SASS-indented-syntax.

Nevertheless, the SASS-indented-syntax is a format that fits well with other space-indented formats such as YAML, HAML, and of course, Python. The good news is that there are Python SCSS libraries (PySCSS, libsass, SASS). The bad news is that none of them compile the SASS-indented-syntax format, even though  some of these libraries confusingly call themselves *SASS.

What to do if you're a Pythonista who wants to SASS?

This is where `sassin` comes in. `sassin` compiles SASS-indented-syntax into SCSS, which is rather straightforward: it wraps indented spaces with curly braces, and adds semicolons to the end of fields. This is sufficient to turn SASS-indented-syntax into SCSS, which any SCSS compiler can read, and thus future-proofs the SASS-indented-syntax.

`sassin` is based on the [RapydCSS](https://bitbucket.org/pyjeon/rapydcss) compiler, but with better consistency with the official [SASS-indented-syntax](http://sass-lang.com/docs/yardoc/file.INDENTED_SYNTAX.html), including comments, improved indentation, error checking, and tweaked to work with projects such as HAMLPY.



## Basic SASS-indented-syntax compilation

If your SASS-indented-syntax file does not use any of the bells and whistles below (variables, mixins, nesting, etc.), then this simple compilation step will give you valid CSS.

    import sassin

    s = '''
    body
      width: 500px
    '''

    print sassin.compile_with_scss(s)

Some of the features that work in this basic mode are:

### Line extensions

Lines ending with `,` will be continued to the next line:

    #container, #article_container, #sidebar_container,
    #footer_container, #useless_container
      background-color: #DDD

That first line is treated is one whole line:

    #container, #article_container, #sidebar_container #footer_container, #useless_container {
      background-color: #DDD; }

### Comments

Comments are prefaced with `/*` and is implemented on a per-line basis:

    /* This is a comment
    /* This is another comment
    body
      /* Yep, a short width
      width: 50px 

Will give:

    /* This is a comment */
    /* This is another comment */
    body {
      /* Yep, a short width */
      width: 50px; }

### Imports

A handy little command is `@import` that - surprise surprise - imports an external `.sass` file into the current `.sass` file.

So let's say you have a `night.sass`:

    body
      background-color: black
      color: white

Then in your file `style.sass`:

    @import night.sass

    #sunny-message
       background-color: white
       color: yellow

Which produces:

    body {
      background-color: #000000;
      color: #ffffff;
    }
    #sunny-message {
      background-color: #ffffff;
      color: #ffff00;
    }

`sassin` looks for the filenames relative to the current working directory. Please don't abuse the imports, it doesn't check for circular imports - that would be your bad.

## Syntax extensions requiring PySCSS

But of course you want to take advantage of the programmatic syntax extensions introduced by SASS. This will require that you pre-install the `PySCSS` module, and the compilation is then:

    import sassin

    s = '''
    @mixin box($width)
      width: $width px
    body
      @include box(500)
    '''

    print sassin.compile_with_scss(s)

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

Cobble together simple expressions:

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

Just beware that `/` will be intrepreted as a division expression, so if `/` appears in `url()` parameters, wrap it with quotation marks `""`.

### Mix-ins with arguments

Mix-ins that group common elements, and can take arguments, which are prefaced by `@`:

    @mixin left($dist)
      float: left
      margin-left: -$dist
      width: $dist - 20
      padding-right: 20

    #sidebar
      @include left(200px) 

Gives:

    #sidebar {
      float: left;
      margin-left: -200px;
      width: 180px;
      padding-right: 20;
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


## Changelog

- 0.9.3 import relative to source file @lamnzurv



