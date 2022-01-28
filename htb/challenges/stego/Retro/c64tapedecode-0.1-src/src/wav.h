/*
 * wav.h, prototypes and definitions for WAV file routines
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

#ifndef _WAV_H_
#define _WAV_H_

struct wav {
	FILE *file;
	unsigned short AudioFormat; /* only 1 (uncompressed PCM) is supported */
	unsigned short NumChannels;
	unsigned long SampleRate;
	unsigned long ByteRate; /* not really used */
	unsigned short BlockAlign;
	unsigned short BitsPerSample;
	unsigned long size;
	long (*getchan)(struct wav *);
	int (*putchan)(long, struct wav *);
};

enum {
	WAVERR_NONE,
	WAVERR_NOT_WAV,
	WAVERR_BAD_FORMAT,
	WAVERR_BAD_SAMPLE_RATE,
	WAVERR_UNSUPP_AUDIO_FORMAT,
	WAVERR_UNSUPP_NUM_CHANNELS,
	WAVERR_UNSUPP_BITS_PER_SAMPLE,
};

int wav_read_header(struct wav *w, FILE *f);
int wav_write_header(struct wav *w, FILE *f);
int wav_get_sample(struct wav *w, long *sample);
int wav_put_sample(struct wav *w, long *sample);
int wav_close(struct wav *w);

#endif
