##
# Project Title
#
# @file
# @version 0.1


CC=./clang-wrapper.sh
# CC=clang
CFLAGS=-Isrc/
DEPS = src/test.h
OBJ = src/main.o src/test.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# build: main
# ./post_process

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)


clean :
	@rm *.o $(objects) *.ll .*.bc .*.o *.out *.opt main *.bc
# end
