#!/bin/env python

import os, sys, re, readline

try:

  Q42FILE = './HaagsTranslator/src/HaagsTranslator/Translator.cs'
  Q42FILE = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), Q42FILE))

  PROMPT = 'harrie> '

  reRe = re.compile(r'new *\[\] *\{ *"([^"]+)" *, *"([^"]+)" *\}')
  reBackref = re.compile(r'\$([0-9]+)')

  if not os.path.exists(Q42FILE):
    print(f'Translation file missing: {Q42FILE}')
    print(f'You can find (and update) it with: git clone git@github.com:Q42/HaagsTranslator.git')
    sys.exit(42)

  reList = []

  with open(Q42FILE) as f:
    for line in f.readlines():
      match = reRe.search(line)
      if match:
        backref = reBackref.sub(r'\\\1', match.group(2))
        reList.append((re.compile(match.group(1)), backref))

  loop = False

  if os.isatty(0) is False:
    text = sys.stdin.read()
  elif len(sys.argv) > 1:
    text = sys.argv[1]
  else:
    text = input(PROMPT)
    loop = True

  while True:
    text = text.strip()

    for i in reList:
      text = i[0].sub(i[1], text)

    print(text)

    if not loop:
      break

    text = input(PROMPT)

except (KeyboardInterrupt, EOFError):
  print()
  sys.exit(0)
