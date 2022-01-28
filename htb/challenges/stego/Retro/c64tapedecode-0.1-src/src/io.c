/*
 * io.c, common I/O routines for reading/writing word and long values
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

#include "commonio.h"

long fgetlong(FILE *file)
{
	unsigned char b[4];
	fread(b, 1, 4, file);
	return ((unsigned long)b[3] << 24) | ((unsigned long)b[2] << 16) |
	       ((unsigned long)b[1] << 8) | b[0];
}

short fgetword(FILE *file)
{
	unsigned char b[2];
	fread(b, 1, 2, file);
	return ((unsigned long)b[1] << 8) | b[0];
}

long fputlong(long n, FILE *file)
{
	fputc(n&0xff, file);
	fputc((n>>8)&0xff, file);
	fputc((n>>16)&0xff, file);
	fputc((n>>24)&0xff, file);
	return n;
}

short fputword(short n, FILE *file)
{
	fputc(n&0xff, file);
	fputc((n>>8)&0xff, file);
	return n;
}


