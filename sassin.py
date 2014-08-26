# sassin (c) 2013 Bosco Ho
# Portion (C) 2012  Alexander Tsepkov
# forked from rapydcss https://bitbucket.org/pyjeon/rapydcss

import os
import StringIO

# attempt to load PySCSS module
try:
  import scss
  if 'Scss' in dir(scss):
    compile_scss = scss.Scss(scss_opts={'style':'expanded'}).compile
except:
  compile_scss = None


def compile(sass, source_fname=''):
  output_buffer = StringIO.StringIO()

  state = {
    'prev_line': '',
    'line_buffer': '',
    'first_indent': None,
    'prev_indents': [],
  }
  
  # create a separate funtion for parsing the line so that we can call it again after the loop terminates
  def parse_line(line, i_line, state):
    # remove EOL character
    line = line.rstrip() 
    
    # check for line continuation
    if state['line_buffer']:
      line = state['line_buffer'] + line.lstrip()
    if line and line[-1] == ',':
      # line continues, skip this line and proceed to the next
      state['line_buffer'] = line + ' '
      return
    else:
      state['line_buffer'] = ''

    is_comment = state['prev_line'].strip().startswith('/*')
    if is_comment:
      text = state['prev_line'].rstrip()
      if not text.endswith('*/'):
        state['prev_line'] = text + ' */'

    # mark indents from first non-whitespace column
    raw_indent = len(line) - len(line.lstrip())
    if state['first_indent'] is None:
      state['first_indent'] = raw_indent
    indent = raw_indent - state['first_indent']  

    if indent == sum(state['prev_indents']):

      if '@import' in state['prev_line']:
        import_fname = state['prev_line'].split()[1]
        if import_fname.startswith('"'):
          import_fname = import_fname[1:-1]

        if not os.path.isfile(os.path.join(os.path.dirname(source_fname), import_fname)):
          raise IOError('Error: @import {0} not found at {1}:{2}'.format(import_fname, source_fname, i_line))
        state['prev_line'] = compile_from_file(os.path.join(os.path.dirname(source_fname), import_fname))

      elif not is_comment and state['prev_line']:
        state['prev_line'] += ';'

    elif indent > sum(state['prev_indents']):
      # indentation is greater than previous: entered a new block
      state['prev_line'] += ' {'
      block_diff = indent - sum(state['prev_indents'])
      state['prev_indents'].append(block_diff)

    else: 
      # indentation is shorter than previous: exited out of block
      if not is_comment and state['prev_line']:
        state['prev_line'] += ';'
      # pull off prev_indents one-by-one and add }
      while len(state['prev_indents']) and indent < sum(state['prev_indents']):
        state['prev_indents'].pop()
        if sum(state['prev_indents']) < indent:
          raise ValueError('Error: indentation mismatch at {0}:{1}'.format(source_fname, i_line+1))
        state['prev_line'] += ' }' 

    if state['prev_line']:
      i = state['first_indent']
      left_padding = state['prev_line'][:i]
      if left_padding.strip():
        raise ValueError('Error: indentation mismatch at {0}:{1}'.format(source_fname, i_line))
      output_buffer.write(state['prev_line'][i:] + '\n')

    state['prev_line'] = line
  
  for i_line, input_line in enumerate(sass.splitlines()):
    if input_line.strip():
      parse_line(input_line, i_line, state)
  # need this last pass to flush the buffered 'prev_line'
  parse_line('\n', i_line+1, state)

  return output_buffer.getvalue()


def compile_from_file(sass_fname):
  with open(sass_fname) as f:
    sass_text = f.read()
  return compile(sass_text, source_fname=sass_fname)


def compile_with_scss(sass):
  if compile_scss is None:
    raise "Error: couldn't load a SCSS compiler"
  scss_text = compile(sass)
  return compile_scss(scss_text)

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
f = 'test/data/sass/test.sass'
scss = compile_from_file(os.path.join(PROJECT_PATH, f))
print scss