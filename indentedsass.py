# take from rapydcss https://bitbucket.org/pyjeon/rapydcss
# Copyright (C) 2012  Alexander Tsepkov
# GPL Version 3 license


import StringIO

compile_scss = None

# attempt to load PySCSS module
if compile_scss is None:
  try:
    import scss
    if 'Scss' in dir(scss):
      compile_scss = scss.Scss(scss_opts={'compress':False}).compile
  except:
    compile_scss = None


# attempt to load python-libsass module
if compile_scss is None:
  try:
    import sass
    if 'compile' in dir(sass):
      compile_scss = lambda text: sass.compile(string=text)
  except:
    compile_scss = None


# attempt to load python-scss module
if compile_scss is None:
  try:
    import sass
    if 'compile_string' in dir(sass):
      compile_scss = sass.compile_string
  except:
    compile_scss = None


def compile(sass):
  scss_buffer = StringIO.StringIO()

  state = {
    'indent_marker':0,
    'prev_indent':  0,
    'prev_line':  '',
    'nested_blocks':0,
    'line_buffer':  '',
  }
  
  # create a separate funtion for parsing the line so that we can call it again after the loop terminates
  def parse_line(line, i_line, state):
    line = state['line_buffer'] + line.rstrip() # remove EOL character
    if line and line[-1] == '\\':
      state['line_buffer'] = line[:-1]
      return
    else:
      state['line_buffer'] = ''
    
    indent = len(line) - len(line.lstrip())
  
    # make sure we support multi-space indent as long as indent is consistent
    if indent and not state['indent_marker']:
      state['indent_marker'] = indent
  
    if state['indent_marker']:
      check = indent % state['indent_marker']
      if 0 < check < state['indent_marker']:
        raise ValueError('Error: indentation not multiple of first indent, at line {}'.format(i_line))
      indent /= state['indent_marker']
  
    if indent == state['prev_indent']:
      # same indentation as previous line
      if state['prev_line']:
        state['prev_line'] += ';'
    elif indent > state['prev_indent']:
      # new indentation is greater than previous, we just entered a new block
      state['prev_line'] += ' {'
      state['nested_blocks'] += 1
    else:
      # indentation is reset, we exited a block
      block_diff = state['prev_indent'] - indent
      if state['prev_line']:
        state['prev_line'] += ';'
      state['prev_line'] += ' }' * block_diff
      state['nested_blocks'] -= block_diff

    scss_buffer.write(state['prev_line'] + '\n')

    state['prev_indent'] = indent
    state['prev_line'] = line
  
  for i_line, input_line in enumerate(sass.splitlines()):
    parse_line(input_line, i_line, state)
  parse_line('\n', i_line+1, state) # parse the last line stored in prev_line buffer

  return scss_buffer.getvalue()


def compile_with_scss(sass):
  if compile_scss is None:
    raise "Error: couldn't load a SCSS compiler"
  scss_text = compile(sass)
  return compile_scss(scss_text)


