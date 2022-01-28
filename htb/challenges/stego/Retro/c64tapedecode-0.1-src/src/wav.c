/*
 * wav.c, routines for reading writing WAV files
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
#include <string.h>

#include "wav.h"
#include "commonio.h"

enum id {
	ID_RIFF,
	ID_FMT,
	ID_DATA,
	ID_WAVE,
	ID_UNKNOWN
};

/* these must be in the same order as enum id! */
static const char *idnames[] = {
	"RIFF",
	"fmt ",
	"data",
	"WAVE",
	NULL
};

#define getLong(w) fgetlong((w)->file)
#define getWord(w) fgetword((w)->file)
#define putLong(n, w) fputlong((n), (w)->file)
#define putWord(n, w) fputword((n), (w)->file)

static enum id getID(struct wav *w)
{
	char id[4];
	const char **np;
	
	fread(id, 1, 4, w->file);
#if 0
	fprintf(stderr, "getID: %.4s\n", id);
#endif
	for (np = idnames; *np; ++np) {
		if (!memcmp(id, *np, 4)) return np - idnames;
	}
	return ID_UNKNOWN;
}

static int putID(enum id id, struct wav *w)
{
	fwrite(idnames[id], 1, 4, w->file);
	return 0;
}

/* 8-bit is unsigned */
static long get_chan8(struct wav *w)
{
	unsigned long n = (unsigned char)(getc(w->file) + 128);
	return (n << 24) | (n << 16) | (n << 8) | n;
}

/* 16-, 24-, and 32-bit are signed */
static long get_chan16(struct wav *w)
{
	unsigned long n = (unsigned short)getWord(w);
	return (n << 16) | n;
}

static long get_chan24(struct wav *w)
{
	char b[3];
	fread(b, 1, 3, w->file);
	return ((unsigned long)b[2] << 24) | ((unsigned long)b[1] << 16) |
	       ((unsigned long)b[0] << 8) | ((unsigned long)b[2]);
}

static long get_chan32(struct wav *w)
{
	return getLong(w);
}

static int put_chan8(long n, struct wav *w)
{
	putc((n>>24) + 128, w->file);
	return 0;
}

static int put_chan16(long n, struct wav *w)
{
	putWord(n>>16, w);
	return 0;
}

static int put_chan24(long n, struct wav *w)
{
	putc((n>>8) & 0xff, w->file);
	putc((n>>16) & 0xff, w->file);
	putc((n>>24) & 0xff, w->file);
	return 0;
}

static int put_chan32(long n, struct wav *w)
{
	putLong(n, w);
	return 0;
}

int wav_read_header(struct wav *w, FILE *f)
{
	unsigned long wavsize;
	unsigned long fmtsize;
	unsigned long datasize;
	
	w->file = f;

	if (getID(w) != ID_RIFF) return WAVERR_NOT_WAV; /* not in WAV format */
	wavsize = getLong(w);
	
	if (getID(w) != ID_WAVE) return WAVERR_BAD_FORMAT;
	if (getID(w) != ID_FMT) return WAVERR_BAD_FORMAT;
	fmtsize = getLong(w);
	if (fmtsize != 16) return WAVERR_BAD_FORMAT;
	w->AudioFormat = getWord(w);
	if (w->AudioFormat != 1) return WAVERR_UNSUPP_AUDIO_FORMAT;
	w->NumChannels = getWord(w);
	if (w->NumChannels < 1 || 2 < w->NumChannels) return WAVERR_UNSUPP_NUM_CHANNELS;
	w->SampleRate = getLong(w);
	if (w->SampleRate == 0) return WAVERR_BAD_SAMPLE_RATE;
	w->ByteRate = getLong(w);
	w->BlockAlign = getWord(w);
	w->BitsPerSample = getWord(w);
	if (w->BlockAlign < w->BitsPerSample / 8) return WAVERR_BAD_FORMAT; /* different error? */
	
	/* other bit depths may be valid, but these
	 * are the only ones that we support */
	switch (w->BitsPerSample) {
	case 8: w->getchan = get_chan8; break;
	case 16: w->getchan = get_chan16; break;
	case 24: w->getchan = get_chan24; break;
	case 32: w->getchan = get_chan32; break;
	default: return WAVERR_UNSUPP_BITS_PER_SAMPLE;
	}
	
	if (getID(w) != ID_DATA) return WAVERR_BAD_FORMAT;
	datasize = getLong(w);
	return 0;
}

int wav_write_header(struct wav *w, FILE *f)
{
	unsigned long wavsize;
	unsigned long fmtsize;
	unsigned long datasize;
	
	w->file = f;

	if (w->NumChannels < 1 || 2 < w->NumChannels) return WAVERR_UNSUPP_NUM_CHANNELS;
	if (w->SampleRate == 0) return WAVERR_BAD_SAMPLE_RATE;
	w->AudioFormat = 1; /* uncompressed PCM */
	
	w->BitsPerSample = (w->BitsPerSample + 7) & ~7;
	/* other bit depths may be valid, but these
	 * are the only ones that we support */
	switch (w->BitsPerSample) {
	case 8: w->putchan = put_chan8; w->BlockAlign = 1; break;
	case 16: w->putchan = put_chan16; w->BlockAlign = 2; break;
	case 24: w->putchan = put_chan24; w->BlockAlign = 3; break;
	case 32: w->putchan = put_chan32; w->BlockAlign = 4; break;
	default: return WAVERR_UNSUPP_BITS_PER_SAMPLE;
	}
	w->ByteRate = w->BitsPerSample / 8 * w->NumChannels * w->SampleRate;
	
	putID(ID_RIFF, w);
	//wavsize = getLong(w);
	wavsize = 0xffffffff;
	putLong(wavsize, w); /* XXX */
	
	putID(ID_WAVE, w);
	putID(ID_FMT, w);
	fmtsize = 16;
	putLong(fmtsize, w);
	putWord(w->AudioFormat, w);
	putWord(w->NumChannels, w);
	putLong(w->SampleRate, w);
	putLong(w->ByteRate, w);
	putWord(w->BlockAlign, w);
	putWord(w->BitsPerSample, w);
	
	putID(ID_DATA, w);
	//datasize = getLong(w);
	datasize = 0xffffffff;
	putLong(datasize, w); /* XXX */
	w->size = 0;
	return 0;
}

int wav_get_sample(struct wav *w, long channels[2])
{
	int i;
	long *cp = channels;
	int pad = w->BlockAlign - (w->NumChannels * w->BitsPerSample/8);
	for (i = 0; i < w->NumChannels; ++i)
		*cp++ = w->getchan(w);
	if (w->NumChannels == 1)
		channels[1] = channels[0];
	for (i = 0; i < pad; ++i) (void)getc(w->file);
	return 0;
}

int wav_put_sample(struct wav *w, long channels[2])
{
	int i;
	long *cp = channels;
	int pad = w->BlockAlign - (w->NumChannels * w->BitsPerSample/8);
	for (i = 0; i < w->NumChannels; ++i)
		w->putchan(*cp++, w);
	for (i = 0; i < pad; ++i) putc(0, w->file);
	w->size += w->BlockAlign;
	return 0;
}

/* close an output wav file */
int wav_close(struct wav *w)
{
	if (fseek(w->file, 0x04, SEEK_SET)) return 1;
	putLong(w->size + 36, w);
	if (fseek(w->file, 0x28, SEEK_SET)) return 1;
	putLong(w->size, w);
	return 0;
}
