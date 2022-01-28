/*
 * tap2tap.c, convert TAP file to TAP file with conversion options
 * Copyright (C) 2010 Christopher Williams
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>
#include <limits.h>

#include "c64.h"
#include "tap.h"

#define TOSTRING2(x) #x
#define TOSTRING(x) TOSTRING2(x)

#define LONG_PULSE 20000

long long_pulse = LONG_PULSE;
int outversion = -1;
float speed = 1.0;
int condense = 0;
int repeat = 0;

char *argv0;

void usage()
{
	fprintf(stderr,
"Usage: %s [-hcr] [-0|-1] [-l length] [-s speed] [tap_filename|-]\n"
"  -0|-1      Output version 0 or 1 TAP file\n"
"  -l length  Set length of long pulses in version 0 TAP files (default="TOSTRING(LONG_PULSE)")\n"
"  -c         Condense runs of long pulses (only for v0->v1)\n"
"  -r         Repeat long pulses (only for v1->v0)\n"
"  -s speed   Play TAP at 'speed' times normal\n"
"  -h         Display this help message\n",
	        argv0);
}

static void getopts(int argc, char **argv)
{
	int opt;

	argv0 = argv[0];

	while ((opt = getopt(argc, argv, "01l:rcs:h")) != -1) {
		switch (opt) {
		case '0':
			if (outversion == 1) {
				fprintf(stderr, "%s: only one of -0 and -1 may be specified\n", argv0);
				exit(1);
			}
			outversion = 0;
			break;
		case '1':
			if (outversion == 0) {
				fprintf(stderr, "%s: only one of -0 and -1 may be specified\n", argv0);
				exit(1);
			}
			outversion = 1;
			break;
		case 'l':
			long_pulse = atol(optarg);
			break;
		case 's':
			speed = atof(optarg);
			break;
		case 'c':
			condense = 1;
			break;
		case 'r':
			repeat = 1;
			break;
		case 'h':
			usage();
			exit(0);
			break;
		default: /* '?' */
			usage();
			exit(1);
		}
	}
}

static long get_pulse(struct tap *tap)
{
	static long next = -1;
	long p;
	long count = 0;
	
	if (tap->version != 0 || !condense)
		return tap_get_pulse(tap);
	
	if (next >= 0) return next;
	
	while ((p = tap_get_pulse(tap)) == V0_LONG_PULSE)
		++count;
	
	if (!count)
		return p;
	
	next = p;
	return count*LONG_PULSE;
}

static int put_pulse(long pulse, struct tap *tap)
{
	long len = pulse;
	if (tap->version == 0) {
		do {
			tap_put_pulse(pulse, tap);
			pulse -= LONG_PULSE;
		} while (repeat && pulse > 0);
		return len;
	}
	return tap_put_pulse(pulse, tap);
}

int main(int argc, char **argv)
{
	struct tap tapin, tapout;
	FILE *infile;
	long pulse;
	
	getopts(argc, argv);
	
	if (optind == argc) {
		infile = stdin;
	} else if (optind == argc - 1) {
		if (!strcmp(argv[optind], "-")) {
			infile = stdin;
		} else {
			infile = fopen(argv[optind], "rb");
			if (!infile) {
				perror(argv[optind]);
				return 1;
			}
		}
	} else {
		fprintf(stderr, "%s: too many arguments\n", argv0);
		usage();
		return 1;
	}
	if (tap_read_header(&tapin, infile)) {
		fprintf(stderr, "%s: error reading TAP file\n", argv0);
		return 1;
	}
	if (outversion < 0) tapout.version = tapin.version;
	else tapout.version = outversion;
	if (tap_write_header(&tapout, stdout)) {
		fprintf(stderr, "%s: error writing TAP file\n", argv0);
		return 1;
	}
	
	while ((pulse = get_pulse(&tapin)) >= 0) {
		if (tapin.version == 0 &&
		    pulse == V0_LONG_PULSE) {
			pulse = LONG_PULSE;
		}
		pulse /= speed;
		put_pulse(pulse, &tapout);
	}
	tap_close(&tapout);
	return 0;
}
