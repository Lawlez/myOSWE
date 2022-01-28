/*
 * tap.h, prototypes for TAP file routines
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

#ifndef _TAP_H_
#define _TAP_H_

struct tap {
	FILE *file;
	int version;
	unsigned long size;
};

#define V0_LONG_PULSE (8*256)

int tap_read_header(struct tap *t, FILE *f);
int tap_write_header(struct tap *t, FILE *f);
long tap_get_pulse(struct tap *t);
int tap_put_pulse(long p, struct tap *t);
int tap_close(struct tap *t);

#endif
