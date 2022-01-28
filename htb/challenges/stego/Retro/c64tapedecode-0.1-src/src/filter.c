/*
 * filter.c, high-/low-pass signal filter
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

#include "filter.h"

int filter_init(struct filter *fp, long freq, long samplerate)
{
	int size;
	if (freq == 0) {
		fp->window = NULL;
		return 0;
	}
	if (freq > samplerate) freq = samplerate;
	size = samplerate / freq;
	fp->window = malloc(sizeof(unsigned short) * size);
	if (!fp->window)
		return 1;
	memset(fp->window, 0, sizeof(unsigned short) * size);
	fp->size = size;
	fp->pos = 0;
	fp->sum = 0;
	return 0;
}

static void addsample(struct filter *fp, signed short sample)
{
	fp->sum -= fp->window[fp->pos];
	fp->window[fp->pos] = sample;
	fp->sum += fp->window[fp->pos];
	fp->pos = (fp->pos + 1) % fp->size;
}

short filter_lowpass(struct filter *fp, signed short sample)
{
	if (!fp || !fp->window) return sample;
	addsample(fp, sample);
	return fp->sum / fp->size;
}

short filter_highpass(struct filter *fp, signed short sample)
{
	if (!fp || !fp->window) return sample;
	addsample(fp, sample);
	return sample - fp->sum / fp->size;
}
