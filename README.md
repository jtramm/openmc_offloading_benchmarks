# openmc_offloading_benchmarks
A set of benchmarks for testing OpenMC

## Models

### Pincell (Fresh)

The pincell benchmark is the smallest benchmark in this repository. It is most useful for rapid code development to check for basic correctness. It features fresh fuel with 35 nuclides in total.

### Pincell (Depleted)

The pincell benchmark is the second smallest benchmark in this repository. It is identical to the fresh pincell but features depleted fuel with 272 nuclides in total.

### Minimal Depleted

This problem is identical to the depleted pincell, but it only runs for a single iteration and uses fewer particles. This may be useful for some debugging purposes.

### HM-Large

This is a medium size model useful for beginning performance analysis. It is simplified full core reactor model featuring depleted fuel. This model is known as the Hoogenboom-Martin (HM) Large variant, due to it featuring depleted fuel with 272 nuclides in total.

### SMR

This is a larger and more challenging benchmark. This model features a small modular reactor with depleted fuel (including unique isotopic compositions for each fuel region in the model) with 296 nuclides in total. This model is the primary challenge problem for the ECP ExaSMR project.

## Notes

- The default number of particles is 200,000, which leads to an overall memory footprint on-device of about 12GB. This value was chosen to work on a wide variety of devices. Better performance can be gained by increasing the number of particles (via \<particles\>n\</particles\> in settings.xml) to the maximum number that can fit in device memory.

- By default, pointwise cross section data lookups will be used. To enable multipole cross section lookups, set \<temperature_multipole\>true\</temperature_multipole\> in settings.xml.

- Each model contains an expected_results.txt file that displays the expected results. If the k-effective values at the bottom of program output match then the results can be considered validated.
