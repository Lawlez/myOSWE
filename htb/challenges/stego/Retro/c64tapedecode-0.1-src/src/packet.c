/*
 * packet.c, decode pulses into packets
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

#include "filter.h"
#include "packet.h"
#include "messages.h"

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

typedef long fixedpoint;

#define FIXED_SHIFT 8
#define FIXED_ONE ((fixedpoint)1<<FIXED_SHIFT)

#define TO_FIXED(a) (fixedpoint)((a)*FIXED_ONE)
#define FIXED_I(a) (int)((a)/FIXED_ONE)
#define FIXED_F(a) (int)((a)%FIXED_ONE)
#define FIXED_DIV(a,b) (fixedpoint)(((a)*FIXED_ONE)/(b))

fixedpoint findzero(fixedpoint y1, fixedpoint y2)
{
	if (y1==y2) return 0;
	return FIXED_DIV(y1, y1-y2);
}

#define SYNC1 20 /* number of short pulses to sync */

#if 1
/* these values come from
 * http://www.infinite-loop.at/Power20/Documentation/Power20-ReadMe/AE-File_Formats.html:
 * short:   0x164 (356) cpu cycles
 * medium:  0x1fc (508) cpu cycles
 * long:    0x2ac (684) cpu cycles
 */
#define SHORT_PULSE 356
#define MED_PULSE   508
#define LONG_PULSE  684
#else
/* it seems that the pulse lengths are nominally evenly spaced:
 * 660 - 508 = 152
 * 508 - 365 = 143
 * after examining a tap file with taphist:
 * 648 - 508 = 140
 * 508 - 368 = 140
 */
#define PULSE_LEN_DELTA 140
#define MED_PULSE   508
#define SHORT_PULSE (MED_PULSE-PULSE_LEN_DELTA)
#define LONG_PULSE (MED_PULSE+PULSE_LEN_DELTA)
#endif

#define MIN_SHORT (0.6*SHORT_PULSE)
#define MAX_SHORT ((SHORT_PULSE+MED_PULSE)/2)
#define MIN_MED   (MAX_SHORT+1)
#define MAX_MED ((MED_PULSE+LONG_PULSE)/2)
#define MIN_LONG  (MAX_MED+1)
#define MAX_LONG  floor(1.7*LONG_PULSE)

enum sync {
	SYNC_NONE,
	SYNC_1,
	SYNC_DATA,
	//SYNC_BYTE2,
	SYNC_BIT1,
	SYNC_BIT2,
};

char *sync_names[] = {
	"NONE",
	"1",
	"DATA",
	//"BYTE2",
	"BIT1",
	"BIT2",
};

enum pulse {
	PULSE_SHORT,
	PULSE_MED,
	PULSE_LONG,
	PULSE_INVALID,
};

#define ENABLE_FILTERS 1

extern char *argv0;
extern int tap_version;
extern int input_tap;
extern int invert_samples;
extern long sample_rate;
extern struct filter highpass_filter;

