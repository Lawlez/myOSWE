/*
 * mktap.c, make a TAP file from pulse lengths given on standard input
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

#include "tap.h"

int main()
{
	long pulse;
	struct tap tapfile;
	tapfile.version = 1;
	if (tap_write_header(&tapfile, stdout)) {
		fprintf(stderr, "error writing TAP file\n");
		return 1;
	}
	
	while (scanf("%ld", &pulse) == 1) {
		if (pulse <= 0) break;
		tap_put_pulse(pulse, &tapfile);
	}
	tap_close(&tapfile);
	return 0;
}
