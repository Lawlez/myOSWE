/*
 * tap.c, routines for reading/writing TAP files
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

#include "tap.h"
#include "commonio.h"

static const char tapmagic[] = "C64-TAPE-RAW";

int tap_read_header(struct tap *t, FILE *f)
{
	char magic[12];
	char reserved[3];
	t->file = f;
	
	fread(magic, 1, 12, t->file);
	if (memcmp(magic, tapmagic, 12)) return 1;
	t->version = getc(t->file);
	if (t->version & ~1) return 1; /* must be 0 or 1 */
	fread(reserved, 1, 3, t->file);
	if (memcmp(reserved, "\0\0\0", 3)) return 1;
	t->size = fgetlong(t->file);
	return 0;
}

int tap_write_header(struct tap *t, FILE *f)
{
	t->file = f;
	
	if (t->version & ~1) return 1; /* must be 0 or 1 */
	fwrite(tapmagic, 1, 12, t->file);
	putc(t->version, t->file);
	fwrite("\0\0\0", 1, 3, t->file);
	fputlong(0xffffffff, t->file); /* XXX */
	t->size = 0;
	return 0;
}

long tap_get_pulse(struct tap *t)
{
	int c;
	long len;
	c = getc(t->file);
	if (c == 0) {
		if (t->version == 0) {
			len = V0_LONG_PULSE;
		} else {
			len = getc(t->file);
			len |= getc(t->file) << 8;
			len |= getc(t->file) << 16;
		}
	} else {
		len = 8*c;
	}
	if (feof(t->file)) return -1;
	return len;
}

int tap_put_pulse(long len, struct tap *t)
{
	if (len > 8*255) {
		putc(0, t->file);
		++t->size;
		if (t->version != 0) {
			putc(len & 0xff, t->file);
			putc((len>>8) & 0xff, t->file);
			putc((len>>16) & 0xff, t->file);
			t->size += 3;
		}
	} else {
		len = (len + 4) / 8 ? : 1;
		putc(len, t->file);
		++t->size;
	}
	return 0;
}

/* close an output tap file */
int tap_close(struct tap *t)
{
	if (fseek(t->file, 0x10, SEEK_SET)) return 1;
	fputlong(t->size, t->file);
	return 0;
}
