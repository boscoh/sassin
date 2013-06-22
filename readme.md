
# Indented-SASS

Indented-SASS is a beautiful space-indented format designed to express CSS stylesheets. It is, in spirit and syntax, similar to the Javascript-based Stylus format. The difference is that indented-SASS can be compiled to CSS in the Python ecosystem.

This is a fork of [`RapydCSS`](https://bitbucket.org/pyjeon/rapydcss), with a API that will work with projects like HAMLPY.

## What is indented-SASS?

Okay this gets confusing: there is a Ruby program called SASS which used to compile an indented syntax for stylesheets into CSS. Let's call this the indented-SASS format. 

Indented-SASS used to be known as the SASS format, but SASS, the program, found that it was losing market share to LESS (another CSS extension format). So SASS decided to deprecate indented-SASS and introduced the SCSS format. This lead to the situation where SASS preferably compiles SCSS, and can also compile deprecated SASS, but would rather not do so.

However, indented-SASS is a lovely format that fits well with other space-indented formats, such as YAML, HAML, and of course, Python. But it gets rather complicated if you want to use indented-SASS in Python. The good news is that there are a few Python SCSS libraries (PySCSS, libsass, SASS). The bad news is that none of these modules can actually compile the indented-SASS format, even though confusingly some of these libraries are called SASS.

Happily, I found RapydCSS a handy indented-SASS compiler in Python. However, as the RapydCSS API is locked into the RapydScript project, I've forked it to provide an API to work easier with other Python projects.

## Installation

    pip install indentedsass

This installs the python module `indentedsass` in the standard default lbiraries. 

As well an executable script is installed:

    sass2css sass [css]

## Indented-SASS syntax

The compilation provided by indented-SASS is quite straightforward. It wraps indented spaces with curly braces, and adds semicolons at the end fields. What is great that this step is sufficient to turn indented-SASS into SCSS, and thus this module is sufficient to future-proof any deprecation of indented-SASS in the Ruby SASS program.

### Flat mode

If your indented-SASS file is flat (no nesting) and does not use any variables or mixins, then this compilation will give you CSS, and you don't need any SCSS modules.


## Indented-SASS with bells and whistles

But of course you want to take advantage of the extensions of CSS provided by the indented-SASS format. Things like:

  - variables
  - mix-ins
  - hierarchical nesting









