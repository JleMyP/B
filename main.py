profile = False

if profile:
  import cProfile

  cProfile.run("import shooter")
  input("")
else:
  import shooter