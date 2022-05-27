# openmc_offloading_benchmarks
A set of benchmarks for testing OpenMC

## Models

### Small - Pincell with Fresh Fuel

The pincell benchmark is the smallest benchmark in this repository. It is most useful for rapid code development to check for basic correctness. It features fresh fuel with 35 nuclides in total.

### Medium - Pincell with Depleted Fuel

The depleted pincell benchmark is the second smallest benchmark in this repository. It is identical to the fresh pincell but features depleted fuel with 272 nuclides in total. This makes the fuel XS lookup routine considerably more expensive.

### Large - Hoogenboom-Martin "Large" Reactor

This is a full core light water reactor model useful for beginning performance analysis. It is simplified full core reactor model featuring depleted fuel. This model is known as the Hoogenboom-Martin (HM) Large variant, due to it featuring depleted fuel with 272 nuclides in total, rather than the original benchmark specification that featured fresh fuel.

### XL - Pincell with Depleted Fuel

This problem is identical to the "medium" problem, but more particles are used leading to a longer runtime.

### XXL - Hoogenboom-Martin "Large" Reactor

This problem is identical to the "Large" problem, but more particles are used leading to a longer runtime. This benchmark is most relevant for performance analysis, though also takes the longest to run.

## Notes

- Each model contains an expected_results.txt file that displays the expected results. If the k-effective values at the bottom of program output match then the results can be considered validated.
