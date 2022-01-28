CFLAGS=-Wall -O2
LDFLAGS=-lm

PREFIX=/usr/local
BINDIR=${PREFIX}/bin

OBJ=wav2tap tap2wav tap2tap mktap c64tapedecode

all: ${OBJ}

install: ${OBJ}
	cp ${OBJ} ${BINDIR}

c64tapedecode: c64tapedecode.o packet.o filter.o io.o

c64tapedecode.o: c64tapedecode.c packet.h filter.h messages.h
packet.o: packet.c packet.h filter.h messages.h
filter.o: filter.c filter.h

# the new utilities
wav.o: wav.c wav.h commonio.h
tap.o: tap.c tap.h commonio.h

wav2tap: wav2tap.o wav.o tap.o filter.o io.o opts.o
wav2tap.o: wav2tap.c wav.h tap.h filter.h fixedpoint.h c64.h opts.h

tap2wav: tap2wav.o tap.o wav.o filter.o io.o
tap2wav.o: tap2wav.c wav.h tap.h filter.h fixedpoint.h c64.h

tap2tap: tap2tap.o tap.o io.o
tap2tap.o: tap2tap.c tap.h

mktap: mktap.o tap.o io.o
mktap.o: mktap.c tap.h

io.o: io.c commonio.h

clean:
	rm -f *.o ${OBJ}
