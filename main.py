from functions import *
from printers import *
import time

start = time.time()
separator('DALLAS')
print("Getting MFP-A meters...")
canon(dal_mfp_a, 'DAL-MFP-A ---> 55258', '125108')

print("Getting MFP-B meters...")
canon(dal_mfp_b, 'DAL-MFP-B ---> 71156', '125108')

print("Getting MFP-C meters...")
canon(dal_mfp_c, 'DAL-MFP-C ---> 55021', '125108')

print("Getting MFP-D meters...")
canon(dal_mfp_d, 'DAL-MFP-D ---> 55259', '125108')

print("Getting MFP-E meters...")
xerox(dal_mfp_e, 'DAL-MFP-E ---> 43644')

print("Getting MFP-F meters...")
canon(dal_mfp_f, 'DAL-MFP-F ---> 55260', '125108')

print("Getting MFP-G meters...")
canon(dal_mfp_g, 'DAL-MFP-G ---> 55215', '125108')

print("Getting MFP-H meters...")
canon(dal_mfp_h, 'DAL-MFP-H ---> 55261', '125108')

print("Getting MFP-I meters...")
canon(dal_mfp_i, 'DAL-MFP-I ---> 55262', '108')

print("Getting MFP-J meters...")
canon(dal_mfp_j, 'DAL-MFP-J ---> 39632', '125108')

print("Getting MFP-K meters...")
canon(dal_mfp_k, 'DAL-MFP-K ---> 55253', '125108')

print("Getting MFP-M meters...")
canon(dal_mfp_m, 'DAL-MFP-M ---> 39631', '125108')

print("Getting MFP-T meters...")
xerox(dal_mfp_t, 'DAL-MFP-T ---> 23579')
print("Done with Dallas....")

separator('FRISCO')
print("Getting MFP-A meters...")
canon(fri_mfp_a, 'FRI-MFP-A', '125108')
print("Done with Frisco....")

separator('HOUSTON')
print("Getting MFP-A meters...")
canon(hou_mfp_a, 'HOU-MFP-A', '125108')
print("Done with Houston....")

separator('Los Angeles')
print("Getting MFP-A meters...")
canon(lax_mfp_a, 'LAX-MFP-A', '124109')
print("Done with Los Angeles....")

separator('New York City')
print("Getting MFP-A meters...")
canon(nyc_mfp_a, 'NYC-MFP-A', '105108')

print("Getting MFP-B meters...")
canon(nyc_mfp_b, 'NYC-MFP-B', '105108')
print("Done with NYC....")

separator('PHOENIX')
print("Getting MFP-A meters...")
canon(phx_mfp_a, 'PHX-MFP-A', '124109')

print("Getting MFP-B meters...")
canon(phx_mfp_b, 'PHX-MFP-B', '125108')
print("All DONE!!")

runtime = time.time() - start
print("Finished in {:.2f} seconds.".format(runtime))
input("Press enter to finish...")