/* XXX: this function can be used to high-pass filter the incoming audio */
long get_sample(FILE *infile)
{
	signed short sample = fgetc(infile) | fgetc(infile) << 8;
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

/* XXX: should the -s (speed) flag affect this? */
/* NB: this returns pulse length in cpu cycles rather than microseconds */
long tap_get_pulse(FILE *infile)
{
	int ch;
	long n;
	ch = fgetc(infile);
	if (ch) {
		n = 8*ch;
	} else if (tap_version == 1) {
		n = fgetc(infile) | (fgetc(infile)<<8) | (fgetc(infile)<<16);
		n *= 8;
	} else if (tap_version == 0) {
		n = 256 * 8;
	}
	if (feof(infile)) return 0;
	return n;
}

/* return pulse length in microseconds */
/* TODO: finish writing this */
long get_pulse(FILE *infile)
{
	static int index = 0, lastindex = 0, positive = 0;
	static fixedpoint lastzero = 0, zero = 0;
	long sample;
	static long lastsample = 0;
	fixedpoint length = 0;
	if (input_tap) return tap_get_pulse(infile);
	for (;;) {
		sample = get_sample(infile);
		if (feof(infile)) return 0;
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
	return length * (1000000L / FIXED_ONE) / sample_rate;
}


int get_packet(FILE *infile, unsigned char **pktbuf) {
	static int shorts = 0;
	static enum sync state = SYNC_NONE;
	static enum pulse lastpulse;

	static unsigned char *buf = NULL;
	static int bufsize = 0;

	fixedpoint pulselen;
	int parity;
	int bit = 0, bitnum = 0;
	int outbyte = 0;

	int bufpos = 0;

	fixedpoint min_short = MIN_SHORT;
	fixedpoint max_short = MAX_SHORT;
	fixedpoint min_med   = MIN_MED;
	fixedpoint max_med   = MAX_MED;
	fixedpoint min_long  = MIN_LONG;
	fixedpoint max_long  = MAX_LONG;
	
#if 0
	fprintf(stderr, "min_short=%d.%03d max_short=%d.%03d\nmin_med=%d.%03d max_med=%d.%03d\nmin_long=%d.%03d max_long=%d.%03d\n",
	        FIXED_I(min_short), (int)(FIXED_F(min_short)*1000/FIXED_ONE),
	        FIXED_I(max_short), (int)(FIXED_F(max_short)*1000/FIXED_ONE),
	        FIXED_I(min_med), (int)(FIXED_F(min_med)*1000/FIXED_ONE),
	        FIXED_I(max_med), (int)(FIXED_F(max_med)*1000/FIXED_ONE),
	        FIXED_I(min_long), (int)(FIXED_F(min_long)*1000/FIXED_ONE),
	        FIXED_I(max_long), (int)(FIXED_F(max_long)*1000/FIXED_ONE));
#endif
	
	for (;;) {
		int pulse;
		pulselen = get_pulse(infile);
		if (!pulselen) break;
		if (min_short <= pulselen && pulselen <= max_short) {
			MESSAGE(VERBOSE_PULSE, "short   %5.3fx expected ", (float)pulselen / SHORT_PULSE);
			pulse = PULSE_SHORT;
			++shorts;
		} else if (min_med <= pulselen && pulselen <= max_med) {
			MESSAGE(VERBOSE_PULSE, "medium  %5.3fx expected ", (float)pulselen / MED_PULSE);
			pulse = PULSE_MED;
			shorts = 0;
		} else if (min_long <= pulselen && pulselen <= max_long) {
			MESSAGE(VERBOSE_PULSE, "long    %5.3fx expected ", (float)pulselen / LONG_PULSE);
			pulse = PULSE_LONG;
			shorts = 0;
		} else {
			MESSAGE(VERBOSE_PULSE, "INVALID ");
			pulse = PULSE_INVALID;
			shorts = 0;
		}
		
		switch (state) {
		case SYNC_NONE:
			if (shorts >= SYNC1) state = SYNC_1;
			break;
		case SYNC_1:
			if (pulse == PULSE_LONG) {
				/* start of a byte sync */
				state = SYNC_DATA;
			} else if (pulse != PULSE_SHORT) {
				state = SYNC_NONE;
				if (bufpos) goto out;
			}
			break;
		case SYNC_DATA:
			if (pulse == PULSE_SHORT) {
				state = SYNC_1;
				if (bufpos) goto out;
			} else if (pulse == PULSE_MED) {
				state = SYNC_BIT1;
				bitnum = 0;
				outbyte = 0;
			} else {
				state = SYNC_NONE;
				if (bufpos) goto out;
			}
			break;
		case SYNC_BIT1:
			if (pulse == PULSE_SHORT || pulse == PULSE_MED) {
				state = SYNC_BIT2;
			} else {
				state = SYNC_NONE;
				if (bufpos) goto out;
			}
			break;
		case SYNC_BIT2:
			if (pulse != lastpulse &&
			    (pulse == PULSE_SHORT || pulse == PULSE_MED)) {
				bit = (pulse == PULSE_SHORT);
				if (bitnum < 8) {
					outbyte |= bit << bitnum;
					state = SYNC_BIT1;
				} else { /* parity bit */
					parity = bit;
					state = SYNC_1;
				}
				MESSAGE(VERBOSE_BIT, "bit=%d ", bit);
				++bitnum;
			} else {
				MESSAGE(VERBOSE_BIT, "bad bit ");
				state = SYNC_NONE;
				if (bufpos) goto out;
			}
			break;
		default:
			fprintf(stderr, "%s: logic error!\n", argv0);
			exit(1);
		}
		lastpulse = pulse;
		
		MESSAGE(VERBOSE_PULSE, "state: %s\n", sync_names[state]);
		
		if (bitnum == 9) { /* we have outbyte */
			int p = 1;
			state = SYNC_1;
			bitnum = 0;
			MESSAGE(VERBOSE_BYTE, "outbyte=%-3d (%c) ", outbyte, isprint(outbyte) ? outbyte : ' ');
			for (bit = 1; bit < 256; bit <<= 1)
				p ^= !!(outbyte&bit);
			//MESSAGE(VERBOSE_BIT, "parity is %s\n", p == parity ? "correct" : "INCORRECT");
			if (p != parity) {
				/* state = SYNC_NONE? */
			}
			if (bufpos >= bufsize) {
				int oldsize = bufsize;
				bufsize += 65536;
				buf = realloc(buf, bufsize);
				if (buf)
					memset(&buf[oldsize], 0, bufsize - oldsize);
			}
			if (buf) {
				MESSAGE(VERBOSE_BYTE, "buf[%d] = 0x%02x\n", bufpos, outbyte);
				assert(bufpos < bufsize);
				buf[bufpos++] = outbyte;
			} else {
				MESSAGE(VERBOSE_BYTE, "ERROR: buf=NULL!\n");
			}
		}
	}
	
out:
	*pktbuf = buf;
	return bufpos;
}
