import pefile
pe = pefile.PE('./file.None.0xfffffa8003b62990.dat')
print(pe.get_imphash())