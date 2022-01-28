/*
 * tap2wav.c, convert TAP file to WAV
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
#include "wav.h"
#include "fixedpoint.h"
#include "filter.h"

/*
 * TODO:
 * This current version only outputs square waves, which have a pulse
 * resolution of 1/samplerate. At 16000 samples/sec, for example, the pulse
 * resolution is 31.25 microseconds, or about 1/4 the resolution of a TAP file
 * (which stores pulse lengths in terms of 8 cpu cycles). The effective
 * resolution can be increased by modifying the amplitude of one sample at each
 * zero crossing (either before or after will work):
 *
 * Simple square waves:
 * |
 * | X---X---X
 * |          \ 
 * +-+---+---+-#-+---+---+--
 * |            \
 * |             X---X---X
 * |
 * 
 * With modified amplitude:
 * |
 * | X---X---X
 * |          '.
 * +-+---+---+--#+---+---+--
 * |             X,_
 * |                'X---X
 * |
 * 
 * X = sample point
 * # = zero crossing
 * -,'\ etc = interpolated values beteen sample points
 * 
 * In this example, the interpolated (simple linear interpolation) zero
 * crossing is 1/6 sample time later with modified amplitude than with simple
 * square waves.
 * 
 * This can be implemented using fixed-point numbers as in the original
 * c64tapedecode program. 24.8 fixed-point numbers are more than sufficient for
 * this application.
 * 
 * y2 = y1 - y1/x
 * 0 <= x < 1
 * for x < 0.5:
 *   y2 is closer to wave 0 (right side)
 *   y1 is wave 1 (left side)
 *   y2 = y1 - y1/(1-x)
 * 
 * another idea:
 * at the zero crossing set the distance between the 2 stradling points half
 * the full amplitude, and set the first point to x * the left wave
 * 
 * @ = control point
 * # = zero crossing
 * 
 * x = 0.0
 * |
 * | X---X,   
 * |       \   
 * +-+---+---@---+---+---+--
 * |           \    
 * |            'X---X---X
 * 
 * x = 0.5
 * |
 * | X---X,_  
 * |        '@,
 * +-+---+---+-#-+---+---+--
 * |            'X,_
 * |                'X---X
 * 
 * x = 1.0
 * |
 * | X---X---@,   
 * |           \   
 * +-+---+---+---X---+---+--
 * |               \    
 * |                'X---X
 */

#define SAMPLERATE 44100L
#define LOW (SHRT_MIN / 2)
#define HIGH (SHRT_MAX / 2)

char *argv0;
int invert = 0;
long samplerate = SAMPLERATE;
long lowpass_freq = 0;
float speed = 1.0;
struct filter lowpass_filter;

void usage()
{
	fprintf(stderr,
"Usage: %s [-hr] [-f rate] [-L freq] [-s speed] [tap_filename|-]\n"
"  -f rate   Set sample rate to 'rate'\n"
"  -L freq   Apply a low-pass filter at 'freq' Hz (try -L 8000).\n"
"            This can be used to round out sharp corners in the signal to\n"
"            prevent ringing.\n"
"  -r        Invert samples\n"
"  -s speed  Play sound at 'speed' times normal\n"
"  -h        Display this help message\n",
	        argv0);
}

static void getopts(int argc, char **argv)
{
	int opt;

	argv0 = argv[0];

	while ((opt = getopt(argc, argv, "f:L:rs:h")) != -1) {
		switch (opt) {
		case 'f':
			samplerate = atol(optarg);
			if (samplerate <= 0) {
				fprintf(stderr, "%s: sample rate must be greater than 0!\n", argv0);
				exit(1);
			}
			if (samplerate < 16000L) {
				fprintf(stderr, "%s: warning: sample rate should be at least 16000 for best results\n", argv0);
			}
			break;
		case 'L':
			lowpass_freq = atol(optarg);
			if (lowpass_freq < 0) {
				fprintf(stderr, "%s: lowpass frequency cannot be less than 0!\n", argv0);
				exit(1);
			}
			break;
		case 'r':
			invert = 1;
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

int main(int argc, char **argv)
{
	struct tap tapfile;
	struct wav wavfile;
	FILE *infile;
	long pulse;
	long i;
	fixedpoint len, accum;
	long channels[2];
	int wave[2];
	int sample;
	
	getopts(argc, argv);
	if (invert) {
		wave[0] = LOW;
		wave[1] = HIGH;
	} else {
		wave[0] = HIGH;
		wave[1] = LOW;
	}
	
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
	if (tap_read_header(&tapfile, infile)) {
		fprintf(stderr, "%s: error reading TAP file\n", argv0);
		return 1;
	}
	wavfile.SampleRate = samplerate;
	wavfile.BitsPerSample = 8;
	wavfile.NumChannels = 1;
	if (wav_write_header(&wavfile, stdout)) {
		fprintf(stderr, "%s: error writing WAV file\n", argv0);
		return 1;
	}
	filter_init(&lowpass_filter, lowpass_freq, wavfile.SampleRate);
#if 0
	/* put one initial sample so the first pulse is recognized */
	channels[0] = wave[1];
	wav_put_sample(&wavfile, channels);
	accum = TO_FIXED(1.5);
#else
	accum = TO_FIXED(2);
#endif
	while ((pulse = tap_get_pulse(&tapfile)) >= 0) {
		//fprintf(stderr, "pulse: %6ld (%04lx)\n", pulse, pulse);
		//if (pulse < 8*256)
			//++pulsehist[pulse/8];
		len = TO_FIXED(((double)pulse * samplerate / PAL_MHZ / speed / 1000000));

		if (len < TO_FIXED(2)) {
			fprintf(stderr, "%s: warning: pulse length (%ld) is less than 2 samples\n", argv0, pulse);
		}
#if 0
		accum = FIXED_F(len + accum);
#else
		len += accum;
		accum = FIXED_F(len);
#endif
#if 0
		fprintf(stderr, "%ld.%03ld 0.%03ld \n",
		        FIXED_I(len),
		        FIXED_F(len) * 1000 / FIXED_ONE,
		        FIXED_F(accum) * 1000 / FIXED_ONE);
#endif
		
		for (i = 0; i < FIXED_I(len) / 2 - 1; ++i) {
			channels[0] = filter_lowpass(&lowpass_filter, wave[0]) << 16;
			wav_put_sample(&wavfile, channels);
		}
		
		for (; i < FIXED_I(len) - 2; ++i) {
			channels[0] = filter_lowpass(&lowpass_filter, wave[1]) << 16;
			wav_put_sample(&wavfile, channels);
		}
#if 0
		channels[0] = FIXED_MUL(wave[1], accum) +
		              FIXED_MUL(wave[0], FIXED_ONE - accum);
		wav_put_sample(&wavfile, channels);
#else
		sample = FIXED_MUL(wave[1], accum);
		channels[0] = filter_lowpass(&lowpass_filter, sample) << 16;
		wav_put_sample(&wavfile, channels);
		sample -= wave[1];
		channels[0] = filter_lowpass(&lowpass_filter, sample) << 16;
		wav_put_sample(&wavfile, channels);
#endif
	}
	wav_close(&wavfile);
	return 0;
}
