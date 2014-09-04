# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
from nose.tools import eq_, raises
import sassin


def splitlines(text):
  return filter(lambda l: l.strip(), text.splitlines())


class SassinTest(unittest.TestCase):
  def test_indent(self):
    in_sass = """
a
  font:
      family: Helvetica
    """
    out_css = sassin.compile(in_sass)
    out_lines = splitlines(out_css)
    test_css = """
a {
  font: {
      family: Helvetica; } }
    """
    test_lines = splitlines(test_css)
    eq_(out_lines, test_lines)

  def test_comment(self):
    in_sass = """
/* comment
body
  /* comment
  background-color: white
    """
    out_css = sassin.compile(in_sass)
    out_lines = splitlines(out_css)
    test_css = """
/* comment */
body {
  /* comment */
  background-color: white; }
    """
    test_lines = splitlines(test_css)
    eq_(out_lines, test_lines)

  def test_line_continuation(self):
    in_sass = """
#container, #article_container, 
#sidebar_container,
#footer_container, #useless_container
  background-color: #DDD
    """
    out_css = sassin.compile(in_sass)
    out_lines = splitlines(out_css)
    test_css = """
#container, #article_container, #sidebar_container, #footer_container, #useless_container {
  background-color: #DDD; }
    """
    test_lines = splitlines(test_css)
    eq_(out_lines, test_lines)

  def test_import(self):
    in_sass = """
@import test-import.sass
    """
    out_css = sassin.compile(in_sass)
    out_lines = splitlines(out_css)
    test_css = """
body {
  background-color: #EEE; }
    """
    test_lines = splitlines(test_css)
    eq_(out_lines, test_lines)

  @raises(ValueError)
  def test_exception_for_misaligned_identation(self):
      in_sass = """
  a
    font:
        family: Helvetica
      weight: bold
      """
      out_css = sassin.compile(in_sass)

  @raises(ValueError)
  def test_exception_for_margin_identation(self):
      in_sass = """
    a
      font:
        family: Helvetica
   #new_class
      """
      out_css = sassin.compile(in_sass)

  def test_import_with_path(self):
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    f = 'data/sass/test.sass'

    scss = sassin.compile_from_file(os.path.join(PROJECT_PATH, f))


if __name__ == '__main__':
  unittest.main()