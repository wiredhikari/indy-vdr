import ctypes

# Load the libindy_vdr library
libindy_vdr = ctypes.cdll.LoadLibrary("libindy_vdr.so")

# Get a list of all ledgers in the pool
ledgers = libindy_vdr_call("libindy_vdr_get_ledgers")

# Print the list of ledgers
print(f"Ledgers: {ledgers}")
