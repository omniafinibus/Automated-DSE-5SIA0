# Determine whether to build for ARM or for Intel
ifeq ($(filter arm,$(MAKECMDGOALS)),arm)
	ARM_CROSS_COMPILE=true
endif

ifeq ($(filter simulate,$(MAKECMDGOALS)),simulate)
	ARM_CROSS_COMPILE=true
endif

# General compiler settings
CFLAGS+= -Wall -O3 -std=c99 -pedantic
LDFLAGS+= -flto

ifdef ARM_CROSS_COMPILE
# Compiler settings for ARM cross-compilation
CC=arm-linux-gnueabihf-gcc
CFLAGS+= -march=armv7-a -mfpu=neon-vfpv4
LDFLAGS+= -static -lc
else
# Compiler settings for Intel native compilation
CC=gcc
CFLAGS+= -march=native
endif

ifdef DEBUG
# Debugging symbols
CFLAGS+= -DDEBUG -g
endif

# Bash colors
RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m

# Source files
SRCS=$(wildcard *.c)
OBJS=$(SRCS:.c=.o)
EXE=inpaint

native:clean .PRECIOUS
arm:clean .PRECIOUS

# Test case
test:clean .PRECIOUS
	@echo "Running test case 'Lincoln' (native)"
	@mkdir -p results
	@rm -f results/lincoln_out.bmp
	./$(EXE) data/lincoln.bmp data/lincoln_mask.bmp results/lincoln_out.bmp
	@diff results/lincoln_out.bmp data/lincoln_golden.bmp && printf "$(GREEN)Correct result$(NC)\n" || printf "$(RED)Incorrect result$(NC)\n"

# GEM5 simulation
simulate:clean .PRECIOUS
	@echo "Running test case 'Lincoln' (GEM5)"
	@mkdir -p results
	@rm -f results/lincoln_out.bmp
	@/home/eca/gem5/build/ARM/gem5.opt --outdir=/home/eca/gem5/m5out /home/eca/gem5/configs/se_mode.py "./$(EXE) data/lincoln.bmp data/lincoln_mask.bmp results/lincoln_out.bmp"
	@diff results/lincoln_out.bmp data/lincoln_golden.bmp && printf "$(GREEN)Correct result$(NC)\n" || printf "$(RED)Incorrect result$(NC)\n"

# Link the executable
.PRECIOUS:$(EXE)
$(EXE):$(OBJS)
	$(CC) $^ -o $@ $(LDFLAGS) $(CFLAGS)

# Compile c files
%.o:%.c
	$(CC) $(INCLUDES) -c $(CFLAGS) $< -o $@

# Build dependency files if we are not cleaning
ifneq ($(filter clean,$(MAKECMDGOALS)),clean)
-include $(DEPS)
endif

CLEAN+=$(OBJS) $(DEPS) $(EXE)

clean:
	@rm -f $(CLEAN)
