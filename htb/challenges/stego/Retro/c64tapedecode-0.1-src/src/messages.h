/*
 * messages.h, macros for verbose messages
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

#ifndef _MESSAGES_H_
#define _MESSAGES_H_

#define MESSAGE(level, ...)                   \
do {                                          \
	if (verbosity >= level)                 \
		fprintf(stderr, __VA_ARGS__); \
} while (0)

enum verbosity {
	VERBOSE_NORMAL,
	VERBOSE_FILE,
	VERBOSE_PACKET,
	VERBOSE_BYTE,
	VERBOSE_BIT,
	VERBOSE_PULSE,
	VERBOSE_WAVEFORM,
	VERBOSE_MAX = VERBOSE_WAVEFORM
};

extern enum verbosity verbosity;

#endif
