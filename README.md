# CEGARBoxCPP

## Original Authorship
Robert McArthur and Cormac Kikkert, for contact email cormac.kikkert@anu.edu.au

## Programs
There are two programs in this repo.

`kaleidoscope`: CEGARBox++(K), handles K extended with single axioms OR global assumptions OR converse modalities (tense logic).

`lumen`: CEGARBox++(LTL), handles LTL and LTL-f, the compilation of which has been commented out of the `Makefile`, but can be reinstated.

## Git Cloning
If you are using a Windows machine with WSL, note that CEGARBox may have conflicting folder names `TrieformProverKt` and `TrieformProverKT` since Windows directories are usually case insensitive. To change this, create an empty folder and in Powershell/Cmd, type:

```
fsutil.exe file setCaseSensitiveInfo <path> enable
```
where `path` is the path to the empty directory. You can now clone the repository here.

## Compilation
Statically compiled files `kaleidoscope` (compiled on Windows 10 with WSL version 2.3.24) and `lumen` (compiled on Ubuntu 20.04.3) are already available on this repo. To recompile these on a different machine, note that the following will have to be installed:

1. [Minisat](https://github.com/agurfinkel/minisat), a SAT-solver. This is a fork, as the original is outdated and no longer works.
2. [antlr4](https://www.antlr.org/download.html) for LTL parsing. This is the C++ target
3. [ltl2snf](https://nalon.org/#software) for converting LTL formula to SNF.

If your CPU does not have AVX2 instructions (or if you are using a virtual machine that is not configured for it), there is a line at the start of the `Makefile` that excludes it.

## Prerequisites
```
sudo apt-get update && sudo apt-get install -y build-essential wget unzip tar cmake sudo libz-dev libgoogle-glog-dev
```

## Installing ANTLR4
```
(
export ANTLR_DIR=/antlr4 && wget https://www.antlr.org/download/antlr4-cpp-runtime-4.13.0-source.zip && \
sudo mkdir -p $ANTLR_DIR && sudo unzip -q antlr4-cpp-runtime-4.13.0-source.zip -d $ANTLR_DIR && \
sudo mkdir -p $ANTLR_DIR/build $ANTLR_DIR/run && cd $ANTLR_DIR/build && sudo cmake .. && sudo make install
)
```

## Installing Minisat
```
(
git clone https://github.com/agurfinkel/minisat.git && cd minisat && \
make config prefix=/usr && sudo make install
)
```

## Installing ltl2snf (unnecessary unless you want to recompile `lumen`)
```
(
wget https://nalon.org/software/ltl2snf-0.1.0.tar.gz && \
tar xzf ltl2snf-0.1.0.tar.gz && cd ltl2snf-0.1.0 && make && mv ./ltl2snf ../ && cd .. && rm -rf ltl2snf-0.1.0*
)
```

## Installing CEGARBoxCPP
Run ``make`` to compile CEGARBox.

Then test with `cd Examples && ./tests.sh` (there may be issues with the text files on Windows).

## Input Formula
CEGARBox(K) accepts file input. Input is terminated by a newline and valid input formula are defined by the following grammar:
```
Index ::= Nat || -Nat
Atom ::= Alphanumeric String
Formula ::=
 Atom || $true || $false || ~Formula ||
 [Index] Formula || <Index> Formula || []Formula || <>Formula || 
 Formula | Formula || Formula & Formula || Formula => Formula || 
 Formula <=> Formula || (Formula) 
```

Here, negative numbers are used to define converse for tense logic. For example ``[-1]`` is the converse of ``[1]``.

CEGARBox(K) does not handle intohylo files! So files with BEGIN and END won't work. Please refer to the examples in `Examples`.

CEGARBox(LTL) uses the same input as ltl2snf:
```
PROPOSITIONAL SYMBOLS: an alfanumeric sequence starting with a letter: p, p1, p_1 (underscore should not be used at the beginning of a name)
CONSTANTS: true, false
NOT: -, ~, not
AND: &, and
OR: |, or
IMPLICATION: ->, =>, imp, imply, implies
ONLY IF: <-, <=
DOUBLE IMPLICATION: <->, <=>, iff
ALWAYS: [], always
EVENTUALLY: <>, sometime
UNTIL: U, until
UNLESS: W, unless
```

## Running CEGARBox 

``./main -f <input_file> [options]``

Options:

* Reflexivity: ``--reflexive`` or ``-t``
* Symmetry: ``--symmetric`` or ``-b``
* Transitivity: ``--transitive`` or ``-4``
* Seriality: ``--serial`` or ``-d``
* Euclidean: ``--euclidean`` or ``-e`` or ``5``
* Valid (whether input formula is valid): ``--valid`` or ``-a``
* Tense: ``--tense`` or `-n`
* Verbose: ``--verbose`` or `-v`
* Use one SAT solver: ``--onesat`` or ``-1``
* KSP: ``--ksp`` or ``-k``
* Use an underlying DAG datastructure: ``--dag`` or ``-q``
* File containing global assumptions: ``--globalAssumptions`` or ``-u``

To use the local prover add `-l`
To use the global prover add `-g`
(Default is bespoke)

## Benchmarks

MQBF, 3CNF and LWB_K benchmarks can be downloaded from [here](http://www.cril.univ-artois.fr/~montmirail/mosaic/#)
ALC benchmarks can be downloaded from [here](https://web.archive.org/web/20190305011522/http://users.cecs.anu.edu.au/~rpg/BDDTab/)

## Examples
Some examples to see how to use the tool are in `Examples`.
Note: logics besides K, KD, KT, KB, K4, K5, and tense are untested, and may not work.

## S5-specific Tests

The `Testing` folder has a Python script that runs ``kaleidoscope`` on all 100 formulae in `Tests` using the command:

```
./kaleidoscope -f <file_name>.txt -t -5
```

If you add a file to `Tests`, ensure there is either the word `sat` or `unsat` in the file name. These have run on both Windows 10 with WSL and Ubuntu 20.04.6 (via virtual machine). The python file accepts the same inputs as ``kaleidoscope`` as well as the following symbols:
```
NOT: ¬
AND: ∧
OR: ∨
NECESSARY: □
```