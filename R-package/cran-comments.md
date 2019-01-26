## Test environments

* local OS X install, R 3.5.1
* ubuntu 14.04 (on travis-ci), R 3.5.1
* win-builder (devel)

## R CMD check results

```
0 errors | 0 warnings | 1 note
```

The following note appears during R CMD check since this is a new package:

```
* checking CRAN incoming feasibility ... NOTE
Maintainer: 'Yuan Tang <terrytangyuan@gmail.com>'

New submission
```

## Comments

The examples are wrapped in `\dontrun{}` block and most of the tests are skipped via `skip_on_cran()` since they can only be run when both Python and TensorFlow are installed but this is currently not viable on CRAN test machines.
