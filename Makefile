CC = g++
#CFLAGS = -std=c++17 -Wall -g -O3 -mavx2 -fopenmp -static #VM NO LIKE AVX2 INSTRUCTIONS
CFLAGS = -std=c++17 -Wall -g -O3 -fopenmp -static 
CFLAGS += -I/usr/local/include/antlr4-runtime
LIBS = -L/usr/local/lib -lminisat -lantlr4-runtime 
SRCDIR = .

#LIBS += -lantlr4-runtime
# CFLAGS += -I/usr/local/include/antlr4-runtime
#CFLAGS += -I$(ANTLR4_INCLUDE_DIR)

LTL2SNF_TAR = ltl2snf-0.1.0.tar.gz
LTL2SNF_DIR = ltl2snf-0.1.0

# Check for Prover/Ipasir/libipasir.a
HAS_IPASIR := $(wildcard Prover/Ipasir/libipasir.a)

# By default, take all .cpp files excluding Prover/IpasirProver
SOURCES = $(shell find $(SRCDIR) -name "*.cpp" | grep -v Prover/IpasirProver)

# If libipasir.a is found, add sources from Prover/IpasirProver
ifneq ($(HAS_IPASIR),)
    LIBS += -L./Prover/IpasirProver -lipasir
    IPASIR_SRC = $(shell find ./Prover/IpasirProver -name "*.cpp")
    SOURCES += $(IPASIR_SRC)
endif

OBJECTS_MAIN = $(filter-out ./ltlmain.o, $(SOURCES:.cpp=.o))
#OBJECTS_LTLMAIN = $(filter-out ./main.o, $(SOURCES:.cpp=.o))
EXECUTABLE_MAIN = kaleidoscope
#EXECUTABLE_LTLMAIN = lumen

all: $(EXECUTABLE_MAIN) #$(EXECUTABLE_LTLMAIN)

$(EXECUTABLE_MAIN): $(OBJECTS_MAIN)
	$(CC) $(CFLAGS) $^ -o $(EXECUTABLE_MAIN) $(LIBS)

#$(EXECUTABLE_LTLMAIN): $(OBJECTS_LTLMAIN)
#	$(CC) $(CFLAGS) $^ -o $(EXECUTABLE_LTLMAIN) $(LIBS)

.cpp.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS_MAIN) $(EXECUTABLE_MAIN) 
#clean:
#	rm -f $(OBJECTS_MAIN) $(EXECUTABLE_MAIN) $(OBJECTS_LTLMAIN) $(EXECUTABLE_LTLMAIN)