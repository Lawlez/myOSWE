/*
 * wav2tap.c, convert WAV file to TAP
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
#include <ctype.h>
#include <math.h>
#include <assert.h>
#include <limits.h>
#include <unistd.h>

#include "filter.h"
#include "messages.h"
#include "wav.h"
#include "tap.h"
#include "fixedpoint.h"
#include "c64.h"

/* 
 * The following feature has been tested and found to work properly! This new
 * feature enables the program to decode signals down to about 8kHz sample
 * rate, though the program is somewhat more sensitive to the speed of playback
 * than at higher sample rates.
 * 
 * increase precision in wavelength calculations by calculating the zero
 * crossings of the waveform:
 * 
 * X
 *  \
 *   \    .X
 * ---+--+--
 *     X`
 * The X's are sample points, the +'s are the calculated zero crossings:
 * x = y1 / (y1 - y2)
 * This can be done easily with fixed-point math (1/256 should be sufficient
 * precision). The pulse width constants can also be in fixed-point to increase
 * their precision as well.
 */

fixedpoint findzero(fixedpoint y1, fixedpoint y2)
{
	if (y1==y2) return 0;
	return FIXED_DIV(y1, y1-y2);
}

#define ENABLE_FILTERS 1

char *argv0;
int invert_samples;
//long sample_rate;
float speed = 1.0; /* speed of output (<1 to slow it down) */
enum verbosity verbosity;
struct filter highpass_filter;
long highpass_freq = 0;

long get_sample(struct wav *wavfile)
{
	long ch[2];
	wav_get_sample(wavfile, ch);
	short sample = (ch[0]/2 + ch[1]/2) >> 16;
	MESSAGE(VERBOSE_WAVEFORM, "%6hd, ", sample);
	
#if ENABLE_FILTERS
	sample = filter_highpass(&highpass_filter, sample);
#endif
	
	if (verbosity >= VERBOSE_WAVEFORM) {
		int i;
		fprintf(stderr, "%6hd ", sample);
		for (i = 0; i < ((long)sample + 32768) * 50 / 65536; ++i)
			fputc('#', stderr);
		fputc('\n', stderr);
	}
	if (invert_samples) /* invert the sample */
		sample = -sample;
	//fprintf(stderr, "get_sample: %hd\n", sample);
	return sample;
}

#if 0
/* return pulse length in microseconds */
/* TODO: finish writing this */
long get_pulse(struct wav *wavfile)
{
	static int index = 0, lastindex = 0, positive = 0;
	static fixedpoint lastzero = 0, zero = 0;
	long sample;
	static long lastsample = 0;
	fixedpoint length = 0;
	for (;;) {
		sample = get_sample(wavfile);
		if (feof(wavfile->file)) return 0;
		//fprintf(stderr, "get_pulse: sample=%ld index=%d\n", sample, index);
		
		if (!positive && sample > 0) {
			/* start of a new cycle */
			zero = findzero(lastsample, sample);
#if 0
			fprintf(stderr, "sample=%hd lastsample=%hd length = %d + (%d - %d) / %d\n",
			        sample, lastsample, index-lastindex, (int)zero, (int)lastzero, (int)FIXED_ONE);
#endif
			length = TO_FIXED(index-lastindex) + zero - lastzero;
			lastzero = zero;
			MESSAGE(VERBOSE_PULSE, "index=%8d wavelength=%3ld.%03ld ",
			        index,
			        (long)FIXED_I(length), (long)FIXED_F(length)*1000/FIXED_ONE);
			//fprintf(stderr, "get_pulse: length=%ld index=%d lastindex=%d\n", length, index, lastindex);
			lastindex = index;
		}
		positive = sample > 0;
		++index;
		lastsample = sample;
		if (length) break;
	}
#define MAX_LENGTH TO_FIXED(LONG_MAX / 1000000L)
	if (length > MAX_LENGTH) length = MAX_LENGTH;
	return length * (1000000L / FIXED_ONE) / wavfile->SampleRate;
}
#else
static fixedpoint get_pulse(struct wav *wavfile)
{
	fixedpoint len;
	long count = 0;
	long sample;
	static long lastsample = 0;
	fixedpoint zero;
	static fixedpoint lastzero = FIXED_ONE * 2;
	
	for (;;) {
		sample = get_sample(wavfile);
		if (feof(wavfile->file)) return 0;
		++count;
		if (lastsample < 0 && sample >= 0) {
			zero = findzero(TO_FIXED(lastsample), TO_FIXED(sample));
			len = TO_FIXED(count) + zero - lastzero;
			lastzero = zero;
			lastsample = sample;
			break;
		}
		lastsample = sample;
	}
	double f = (len * 1000000. + wavfile->SampleRate / 2) /
	            wavfile->SampleRate;
	if (f > LONG_MAX) return LONG_MAX;
	return f;
}
#endif

static int outversion = -1;

void usage(void)
{
	fprintf(stderr,
"Usage: %s [-hr] [-0|-1] [-H freq] [-s speed] [tap_filename|-]\n"
"  -0|-1     Output version 0 or 1 TAP file\n"
"  -H freq   Apply a high-pass filter at 'freq' Hz (try -H 100).\n"
"            This can be used to remove DC offsets in the WAV input.\n"
"  -r        Invert samples\n"
"  -s speed  Play output at 'speed' times normal\n"
"  -h        Display this help message\n",
	        argv0);
}

static void getopts(int argc, char **argv)
{
	int opt;

	argv0 = argv[0];

	while ((opt = getopt(argc, argv, "01H:rs:h")) != -1) {
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
		case 'H':
			highpass_freq = atol(optarg);
			if (highpass_freq < 0) {
				fprintf(stderr, "%s: highpass frequency cannot be less than 0!\n", argv0);
				exit(1);
			}
			break;
		case 'r':
			invert_samples = 1;
			break;
		case 's':
			speed = atof(optarg);
			if (speed < 0.1 || 10 < speed) {
				fprintf(stderr, "%s: speed must be between 0.1 and 10!\n", argv0);
				exit(1);
			}
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

/* TODO: copy most options from c64tapedecode to here,
 * and add option for NTSC/PAL timing:
 * NTSC: 1.022727 MHz
 * PAL:  0.9852484 MHz
 */
int main(int argc, char *argv[])
{
	struct wav wavfile;
	struct tap tapfile;
	argv0 = argv[0];
	long pulse;
	FILE *infile;
	
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

	if (wav_read_header(&wavfile, infile)) {
		fprintf(stderr, "%s: error reading WAV file\n", argv0);
		return 1;
	}
	filter_init(&highpass_filter, highpass_freq, wavfile.SampleRate);
	if (outversion == -1) outversion = 1;
	tapfile.version = outversion;
	if (tap_write_header(&tapfile, stdout)) {
		fprintf(stderr, "%s: error writimg TAP file\n", argv0);
		return 1;
	}
	while ((pulse = get_pulse(&wavfile)) != 0) {
		//fprintf(stderr, "%s: %6ld\n", argv0, pulse);
		tap_put_pulse(FIXED_I(pulse*PAL_MHZ/speed + FIXED_HALF), &tapfile);
	}
	tap_close(&tapfile);
	return 0;
}
