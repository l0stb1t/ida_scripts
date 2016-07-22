ea = ScreenEA()
ins = list(FuncItems(ea))
for i in ins:
	disasm = GetDisasm(i)
	if 'call' in disasm and not 'runtime' in disasm:
		print '%x'%i, disasm
